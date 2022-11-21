import django_filters
from django.db.models import Q

from .models import (
    City, Airline, Airplane, Airport, AirportTerminal, Flight, 
    TripSource, TripClass, Trip, Seat, Traveller, 
)




### City Filter ###################################################

class CityFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = City
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(country__icontains=value) |
            Q(notes__icontains=value)
        ) 


### Airline Filter #################################################

class AirlineFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Airline
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(country__icontains=value) |
            Q(notes__icontains=value)
        ) 


### Airplane Filter ###################################################

class AirplaneFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Airplane
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(notes__icontains=value)
        ) 


### Airport Filter ###################################################

class AirportFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Airport
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(code__icontains=value) |
            Q(city__name__icontains=value) |
            Q(notes__icontains=value)
        ) 


### Airport Terminal Filter ##########################################

class AirportTerminalFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = AirportTerminal
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(airport__name__icontains=value) |
            Q(notes__icontains=value)
        ) 
 

### Flight Filter #####################################################

class FlightFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Flight
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(airline__name__icontains=value) |
            Q(airplane__name__icontains=value) |
            Q(depart_airport__name__icontains=value) |
            Q(arrive_airport__name__icontains=value) |
            Q(notes__icontains=value)
        ) 


### Trip Source Filter ##################################################

class TripSourceFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = TripSource
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(notes__icontains=value)
        ) 


### Trip Class Filter ############################################

class TripClassFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = TripClass
        fields = ['name', 'airline',  ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(airline__name__icontains=value) |
            Q(notes__icontains=value)
        ) 


### Trip Filter #####################################################

class TripFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Trip
        fields = ['name', 'orig', 'dest']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(orig__name__icontains=value) |
            Q(dest__name__icontains=value) |
            Q(source_found__name__icontains=value) |
            Q(out_class__name__icontains=value) |
            Q(out_first_flight__name__icontains=value) |
            Q(out_first_flight__airline__name__icontains=value) |
            Q(out_first_flight_dep_term__name__icontains=value) |
            Q(out_first_flight_arr_term__name__icontains=value) |
            Q(out_second_flight__name__icontains=value) |
            Q(out_second_flight__airline__name__icontains=value) |
            Q(out_second_flight_dep_term__name__icontains=value) |
            Q(out_second_flight_arr_term__name__icontains=value) |
            Q(ret_class__name__icontains=value) |
            Q(ret_first_flight__name__icontains=value) |
            Q(ret_first_flight__airline__name__icontains=value) |
            Q(ret_first_flight_dep_term__name__icontains=value) |
            Q(ret_first_flight_arr_term__name__icontains=value) |
            Q(ret_second_flight__name__icontains=value) |
            Q(ret_second_flight__airline__name__icontains=value) |
            Q(ret_second_flight_dep_term__name__icontains=value) |
            Q(ret_second_flight_arr_term__name__icontains=value) |
            Q(notes__icontains=value) 
        ) 


### Traveller Filter ###############################################

class TravellerFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Traveller
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(notes__icontains=value)
        )


### Seat Filter ####################################################

class SeatFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Seat
        fields = ['seat_number', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(seat_number__icontains=value) |
            Q(traveller__name__icontains=value) |
            Q(trip__name__icontains=value) |
            Q(notes__icontains=value)
        ) 



