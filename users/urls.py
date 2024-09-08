from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentAPIViewSet, PaymentCreateAPIView, UserCreateAPIView, UserListAPIView, UserUpdateAPIView, \
    UserDestroyAPIView
#from users.views import UserCreateView, email_verification, PasswordResetView
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-create'),
    path('list/', UserListAPIView.as_view(), name='user-retrieve'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-destroy'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('list/', UserListView.as_view(), name='user-list'),
    path('payment/list/', PaymentAPIViewSet.as_view({'get': 'list'}), name='payment-list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    # path('payment/update/<int:pk>/', PaymentUpdateAPIView.as_view(), name='payment-update'),
    # path('payment/delete/<int:pk>/', PaymentDestroyAPIView.as_view(), name='payment-delete'),
    # path('register/', UserCreateView.as_view(), name='register'),
    # path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    # path('reset_password/', PasswordResetView.as_view(), name='reset_password'),
    # path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

]
