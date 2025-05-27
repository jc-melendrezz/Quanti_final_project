from django.urls import path
from .views import login_view, users_view, user_stats_view, logout_view, age_chart_view

urlpatterns = [
    path('', login_view, name="login"),
    path('users/', users_view, name="users"),
    path('user_stats/', user_stats_view, name="user_stats"),
    path('logout/', logout_view, name="logout"),
    path('age_chart/', age_chart_view, name='age_chart')
]