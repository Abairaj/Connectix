from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path(
        "magic-link-request/",
        views.MagicLinkRequestView.as_view(),
        name="magic-link-request",
    ),
    path(
        "magic-link-login/", views.MagicLinkLoginView.as_view(), name="magic-link-login"
    ),
    path(
        "forgot-password/", views.ForgotPasswordView.as_view(), name="forgot-password"
    ),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
]
