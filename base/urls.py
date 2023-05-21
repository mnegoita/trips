from django.urls import path 
from . import views
from trips.views import TripsView


app_name = 'base'


urlpatterns = [
    
    path(r'', TripsView.as_view(), name='home'),
    path(r'search/', views.SearchView.as_view(), name='search'),

] 
