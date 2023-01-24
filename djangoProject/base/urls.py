from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerUser, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('question/<int:pk>/', views.question, name="question"),
    path('create-question/', views.createQuestion, name="create-question"),
    path('update-question/<int:pk>/', views.updateQuestion, name="update-question"),
    path('delete-question/<int:pk>/', views.delete, name="delete-question"),
    path('delete-answer/<int:pk>/', views.deleteAnswer, name="delete-answer"),
    path('delete-comment/<int:pk>/', views.deleteComment, name="delete-comment"),
    path('like-answer/<int:pk>/', views.likeAnswer, name="like-answer"),
    path('dislike-answer/<int:pk>/', views.dislikeAnswer, name="dislike-answer"),
]
