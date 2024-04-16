from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create, name="create"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("item/<int:id>", views.item, name="item"),
    path("Category",views.category, name="category"),
    path("Category/<str:name>", views.OneCat, name="OneCat"),
    path("didIwin",views.didIwin,name="didIwin")
]
