import django_tables2 as tables

from .models import (
    City, Airline, Airplane, Airport, AirportTerminal, Flight, 
    TripSource, TripClass, Trip, Seat, Traveller )




# Base Tables ######################################################

class BaseTable(tables.Table):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.empty_text is None:
            self.empty_text = 'No {} found'.format(self._meta.model._meta.verbose_name_plural)

    class Meta:
        attrs = {
            'class': 'table table-sm'
        }                    


# City Tables ######################################################

class CityTable(BaseTable):
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = City
        fields = ('name', 'country', 'prov_st',)


# Airline Tables ######################################################

class AirlineTable(BaseTable):
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Airline
        fields = ('name', 'country', )


FL_FROM = """
{{ record.depart_airport.city }}
"""
FL_TO = """
{{ record.arrive_airport.city }}
"""
FL_DEPT_TIME = """
{{ record.depart_time }}
"""
FL_ARR_TIME = """
{{ record.arrive_time }}
"""

class AirlineFlightsTable(BaseTable):

    name = tables.LinkColumn()
    
    fl_from = tables.TemplateColumn(template_code=FL_FROM,verbose_name = "From")
    fl_to = tables.TemplateColumn(template_code=FL_TO, verbose_name = "To")
    fl_dept_time = tables.TemplateColumn(template_code=FL_DEPT_TIME, verbose_name = "Depart")
    fl_arr_time = tables.TemplateColumn(template_code=FL_ARR_TIME, verbose_name = "Arrive")
    

    class Meta(BaseTable.Meta):
        model = Flight
        fields = (
            'name', 
            'fl_dept_time', 
            'fl_from', 
            'fl_arr_time', 
            'fl_to',  
            'airplane', 
            'date_found',
        )
        attrs = {
            'class': 'table table-sm card-body'
        } 


# Airplane Tables ###############################################################

class AirplaneTable(BaseTable):
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Airplane
        fields = ( 'name', )


AIRPL_AIRL = """
<a href="{{ record.airline.get_absolute_url }}"> {{ record.airline.name }} </a>
"""

class AirplaneFlightsTable(BaseTable):

    name = tables.LinkColumn(orderable = False)
    airpl_airl = tables.TemplateColumn(
        template_code=AIRPL_AIRL, 
        verbose_name = "Airline",
        orderable = False)
    
    class Meta(BaseTable.Meta):
        model = Flight
        fields = ( 'name', 'airpl_airl',)


# Airport Tables ######################################################################

class AirportTable(BaseTable):
    name = tables.LinkColumn()
    code = tables.Column(orderable=False, )
    city = tables.Column(orderable=False, )

    class Meta(BaseTable.Meta):
        model = Airport
        fields = ('name', 'code', 'city', )


TIME_DEPT = """
{{ record.depart_time }}
"""
DEPT_TO = """
{{ record.arrive_airport.city }}
"""


class AirportDepartTable(BaseTable):
    """
    Table used in Airport Detail View the departing 
    fligts from this airport
    """

    name = tables.LinkColumn(verbose_name = "Depart Flight")
    time_dept = tables.TemplateColumn(template_code=TIME_DEPT, verbose_name = "Time", accessor = 'depart_time')
    dept_to = tables.TemplateColumn(template_code=DEPT_TO, verbose_name = "To", accessor = 'arrive_airport__city')

    class Meta(BaseTable.Meta):
        model = Flight
        fields = ('name', 'airline', 'time_dept', 'dept_to', )
        attrs = {
            'class': 'table table-sm card-body'
        } 


TIME_ARRV = """
{{ record.depart_time }}
"""
ARR_FROM = """
{{ record.depart_airport.city }}
"""

class AirportArriveTable(BaseTable):
    """
    Table used in Airport Detail View the arriving 
    fligts from this airport
    """
    name = tables.LinkColumn(verbose_name = "Arrive Flight")
    time_arrv = tables.TemplateColumn(template_code=TIME_ARRV, verbose_name = "Time", accessor = 'arrive_time')
    arr_from = tables.TemplateColumn(template_code=ARR_FROM, verbose_name = "From", accessor = 'depart_airport__city')

    class Meta(BaseTable.Meta):
        model = Flight
        fields = ('name',  'airline', 'time_arrv', 'arr_from', )
        attrs = {
            'class': 'table table-sm card-body'
        }


# AirportTerminal Tables ########################################################

AT_CITY = """
{{ record.airport.city }}
"""

class AirportTerminalTable(BaseTable):

    name = tables.LinkColumn(orderable = False)
    airport = tables.Column(orderable = False)
    city = tables.TemplateColumn(
        template_code=AT_CITY, 
        orderable=False, 
        verbose_name = "City", 
        accessor = 'airport__city')

    class Meta(BaseTable.Meta):
        model = AirportTerminal
        fields = ('name', 'airport', 'city',)


AT_FL_TO = """
{{ record.arrive_airport.city }}
"""

class AirportTerminalFlightsDepartTable(BaseTable):

    name = tables.LinkColumn(orderable=False,)
    at_fl_to = tables.TemplateColumn(
        template_code=AT_FL_TO, 
        orderable=False, 
        verbose_name = "To", 
        accessor = 'arrive_airport__city')
    depart_time = tables.Column(orderable=False, )

    class Meta(BaseTable.Meta):
        model = Flight
        fields = ('name', 'at_fl_to', 'depart_time',  )
        attrs = {
            'class': 'table table-sm card-body'
        }


AT_FL_FROM = """
{{ record.depart_airport.city }}
"""

class AirportTerminalFlightsArriveTable(BaseTable):

    name = tables.LinkColumn(orderable=False,)
    at_fl_from = tables.TemplateColumn(
        template_code=AT_FL_FROM, 
        orderable=False, 
        verbose_name = "From", 
        accessor = 'depart_airport__city')
    arrive_time = tables.Column(orderable=False, )

    class Meta(BaseTable.Meta):
        model = Flight
        fields = ('name', 'at_fl_from', 'arrive_time')
        attrs = {
            'class': 'table table-sm card-body'
        }


# Flight Tables ##################################################################

FL_DURATION = """
{% load custom_filters %} 
{{ record.duration|floor_div:60 }} h {{ record.duration|modulo:60 }} min 
"""

class FlightTable(BaseTable):

    name = tables.LinkColumn()
    fl_duration = tables.TemplateColumn(
        template_code=FL_DURATION, 
        verbose_name="Duration", 
        accessor="duration"
    )

    class Meta(BaseTable.Meta):
        model = Flight
        fields = ('name',
                  'fl_duration',
                  'airline', 
                  'airplane',                   
                  'depart_airport',
                  'depart_time',
                  'arrive_airport',
                  'arrive_time',
                  ) 


# TripSource Table ##############################################################

class TripSourceTable(BaseTable):
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = TripSource
        fields = ( 'name', )


# TripClass Table ##############################################################

class TripClassTable(BaseTable):
    name = tables.LinkColumn()
    airline = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = TripClass
        fields = ( 'name', 'airline', )


# Trip Tables ###################################################################

# Durations
OUT_DURATION = """
{% load custom_filters %} 
{{ record.out_duration|floor_div:60 }} h {{ record.out_duration|modulo:60 }} min 
"""
OUT_STOP_DURATION = """
{% load custom_filters %} 
{% if record.out_stop_duration %}
    {{ record.out_stop_duration|floor_div:60 }} h {{ record.out_stop_duration|modulo:60 }} min 
{% else %}
    <span> &mdash; </span>
{% endif %}
"""
RET_DURATION = """
{% load custom_filters %} 
{{ record.ret_duration|floor_div:60 }} h {{ record.ret_duration|modulo:60 }} min 
"""
RET_STOP_DURATION = """
{% load custom_filters %} 
{% if record.ret_stop_duration %}
    {{ record.ret_stop_duration|floor_div:60 }} h {{ record.ret_stop_duration|modulo:60 }} min 
{% else %}
    <span> &mdash; </span>
{% endif %}
"""

COL_OUTGOING = """
First Flight: {{ record.out_first_flight }} <br />
{% if record.out_second_flight %}
    Second Flight: {{ record.out_second_flight }} <br />
    {% load custom_filters %} 
    Stop: {{ record.out_stop_duration|floor_div:60 }} h {{ record.out_stop_duration|modulo:60 }} min        
{% endif %}
"""

COL_RETURNING = """
First Flight: {{ record.ret_first_flight }} <br />
{% if record.ret_second_flight %}
    Second Flight: {{ record.ret_second_flight }} <br />
    {% load custom_filters %} 
    Stop: {{ record.ret_stop_duration|floor_div:60 }} h {{ record.ret_stop_duration|modulo:60 }} min  
{% endif %}
"""

COL_PRICE = """
{{ record.price }} {{ record.currency }}
"""

class TripTable(BaseTable):

    name = tables.LinkColumn(
        orderable=False
    )
    col_price = tables.TemplateColumn(
        template_code = COL_PRICE,
        orderable = False,
        verbose_name = "Price"
    )
    trav = tables.Column(
        orderable=False,
        verbose_name = "Trav"
    )
    col_out = tables.TemplateColumn(
        template_code=COL_OUTGOING,
        orderable = False,
        verbose_name = "Outgoing"
    )
    out_duration = tables.TemplateColumn(
        template_code=OUT_DURATION,
        orderable = False,
        verbose_name = "Duration"
    )
    col_ret = tables.TemplateColumn(
        template_code=COL_RETURNING,
        orderable = False,
        verbose_name = "Returning"
    )
    ret_duration = tables.TemplateColumn(
        template_code=RET_DURATION,
        orderable = False,
        verbose_name = "Duration"
    )

    class Meta(BaseTable.Meta):
        model = Trip
        fields = [
            'name',
            'col_price',
            'trav',
            'col_out',
            'out_duration',
            'col_ret',
            'ret_duration',
        ]


class FlightTripsTable(BaseTable):
    """
    Table use in the Flight Detail view to show trips
    which contain this specific flight
    """
    name = tables.LinkColumn(
        orderable = False,
    )
    price = tables.LinkColumn(
        orderable = False,
    )

    class Meta(BaseTable.Meta):
        model = Trip
        fields = (
            'name',
            'price',
        )


# Traveller Tables #########################################

TR_SEAT = """
<table>
{% for seat in  record.seats_traveller.all %}
<tr><td>{{ seat.seat_number }}</td></tr>
{% endfor %}
</table>
"""
TR_TRIP = """
<table>
{% for seat in  record.seats_traveller.all %}
<tr><td>{{ seat.trip }}</td></tr>
{% endfor %}
</table>
"""


class TravellerTable(BaseTable):
    name = tables.LinkColumn()
    tr_seat = tables.TemplateColumn(template_code=TR_SEAT, verbose_name="Seats", orderable=False)
    tr_trip = tables.TemplateColumn(template_code=TR_TRIP, verbose_name="Trips", orderable=False)

    class Meta(BaseTable.Meta):
        model = Traveller
        fields = ('name', 'tr_seat', 'tr_trip', )


# Seat Table #############################################

class SeatTable(BaseTable):
    seat_number = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Seat
        fields = ('seat_number', 'trip', 'flight', 'traveller', )


TRAV_SEAT = """
{{ record.seat_number }}
"""
TRAV_TRIP = """
<a href="{{ record.trip.get_absolute_url }}"> {{ record.trip }} </a>
"""
TRAV_FL = """
<a href="{{ record.flight.get_absolute_url }}"> {{ record.flight }} </a>
"""

class TravellerSeatsTable(BaseTable):
    trav_seat = tables.TemplateColumn(template_code=TRAV_SEAT, verbose_name = "Seat", orderable=False)
    trav_trip = tables.TemplateColumn(template_code=TRAV_TRIP, verbose_name = "Trip", orderable=False)
    trav_fl = tables.TemplateColumn(template_code=TRAV_FL, verbose_name = "Flight", orderable=False)

    class Meta(BaseTable.Meta):
        model = Seat
        fields = ('trav_seat', 'trav_trip', 'trav_fl', )

