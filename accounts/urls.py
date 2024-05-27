from django.urls import path
from .views import PasswordResetView, PasswordResetConfirmView, UserOrdersView, UserProfileView, UserSignupView, UserLoginView

urlpatterns = [
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('user/', UserProfileView.as_view(), name='user-profile'),
    path('user/orders/', UserOrdersView.as_view(), name='user-orders'),
]
