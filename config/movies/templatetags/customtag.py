from django import template

register = template.Library()

@register.filter
def customMovieList(movies):
    size = 5
    return [movies[i:i + size] for i in range(len(movies) - size)]