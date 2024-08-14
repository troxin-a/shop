from django.urls import path
from users.apps import UsersConfig
from users import views
from django.contrib.auth.views import LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path("login", views.CustomLoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("register", views.UserCreateView.as_view(), name="register"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path("user-created", views.user_created, name="user_created"),
    path("confirm-email/<str:token>/", views.confirm_email, name="confirm_email"),

    # Автоматическая генерация пароля
    path("reset-pass", views.ResetPassView.as_view(), name="reset_pass"),


    # Сброс пароля нормальный
    path("reset-password/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path("reset-password/done", views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
]
