from django.urls import path 
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'trips'


urlpatterns = [

    path('cities/', views.CityTableView.as_view(), name='city_list'),
    path('cities/add/', login_required(views.CityCreateView.as_view()), name='city_add'),
    path('cities/search-results/', views.CitySearchResultsView.as_view(), name='city_search'),
    path('cities/<int:pk>/', views.CityDetailView.as_view(), name='city'),
    path('cities/<int:pk>/edit/', login_required(views.CityEditView.as_view()), name='city_edit'),
    path('cities/<int:pk>/delete/', login_required(views.CityDeleteView.as_view()), name='city_delete'),

    path('airlines/', views.AirlineTableView.as_view(), name='airline_list'), 
    path('airlines/add/', login_required(views.AirlineCreateView.as_view()), name='airline_add'),
    path('airlines/search-results/', views.AirlineSearchResultsView.as_view(), name='airline_search'),
    path('airlines/<int:pk>/', views.AirlineDetailView.as_view(), name='airline'),
    path('airlines/<int:pk>/edit/', login_required(views.AirlineEditView.as_view()), name='airline_edit'),
    path('airlines/<int:pk>/delete/', login_required(views.AirlineDeleteView.as_view()), name='airline_delete'),

    path('airplanes/', views.AirplaneListView.as_view(), name='airplane_list'),    
    path('airplanes/add/', login_required(views.AirplaneCreateView.as_view()), name='airplane_add'),
    path('airplanes/search-results/', views.AirplaneSearchResultsView.as_view(), name='airplane_search'),
    path('airplanes/<int:pk>/', views.AirplaneDetailView.as_view(), name='airplane'),
    path('airplanes/<int:pk>/edit/', login_required(views.AirplaneEditView.as_view()), name='airplane_edit'),
    path('airplanes/<int:pk>/delete/', login_required(views.AirplaneDeleteView.as_view()), name='airplane_delete'),
 
    path('airports/', views.AirportTableView.as_view(), name='airport_list'),     
    path('airports/add/', login_required(views.AirportCreateView.as_view()), name='airport_add'),
    path('airports/search-results/', views.AirportSearchResultsView.as_view(), name='airport_search'),
    path('airports/<int:pk>/', views.AirportDetailView.as_view(), name='airport'),
    path('airports/<int:pk>/edit/', login_required(views.AirportEditView.as_view()), name='airport_edit'),
    path('airports/<int:pk>/delete/', login_required(views.AirportDeleteView.as_view()), name='airport_delete'),

    path('airportterminals/', views.AirportTerminalTableView.as_view(), name='airportterminal_list'),    
    path('airportterminals/add/', login_required(views.AirportTerminalCreateView.as_view()), name='airportterminal_add'),
    path('airportterminals/search-results/', views.AirportTerminalSearchResultsView.as_view(), name='airportterminal_search'),
    path('airportterminals/<int:pk>/', views.AirportTerminalDetailView.as_view(), name='airportterminal'),
    path('airportterminals/<int:pk>/edit/', login_required(views.AirportTerminalEditView.as_view()), name='airportterminal_edit'),
    path('airportterminals/<int:pk>/delete/', login_required(views.AirportTerminalDeleteView.as_view()), name='airportterminal_delete'),

    path('flights/', views.FlightTableView.as_view(), name='flight_list'),   
    path('flights/add/', login_required(views.FlightCreateView.as_view()), name='flight_add'),
    path('flights/search-results/', views.FlightSearchResultsView.as_view(), name='flight_search'),
    path('flights/<int:pk>/', views.FlightDetailView.as_view(), name='flight'),
    path('flights/<int:pk>/edit/', login_required(views.FlightEditView.as_view()), name='flight_edit'),
    path('flights/<int:pk>/delete/', login_required(views.FlightDeleteView.as_view()), name='flight_delete'),

    path('tripsources/', views.TripSourceListView.as_view(), name='tripsource_list'),   
    path('tripsources/add/', login_required(views.TripSourceCreateView.as_view()), name='tripsource_add'),
    path('tripsources/search-results/', views.TripSourceSearchResultsView.as_view(), name='tripsource_search'),
    path('tripsources/<int:pk>/', views.TripSourceDetailView.as_view(), name='tripsource'),
    path('tripsources/<int:pk>/edit/', login_required(views.TripSourceEditView.as_view()), name='tripsource_edit'),
    path('tripsources/<int:pk>/delete/', login_required(views.TripSourceDeleteView.as_view()), name='tripsource_delete'),

    path('tripclass/', views.TripClassListView.as_view(), name='tripclass_list'),   
    path('tripclass/add/', login_required(views.TripClassCreateView.as_view()), name='tripclass_add'),
    path('tripclass/search-results/', views.TripClassSearchResultsView.as_view(), name='tripclass_search'),
    path('tripclass/<int:pk>/', views.TripClassDetailView.as_view(), name='tripclass'),
    path('tripclass/<int:pk>/edit/', login_required(views.TripClassEditView.as_view()), name='tripclass_edit'),
    path('tripclass/<int:pk>/delete/', login_required(views.TripClassDeleteView.as_view()), name='tripclass_delete'),

    path('trips/', views.TripsView.as_view(), name='trip_list'),    
    path('trips/add/', login_required(views.TripCreateView.as_view()), name='trip_add'),
    path('trips/search-results/', views.TripSearchResultsView.as_view(), name='trip_search'),
    path('trips/<int:pk>/', views.TripDetailView.as_view(), name='trip'),
    path('trips/<int:pk>/edit/', login_required(views.TripEditView.as_view()), name='trip_edit'),
    path('trips/<int:pk>/delete/', login_required(views.TripDeleteView.as_view()), name='trip_delete'),

    path('travellers/', views.TravellerListView.as_view(), name='traveller_list'),    
    path('travellers/add/', login_required(views.TravellerCreateView.as_view()), name='traveller_add'),
    path('travellers/search-results/', views.TravellerSearchResultsView.as_view(), name='traveller_search'),
    path('travellers/<int:pk>/', views.TravellerDetailView.as_view(), name='traveller'),
    path('travellers/<int:pk>/edit/', login_required(views.TravellerEditView.as_view()), name='traveller_edit'),
    path('travellers/<int:pk>/delete/', login_required(views.TravellerDeleteView.as_view()), name='traveller_delete'),

    path('seats/', views.SeatTableView.as_view(), name='seat_list'),    
    path('seats/add/', login_required(views.SeatCreateView.as_view()), name='seat_add'),
    path('seats/search-results/', views.SeatSearchResultsView.as_view(), name='seat_search'),
    path('seats/<int:pk>/', views.SeatDetailView.as_view(), name='seat'),
    path('seats/<int:pk>/edit/', login_required(views.SeatEditView.as_view()), name='seat_edit'),
    path('seats/<int:pk>/delete/', login_required(views.SeatDeleteView.as_view()), name='seat_delete'),
] 
