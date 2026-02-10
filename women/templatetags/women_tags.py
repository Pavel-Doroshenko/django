"""Категории известных женщин"""
from django import template
from django.db.models import Count

from women.models import Category, TagPost
from women.utils import menu

register = template.Library()


@register.inclusion_tag("women/list_categories.html")
def show_categories(cat_selected_id=0):
    """Категории"""
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {"cats": cats, "cat_selected": cat_selected_id}


@register.inclusion_tag("women/list_tags.html")
def show_all_tags():
    """Тэг"""
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}


@register.simple_tag
def get_menu():
    """Меню"""
    return menu
