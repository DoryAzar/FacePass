from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("personalinformation", views.personal_information_view,
         name="personal_information"),
    path("passes", views.passes_view, name="passes"),
    path("onboard", views.onboard_view, name="onboard"),
    path("testcompany", views.testcompany_view, name="testcompany"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("message", views.message, name="message"),
    path("pass/<str:token>", views.protected_view, name="protected"),

    # API routes
    path("api/identify", views.identify, name="identify"),
    path("api/pass", views.resolve_pass, name="resolve_pass")
]
