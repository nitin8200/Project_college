from django.shortcuts import render, get_object_or_404
from .models import Tool
# Create your views here.
def browse(request):
    
    tools = Tool.objects.all()
    categories = Tool.objects.values('category').distinct()
    featured_tools = Tool.objects.filter(is_featured=True)
    context = {
        'tools': tools,
        'categories': categories,
        'featured_tools': featured_tools,
    }
    return render(request, "browse.html", context)

def compare(request):
    return render(request,"compare.html")

def toolDetails(request, tool_id):

    tool = get_object_or_404(Tool, id=tool_id)
    print(tool.name)
    context = {
        "tool": tool
    }

    return render(request,"product_details.html", context=context)