from django.urls import path
from . import views

app_name = 'teamoperation'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_operative/', views.operative_create_view, name='create_operative'),
    path('create_mission/', views.mission_create_view, name='create_mission'),
    path('create_team/', views.team_create_view, name='create_team'),
    path('search/', views.operative_list_view, name='search_operative'),
    path('<int:get_operative>/edit_operative/', views.operative_edit_display, name='edit_operative'),
    path('<int:op_id>/edit_fin/', views.operative_edit_submit, name='operative_edit_submit'),
    path('search_team/', views.team_list_view, name='search_team'),
    path('<int:get_team>/edit_team/', views.team_edit_display, name='edit_team'),
    path('<int:team_id>/create_mission/', views.mission_create_for_team, name='create_mission_for_team'),

]