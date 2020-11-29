from django import template

register = template.Library()

@register.filter
def customMovieList(movies):
    size = 5 if len(movies) >= 5 else len(movies)
    return [movies[i:i + size] for i in range(len(movies) - size + 1)]
