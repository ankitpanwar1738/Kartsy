from django import template

register = template.Library()

@register.filter
def star_range(rating):
    try:
        rating = float(rating)
    except (ValueError, TypeError):
        rating = 0.0

    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    return ['full'] * full_stars + ['half'] * half_star + ['empty'] * empty_stars
