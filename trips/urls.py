from django.urls import path 
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'trips'


urlpatterns = [

    path('cities/', views.CityTable.as_view(), name='city_list'),
    path('cities/add/', login_required(views.CityCreate.as_view()), name='city_add'),
    path('cities/search-results/', views.CitySearchResults.as_view(), name='city_search'),
    path('cities/<int:pk>/', views.CityDetail.as_view(), name='city'),
    path('cities/<int:pk>/edit/', login_required(views.CityEdit.as_view()), name='city_edit'),
    path('cities/<int:pk>/delete/', login_required(views.CityDelete.as_view()), name='city_delete'),

    path('airlines/', views.AirlineTable.as_view(), name='airline_list'),  
    path('airlines/add/', login_required(views.AirlineCreate.as_view()), name='airline_add'),
    path('airlines/search-results/', views.AirlineSearchResults.as_view(), name='airline_search'),
    path('airlines/<int:pk>/', views.AirlineDetail.as_view(), name='airline'),
    path('airlines/<int:pk>/edit/', login_required(views.AirlineEdit.as_view()), name='airline_edit'),
    path('airlines/<int:pk>/delete/', login_required(views.AirlineDelete.as_view()), name='airline_delete'),

    path('airplanes/', views.AirplaneList.as_view(), name='airplane_list'),    
    path('airplanes/add/', login_required(views.AirplaneCreate.as_view()), name='airplane_add'),
    path('airplanes/search-results/', views.AirplaneSearchResults.as_view(), name='airplane_search'),
    path('airplanes/<int:pk>/', views.AirplaneDetail.as_view(), name='airplane'),
    path('airplanes/<int:pk>/edit/', login_required(views.AirplaneEdit.as_view()), name='airplane_edit'),
    path('airplanes/<int:pk>/delete/', login_required(views.AirplaneDelete.as_view()), name='airplane_delete'),
 
    path('airports/', views.AirportTable.as_view(), name='airport_list'),     
    path('airports/add/', login_required(views.AirportCreate.as_view()), name='airport_add'),
    path('airports/search-results/', views.AirportSearchResults.as_view(), name='airport_search'),
    path('airports/<int:pk>/', views.AirportDetail.as_view(), name='airport'),
    path('airports/<int:pk>/edit/', login_required(views.AirportEdit.as_view()), name='airport_edit'),
    path('airports/<int:pk>/delete/', login_required(views.AirportDelete.as_view()), name='airport_delete'),

    path('airportterminals/', views.AirportTerminalTable.as_view(), name='airportterminal_list'),    
    path('airportterminals/add/', login_required(views.AirportTerminalCreate.as_view()), name='airportterminal_add'),
    path('airportterminals/search-results/', views.AirportTerminalSearchResults.as_view(), name='airportterminal_search'),
    path('airportterminals/<int:pk>/', views.AirportTerminalDetail.as_view(), name='airportterminal'),
    path('airportterminals/<int:pk>/edit/', login_required(views.AirportTerminalEdit.as_view()), name='airportterminal_edit'),
    path('airportterminals/<int:pk>/delete/', login_required(views.AirportTerminalDelete.as_view()), name='airportterminal_delete'),

    path('flights/', views.FlightTable.as_view(), name='flight_list'),   
    path('flights/add/', login_required(views.FlightCreate.as_view()), name='flight_add'),
    path('flights/search-results/', views.FlightSearchResults.as_view(), name='flight_search'),
    path('flights/<int:pk>/', views.FlightDetail.as_view(), name='flight'),
    path('flights/<int:pk>/edit/', login_required(views.FlightEdit.as_view()), name='flight_edit'),
    path('flights/<int:pk>/delete/', login_required(views.FlightDelete.as_view()), name='flight_delete'),

    path('tripsources/', views.TripSourceList.as_view(), name='tripsource_list'),   
    path('tripsources/add/', login_required(views.TripSourceCreate.as_view()), name='tripsource_add'),
    path('tripsources/search-results/', views.TripSourceSearchResults.as_view(), name='tripsource_search'),
    path('tripsources/<int:pk>/', views.TripSourceDetail.as_view(), name='tripsource'),
    path('tripsources/<int:pk>/edit/', login_required(views.TripSourceEdit.as_view()), name='tripsource_edit'),
    path('tripsources/<int:pk>/delete/', login_required(views.TripSourceDelete.as_view()), name='tripsource_delete'),

    path('tripclass/', views.TripClassList.as_view(), name='tripclass_list'),   
    path('tripclass/add/', login_required(views.TripClassCreate.as_view()), name='tripclass_add'),
    path('tripclass/search-results/', views.TripClassSearchResults.as_view(), name='tripclass_search'),
    path('tripclass/<int:pk>/', views.TripClassDetail.as_view(), name='tripclass'),
    path('tripclass/<int:pk>/edit/', login_required(views.TripClassEdit.as_view()), name='tripclass_edit'),
    path('tripclass/<int:pk>/delete/', login_required(views.TripClassDelete.as_view()), name='tripclass_delete'),

    path('trips/', views.TripList.as_view(), name='trip_list'),    
    path('trips/add/', login_required(views.TripCreate.as_view()), name='trip_add'),
    path('trips/search-results/', views.TripSearchResults.as_view(), name='trip_search'),
    path('trips/<int:pk>/', views.TripDetail.as_view(), name='trip'),
    path('trips/<int:pk>/edit/', login_required(views.TripEdit.as_view()), name='trip_edit'),
    path('trips/<int:pk>/delete/', login_required(views.TripDelete.as_view()), name='trip_delete'),

    path('travellers/', views.TravellerList.as_view(), name='traveller_list'),    
    path('travellers/add/', login_required(views.TravellerCreate.as_view()), name='traveller_add'),
    path('travellers/search-results/', views.TravellerSearchResults.as_view(), name='traveller_search'),
    path('travellers/<int:pk>/', views.TravellerDetail.as_view(), name='traveller'),
    path('travellers/<int:pk>/edit/', login_required(views.TravellerEdit.as_view()), name='traveller_edit'),
    path('travellers/<int:pk>/delete/', login_required(views.TravellerDelete.as_view()), name='traveller_delete'),

    path('seats/', views.SeatTable.as_view(), name='seat_list'),    
    path('seats/add/', login_required(views.SeatCreate.as_view()), name='seat_add'),
    path('seats/search-results/', views.SeatSearchResults.as_view(), name='seat_search'),
    path('seats/<int:pk>/', views.SeatDetail.as_view(), name='seat'),
    path('seats/<int:pk>/edit/', login_required(views.SeatEdit.as_view()), name='seat_edit'),
    path('seats/<int:pk>/delete/', login_required(views.SeatDelete.as_view()), name='seat_delete'),
] 

 



