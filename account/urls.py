from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from account.views import SignUpView, ProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('profile/', ProfileView.as_view()),
]