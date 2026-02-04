from django.urls import path, register_converter

from . import views
from . import converters
from .views import WomenCategory, WomenHome, AddPage, TagPostList

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", WomenHome.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("addpage/", AddPage.as_view(), name="add_page"),
    path("contact/", views.contact, name="contact"),
    path("login/", views.login, name="login"),
    path("post/<slug:post_slug>/", views.ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", WomenCategory.as_view(), name="category"),
    path("tag/<slug:tag_slug>/", TagPostList.as_view(), name="tag"),
    path("edit/<slug:slug>/", views.UpdatePage.as_view(), name="edit_page"),
]
