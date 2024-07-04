from django.urls import path
from . import views

urlpatterns = [
    path('', views.post, name='post'),
    path('post/<str:category_name>/', views.post_category, name='post_category'),
    path('write/', views.postwrite, name='postwrite'),
    path('<int:pk>/', views.postdetail, name='postdetail'),
    path('<int:pk>/edit/', views.postedit, name='postedit'),
    path('<int:pk>/delete/', views.postdelete, name='postdelete'),
    path('<int:pk>/like/', views.post_like, name='post_like'),
    path('comment/<int:pk>/like/', views.comment_like, name='comment_like'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]