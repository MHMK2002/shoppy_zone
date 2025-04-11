from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from account.views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
]