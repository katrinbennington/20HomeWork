from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserListView, PaymentAPIViewSet, PaymentCreateAPIView
#from users.views import UserCreateView, email_verification, PasswordResetView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('payment/list/', PaymentAPIViewSet.as_view({'get': 'list'}), name='payment-list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    # path('payment/update/<int:pk>/', PaymentUpdateAPIView.as_view(), name='payment-update'),
    # path('payment/delete/<int:pk>/', PaymentDestroyAPIView.as_view(), name='payment-delete'),
    # path('register/', UserCreateView.as_view(), name='register'),
    # path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    # path('reset_password/', PasswordResetView.as_view(), name='reset_password'),
    # path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

]
