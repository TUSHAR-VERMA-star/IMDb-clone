from django.urls import path
from watchlist_app.api import views

urlpatterns = [
    path('list/',views.WatchlistGV.as_view()),
    path('platform/', views.StreamingPlatformGV.as_view()),
    path('list/<int:pk>/', views.WatchDetails.as_view()),
    path('platform/<int:pk>/', views.StreamingPlatformDetails.as_view()),
    path('list/<int:pk>/reviews/', views.ReviewList.as_view()),
    path('review/<int:pk>/', views.ReviewDetail.as_view()),
    path('list/<int:pk>/review-create/', views.ReviewCreate.as_view())
]
