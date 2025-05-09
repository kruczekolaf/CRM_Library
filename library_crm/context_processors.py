from django.conf import settings

def navbar_context(request):
    show_navbar = request.resolver_match and request.resolver_match.url_name not in settings.NAVBAR_EXCLUDED_PAGES
    return {'show_navbar': show_navbar}