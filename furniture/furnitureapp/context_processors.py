from .models import Category

def category_menu(request):
    selected_category = request.GET.get("category", "")
    categories = Category.objects.all()

    return {
        "categories": categories,
        "selected_category": selected_category
    }
