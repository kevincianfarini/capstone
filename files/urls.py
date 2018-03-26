from django.urls import path
from files.views import ContentView

urlpatterns = [
    path('content/<int:id>/', ContentView.as_view())
]