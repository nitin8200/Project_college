from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Tool, Category, Review

def browse(request):
    tools = Tool.objects.all()
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    selected_pricing = request.GET.get('pricing')
    if selected_category:
        tools = tools.filter(category_id=selected_category)
    if selected_pricing:
        tools = tools.filter(pricing=selected_pricing)
    # Get bookmarked tool ids for the current user
    bookmarked_ids = []
    if request.user.is_authenticated:
        bookmarked_ids = request.user.bookmarked_tools.values_list('id', flat=True)
    return render(request, 'browse.html', {
        'tools': tools,
        'categories': categories,
        'selected_category': selected_category,
        'selected_pricing': selected_pricing,
        'bookmarked_ids': bookmarked_ids,
    })

def compare(request):
    tool_ids = request.GET.getlist('tools')
    # Only keep unique, non-empty IDs
    tool_ids = [tid for tid in tool_ids if tid]
    if len(tool_ids) >= 2:
        tools = Tool.objects.filter(id__in=tool_ids)
        all_tools = Tool.objects.exclude(id__in=tool_ids)
        current_ids = tool_ids
    else:
        # Show first 2 tools by default if none or only one selected
        tools = Tool.objects.all()[:2]
        all_tools = Tool.objects.exclude(id__in=[tool.id for tool in tools])
        current_ids = [str(tool.id) for tool in tools]

    features = [
        {'name': 'Category', 'values': [tool.category.name for tool in tools]},
        {'name': 'Pricing', 'values': [tool.pricing for tool in tools]},
        {'name': 'Rating', 'values': [f"{tool.rating:.1f}/5.0" for tool in tools]},
        {'name': 'Description', 'values': [tool.description for tool in tools]},
    ]
    context = {
        'tools': tools,
        'all_tools': all_tools,
        'current_ids': current_ids,
        'features': features,
    }
    return render(request, "compare.html", context)

def toolDetails(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    reviews = tool.reviews.select_related('user').all()
    if request.method == "POST" and request.user.is_authenticated:
        rating = int(request.POST.get("rating", 5))
        comment = request.POST.get("comment", "").strip()
        if comment:
            Review.objects.create(tool=tool, user=request.user, rating=rating, comment=comment)
            messages.success(request, "Your review has been submitted.")
            return redirect('toolDetails', tool_id=tool.id)
        else:
            messages.error(request, "Comment cannot be empty.")
    context = {
        "tool": tool,
        "reviews": reviews
    }
    return render(request, "product_details.html", context=context)

@require_POST
def rate_tool(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    try:
        rating = float(request.POST.get("rating"))
        # Simple average update (replace with your own logic if you have user-based ratings)
        tool.rating = (tool.rating + rating) / 2
        tool.save()
    except Exception:
        pass
    # Redirect back to the referring page
    return redirect(request.META.get('HTTP_REFERER', '/compare/'))

@login_required
def toggle_bookmark(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    if tool in request.user.bookmarked_tools.all():
        request.user.bookmarked_tools.remove(tool)
        status = 'removed'
    else:
        request.user.bookmarked_tools.add(tool)
        status = 'added'
    # If AJAX request, return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status})
    # Otherwise, redirect back to bookmarks page
    return redirect('bookmarked_tools')

@login_required
def profile(request):
    bookmarks = request.user.bookmarked_tools.all()
    return render(request, 'profile.html', {'bookmarks': bookmarks})

def search_results(request):
    query = request.GET.get('query', '')
    tools = Tool.objects.filter(name__icontains=query) if query else []
    return render(request, 'search_results.html', {'tools': tools, 'query': query})

@login_required
def bookmarked_tools(request):
    bookmarks = request.user.bookmarked_tools.all()
    return render(request, 'bookmarked_tools.html', {'bookmarks': bookmarks})