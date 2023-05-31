from .models import Category, SocialLink


def get_categories(request):
    categories = Category.objects.all()
    social_apps = SocialLink.objects.all()
    return dict(
        tags=categories, social_apps=social_apps
    )  # This function only return the dictionary
