from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Tool, Category

def browse(request):
    category_id = request.GET.get('category')  # Get the category ID from query parameters
    if category_id:
        tools = Tool.objects.filter(category=category_id)  # Filter tools by category
    else:
        tools = Tool.objects.all()  # Show all tools if no category is selected

    categories = Category.objects.all()  # Fetch all categories
    featured_tools = Tool.objects.filter(is_featured=True)  # Fetch featured tools

    context = {
        'tools': tools,
        'categories': categories,
        'featured_tools': featured_tools,
        'selected_category': int(category_id) if category_id else None,  # Pass selected category ID
    }
    return render(request, "browse.html", context)

def compare(request):
    tool_ids = request.GET.getlist('tools')
    tools = Tool.objects.filter(id__in=tool_ids)
    all_tools = Tool.objects.exclude(id__in=tool_ids)
    current_ids = tool_ids
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
    context = {
        "tool": tool
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