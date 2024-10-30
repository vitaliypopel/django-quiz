def get_color_theme(request):
    return {
        'theme': request.COOKIES.get('theme', 'dark'),
        'color_theme': request.COOKIES.get('color_theme', 'success'),
    }
