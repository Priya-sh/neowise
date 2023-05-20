from django.urls import path
from transactions import views

urlpatterns = [
	path('user/', views.home),
]