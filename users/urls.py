from django.urls import path
from .views import RegisterUserView, LoginUserView, UserDetailsView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('<int:id>/', UserDetailsView.as_view(), name='user-details'),
]
