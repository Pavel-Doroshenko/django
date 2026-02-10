"""context_processors"""
from women.utils import menu


def get_women_context(_request):
    """Отображение меню"""
    return {"main_menu": menu}
