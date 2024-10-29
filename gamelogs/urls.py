from django.urls import path

from . import views

app_name = "gamelogs"
urlpatterns = [
    path("", views.index, name="index"),
    path("add_user/", views.add_user, name='add_user'),
    path('select_dashboard/', views.select_dashboard, name='select_dashboard'),
    path('review_dashboard/', views.review_dashboard, name='review_dashboard'),
    path('add_review/', views.add_review, name='add_review'),
    path('update_review/<int:review_id>/', views.update_review, name='update_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]
