from django.urls import path
from files.views import ContentView, ListTagAPIView

urlpatterns = [
    path('content/<int:id>/', ContentView.as_view()),
    path('tags/', ListTagAPIView.as_view())
]