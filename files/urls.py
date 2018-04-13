from django.urls import path
from files.views import ContentView, ListTagAPIView, ListBlogPostAPIView

urlpatterns = [
    path('content/<int:id>/', ContentView.as_view()),
    path('tags/', ListTagAPIView.as_view()),
    path('', ListBlogPostAPIView.as_view())
]