from .models import Category


def get_categories(request):
    categories = Category.objects.all()
    return dict(tags=categories)  # This function only return the dictionary
