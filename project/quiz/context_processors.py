def get_color_theme(request):
    return {'color_theme': request.COOKIES.get('color_theme', 'success')}
