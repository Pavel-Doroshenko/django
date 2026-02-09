# pylint disable=duplicate-code
# from winreg import CreateKey
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from women.forms import AddPostForm
from women.models import Women, TagPost
#from django.views.generic import ListView
from women.utils import DataMixin

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


# Create your views here.
# def index(request):
#     #posts = Women.published.all()
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': Women.published.all().select_related('cat'),
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=data)


class WomenHome(DataMixin, ListView):
    # model = Women
    template_name = "women/index.html"
    context_object_name = "posts"
    # paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(
            super().get_context_data(**kwargs),
            title="Главная страница",
            cat_selected=0,
        )

    def get_queryset(self):
        return Women.published.all().select_related("cat")


def page_not_found(_request, _exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


@login_required(login_url="/admin/")
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "women/about.html", {"page_obj": page_obj, "title": "О сайте"}
    )


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'women/post.html', context=data)


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"])

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#     }
#
#     return render(request,'women/addpage.html', {'menu': menu,
#                                                  'title': 'Добавление статьи', 'form': form})


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    # model = Women
    # fields = ['title', 'slug', 'content', 'is_published', 'cat']
    form_class = AddPostForm
    template_name = "women/addpage.html"
    # success_url = reverse_lazy('home')
    title_page = "Добавление статьи"
    permission_required = "women.add_women"
    # extra_context = {
    #     'menu': menu,
    #     'title': 'Добавление статьи'
    # }

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Редактирование статьи"
    permission_required = "women.change_women"
    # extra_context = {
    #     'menu': menu,
    #     'title': 'Редактирование статьи'
    # }


@permission_required(perm="women.add_women", raise_exception=True)
def contact(_request):
    return HttpResponse("Обратная связь")


def login(_request):
    return HttpResponse("Авторизация")


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk)
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#
#     return render(request, 'women/index.html', context=data)


class WomenCategory(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        return self.get_mixin_context(
            context,
            title="Категория - " + cat.name,
            cat_selected=cat.id,
        )

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related(
            "cat"
        )


#     def show_tag_post_list(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'women/index.html', context=data)


class TagPostList(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(context, title="Тег: " + tag.tag)

    def get_queryset(self):
        """ функция опубликованные посты по slug"""
        return Women.published.filter(
            tags__slug=self.kwargs["tag_slug"]
        ).select_related("cat")
