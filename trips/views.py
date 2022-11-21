from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django_tables2 import RequestConfig
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect

from base.views import (
    BaseItemsList, BaseItemsTable, BaseItemsSearchResults, BaseItemCreateWithPopup, BaseItemEdit
)

from .models import (
    City, Airline, Airplane, Airport, AirportTerminal, Flight, 
    TripSource, TripClass, Trip, Seat, Traveller )

from .forms import (
    CityForm, AirlineForm, AirplaneForm, AirportForm, AirportTerminalForm, 
    FlightForm, TripSourceForm, TripClassForm, 
    TripForm, SeatForm, TravellerForm )

from .tables import (
    CityTable, AirlineTable, AirplaneTable, AirportTable, AirportTerminalTable,
    FlightTable, FlightTripsTable, SeatTable, TravellerTable, 
    AirportDepartTable, AirportArriveTable, AirlineFlightsTable, AirplaneFlightsTable,
    AirportTerminalFlightsDepartTable, AirportTerminalFlightsArriveTable,
    TravellerSeatsTable, TripClassTable, TripSourceTable, TripTable)

from .filters import (
    CityFilter, AirlineFilter, AirplaneFilter, AirportFilter, AirportTerminalFilter,
    FlightFilter, TripClassFilter, TripSourceFilter, TripFilter, SeatFilter, TravellerFilter)

# Paths for common templates
template_path = 'trips/'
search_results_template = "base/search_results.html"
confirm_delete_template = "base/item_confirm_delete.html"




# City Views ############################################################

class CityTable(BaseItemsTable):
    model = City
    table = CityTable
    filter = CityFilter
    queryset = City.objects.all()    


class CitySearchResults(BaseItemsSearchResults):
    model = City
    table = CityTable
    filter = CityFilter
    queryset = City.objects.all()


class CityDetail(DetailView):
    model = City
    template_name = template_path + 'city_detail.html'


class CityCreate(BaseItemCreateWithPopup):
    model = City
    form_class = CityForm
    template_name = template_path + 'city_form.html'
    template_name_popup = template_path + 'city_form_popup.html'
    cancel_button_url = reverse_lazy('trips:city_list')  


class CityEdit(BaseItemEdit):
    model = City
    form_class = CityForm
    template_name = template_path + 'city_form.html'


class CityDelete(DeleteView):
    model = City
    success_url = reverse_lazy('trips:city_list')
    template_name = confirm_delete_template

    def get_dependencies(self):

        deps = []

        airports_deps = []
        for airport in self.object.airports.all():
            airports_deps.append(airport)
        if airports_deps:
            deps.append({'Airports': airports_deps})

        trips_orig_deps = []
        for trip_orig in self.object.trips_orig.all():
            trips_orig_deps.append(trip_orig)
        if trips_orig_deps:
            deps.append({'Trips Origin Cities': trips_orig_deps})

        trips_dest_deps = []
        for trip_dest in self.object.trips_dest.all():
            trips_dest_deps.append(trip_dest)
        if trips_dest_deps:
            deps.append({'Trips Destination Cities': trips_dest_deps}) 
               
        return deps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        deps = self.get_dependencies()

        context['obj_type'] = self.model._meta.verbose_name
        context['deps'] = deps
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error = (f"<p> <strong>{self.object}</strong> cannot be deleted. </p>"
                         f"<p> Try delete the dependencies first, then delete <strong> {self.object}. </strong></p>")
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# Airline Views ##############################################

class AirlineTable(BaseItemsTable):
    model = Airline
    table = AirlineTable
    filter = AirlineFilter
    queryset = Airline.objects.all()    
    

class AirlineSearchResults(BaseItemsSearchResults):
    model = Airline
    table = AirlineTable
    filter = AirlineFilter
    queryset = Airline.objects.all()


class AirlineDetail(DetailView):
    template_name = 'trips/airline_detail.html'
    model = Airline
    airl_fl_table = AirlineFlightsTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object = self.get_object()
        
        fl_airl = Flight.objects.filter(airline=object)
        airl_fl_table = self.airl_fl_table(fl_airl, orderable=False)
        paginate = {'paginator_class': Paginator, 'per_page': 10}
        RequestConfig(self.request, paginate).configure(airl_fl_table)

        context["airl_fl_table"] = airl_fl_table
        context["airline"] = object

        return context


class AirlineCreate(BaseItemCreateWithPopup):
    model = Airline
    form_class = AirlineForm
    template_name = template_path + 'airline_form.html'
    template_name_popup = template_path + 'airline_form_popup.html'
    cancel_button_url = reverse_lazy('trips:airline_list')      


class AirlineEdit(BaseItemEdit):
    model = Airline
    form_class = AirlineForm
    template_name = template_path + 'airline_form.html'


class AirlineDelete(DeleteView):
    model = Airline
    success_url = reverse_lazy('trips:airline_list')
    template_name = confirm_delete_template

    def get_dependencies(self):

        deps = []

        flights_deps = []
        for flight in self.object.flights.all():
            flights_deps.append(flight)
        if flights_deps:
            deps.append({'Flights': flights_deps})

        trip_classes_deps = []
        for trip_class in self.object.trip_classes.all():
            trip_classes_deps.append(trip_class)
        if trip_classes_deps:
            deps.append({'Trip Classes': trip_classes_deps})
        
        return deps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        deps = self.get_dependencies()

        context['obj_type'] = self.model._meta.verbose_name
        context['deps'] = deps
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error = (f"<p> <strong>{self.object}</strong> cannot be deleted. </p>"
                         f"<p> Try delete the dependencies first, then delete <strong> {self.object}. </strong></p>")
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)

 
# Airplane Views #########################################################

class AirplaneList(BaseItemsList):
    model = Airplane
    paginate_by = 18


class AirplaneSearchResults(BaseItemsSearchResults):
    model = Airplane
    table = AirplaneTable
    filter = AirplaneFilter
    queryset = Airplane.objects.all()


class AirplaneDetail(View):
    template_name = template_path + 'airplane_detail.html'
    table_plane_flights = AirplaneFlightsTable
    
    def get(self, request, pk):
        airplane = get_object_or_404(Airplane.objects.all(), pk=pk)
        airplane_flight = Flight.objects.filter(airplane=airplane)
        table_plane_flights = self.table_plane_flights(airplane_flight)
        
        return render(request, self.template_name, {
            'object': airplane,
            'airplane_flight': airplane_flight,
            'table_plane_flights': table_plane_flights,
        })
    

class AirplaneCreate(BaseItemCreateWithPopup):
    model = Airplane
    form_class = AirplaneForm
    template_name = template_path + 'airplane_form.html'
    template_name_popup = template_path + 'airplane_form_popup.html'
    cancel_button_url = reverse_lazy('trips:airportterminal_list')


class AirplaneEdit(BaseItemEdit):
    model = Airplane
    form_class = AirplaneForm
    template_name = template_path + 'airplane_form.html'


class AirplaneDelete(DeleteView):
    model = Airplane
    success_url = reverse_lazy('trips:airplane_list')
    template_name = confirm_delete_template

    def get_dependencies(self):

        deps = []

        flights_deps = []
        for flight in self.object.flights.all():
            flights_deps.append(flight)        
        if flights_deps:
            deps.append({'Flights': flights_deps})

        return deps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        deps = self.get_dependencies()

        context['obj_type'] = self.model._meta.verbose_name
        context['deps'] = deps
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error = (f"<p> <strong>{self.object}</strong> cannot be deleted. </p>"
                         f"<p> Try delete the dependencies first, then delete <strong> {self.object}. </strong></p>")
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# Airport Views #########################################################

class AirportTable(BaseItemsTable):
    model = Airport
    table = AirportTable
    filter = AirportFilter
    queryset = Airport.objects.all()    
    

class AirportSearchResults(BaseItemsSearchResults):
    model = Airport
    table = AirportTable
    filter = AirportFilter
    queryset = Airport.objects.all().prefetch_related('city',)


class AirportDetail(View):
    template_name = template_path + 'airport_detail.html'
    table = AirportTable
    table_depart_from_airport = AirportDepartTable
    table_arrive_to_airport = AirportArriveTable

    def get(self, request, pk):
        
        airport = get_object_or_404(Airport.objects.all(), pk=pk)
        depart_from_airport = Flight.objects.filter(depart_airport=airport).order_by('depart_time',)
        arrive_to_airport = Flight.objects.filter(arrive_airport=airport).order_by('arrive_time',)
        
        table_depart_from_airport = self.table_depart_from_airport(
            depart_from_airport,
            orderable = False)
        table_arrive_to_airport = self.table_arrive_to_airport(
            arrive_to_airport,
            orderable = False)
        paginate = {'paginator_class': Paginator, 'per_page': 20}
        RequestConfig(request, paginate).configure(table_depart_from_airport)
        RequestConfig(request, paginate).configure(table_arrive_to_airport)

        return render(request, self.template_name, {
            'object': airport,
            'depart_from_airport': depart_from_airport,
            'table_depart_from_airport': table_depart_from_airport,
            'table_arrive_to_airport': table_arrive_to_airport,
        })
    

class AirportCreate(BaseItemCreateWithPopup):
    model = Airport
    form_class = AirportForm
    template_name = template_path + 'airport_form.html'
    template_name_popup = template_path + 'airport_form_popup.html'
    cancel_button_url = reverse_lazy('trips:airport_list')      


class AirportEdit(BaseItemEdit):
    model = Airport
    form_class = AirportForm
    template_name = template_path + 'airport_form.html'


class AirportDelete(DeleteView):
    model = Airport
    success_url = reverse_lazy('trips:airport_list')
    template_name = confirm_delete_template

    def get_dependencies(self):

        deps = []

        terminals_deps = []
        for terminal in self.object.terminals.all():
            terminals_deps.append(terminal)
        if terminals_deps:
            deps.append({'Airport Terminals': terminals_deps})

        return deps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name

        deps = self.get_dependencies()
        context['deps'] = deps        
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error = (f"<p> <strong>{self.object}</strong> cannot be deleted. </p>"
                         f"<p> Try delete the dependencies first, then delete <strong> {self.object}. </strong></p>")
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# AirportTerminal Views #########################################################

class AirportTerminalTable(BaseItemsTable):
    model = AirportTerminal
    table = AirportTerminalTable
    filter = AirportTerminalFilter
    queryset = AirportTerminal.objects.all()    


class AirportTerminalSearchResults(BaseItemsSearchResults):
    model = AirportTerminal
    table = AirportTerminalTable
    filter = AirportTerminalFilter
    queryset = AirportTerminal.objects.all().prefetch_related('airport',)


class AirportTerminalDetail(DetailView):
    model = AirportTerminal
    table_terms_arrs = AirportTerminalFlightsArriveTable
    table_terms_deps = AirportTerminalFlightsDepartTable
    template_name = template_path + 'airportterminal_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.object = self.get_object()

        out_first_flights_dep_term = self.object.out_first_flights_dep_term.all()
        out_first_flights_arr_term = self.object.out_first_flights_arr_term.all()
        ret_first_flights_dep_term = self.object.ret_first_flights_dep_term.all()
        ret_first_flights_arr_term = self.object.ret_first_flights_arr_term.all()

        terminal_arrivals = out_first_flights_arr_term | ret_first_flights_arr_term
        terminal_departures = out_first_flights_dep_term | ret_first_flights_dep_term
       
        terminal_arrivals_table = self.table_terms_arrs(terminal_arrivals)
        terminal_departures_table = self.table_terms_deps(terminal_departures)

        context['terminal_arrivals_table'] = terminal_arrivals_table    
        context['terminal_departures_table'] = terminal_departures_table
        
        return context


class AirportTerminalCreate(BaseItemCreateWithPopup):
    model = AirportTerminal
    form_class = AirportTerminalForm
    template_name = template_path + 'airportterminal_form.html'
    template_name_popup = template_path + 'airportterminal_form_popup.html'
    cancel_button_url = reverse_lazy('trips:airportterminal_list') 


class AirportTerminalEdit(BaseItemEdit):
    model = AirportTerminal
    form_class = AirportTerminalForm
    template_name = template_path + 'airportterminal_form.html'  


class AirportTerminalDelete(DeleteView):
    model = AirportTerminal
    success_url = reverse_lazy('trips:airportterminal_list')
    template_name = confirm_delete_template

    def get_dependencies(self):

        deps = []

        out_first_flights_dep_term_deps = []
        for flight in self.object.out_first_flights_dep_term.all():
            out_first_flights_dep_term_deps.append(flight)
        if out_first_flights_dep_term_deps:
            deps.append({'Outgoing First Flights Departure Terminal': out_first_flights_dep_term_deps})

        out_first_flights_arr_term_deps = []
        for flight in self.object.out_first_flights_arr_term.all():
            out_first_flights_arr_term_deps.append(flight)
        if out_first_flights_arr_term_deps:
            deps.append({'Outgoing First Flights Arrival Terminal': out_first_flights_arr_term_deps})

        out_second_flights_dep_term_deps = []
        for flight in self.object.out_second_flights_dep_term.all():
            out_second_flights_dep_term_deps.append(flight)
        if out_second_flights_dep_term_deps:
            deps.append({'Outgoing Second Flights Departure Terminal': out_second_flights_dep_term_deps})

        out_second_flights_arr_term_deps = []
        for flight in self.object.out_second_flights_arr_term.all():
            out_second_flights_arr_term_deps.append(flight)
        if out_second_flights_arr_term_deps:
            deps.append({'Outgoing Second Flights Arrival Terminal': out_second_flights_arr_term_deps})

        ret_first_flights_dep_term_deps = []
        for flight in self.object.ret_first_flights_dep_term.all():
            ret_first_flights_dep_term_deps.append(flight)
        if ret_first_flights_dep_term_deps:
            deps.append({'Returning First Flights Departure Terminal': ret_first_flights_dep_term_deps})

        ret_first_flights_arr_term_deps = []
        for flight in self.object.ret_first_flights_arr_term.all():
            ret_first_flights_arr_term_deps.append(flight)
        if ret_first_flights_arr_term_deps:
            deps.append({'Returning First Flights Arrival Terminal': ret_first_flights_arr_term_deps})

        ret_second_flights_dep_term_deps = []
        for flight in self.object.ret_second_flights_dep_term.all():
            ret_second_flights_dep_term_deps.append(flight)
        if ret_second_flights_dep_term_deps:
            deps.append({'Returning Second Flights Departure Terminal': ret_second_flights_dep_term_deps})

        ret_second_flights_arr_term_deps = []
        for flight in self.object.ret_second_flights_arr_term.all():
            ret_second_flights_arr_term_deps.append(flight)
        if ret_second_flights_arr_term_deps:
            deps.append({'Returning Second Flights Arrival Terminal': ret_second_flights_arr_term_deps})

        return deps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name

        deps = self.get_dependencies()
        context['deps'] = deps        
        
        return context


# Flight Views #########################################################

class FlightTable(BaseItemsTable):
    model = Flight
    table = FlightTable
    filter = FlightFilter
    queryset = Flight.objects.all().prefetch_related(
        'airline', 'airplane', 'depart_airport', 'arrive_airport', ) 
    template_name = template_path + 'flight_list.html'  


class FlightSearchResults(BaseItemsSearchResults):
    model = Flight
    table = FlightTable
    filter = FlightFilter
    queryset = Flight.objects.all().prefetch_related(
        'airline', 'airplane', 'depart_airport', 'arrive_airport', )


class FlightDetail(View):
    template_name = template_path + 'flight_detail.html'

    def get(self, request, pk):
        flight = get_object_or_404(Flight.objects.all(), pk=pk)

        out_first_flights = flight.out_first_flights.all()
        out_second_flights = flight.out_second_flights.all()
        ret_first_flights = flight.ret_first_flights.all()
        ret_second_flights = flight.ret_second_flights.all()

        out_first_flights_table = FlightTripsTable(out_first_flights)
        out_second_flights_table = FlightTripsTable(out_second_flights)
        ret_first_flights_table = FlightTripsTable(ret_first_flights)
        ret_second_flights_table = FlightTripsTable(ret_second_flights)


        return render(request, self.template_name, {
            'object': flight,
            'out_first_flights': out_first_flights,
            'out_second_flights': out_second_flights,
            'ret_first_flights': ret_first_flights,
            'ret_second_flights': ret_second_flights,
            'out_first_flights_table': out_first_flights_table,
            'out_second_flights_table': out_second_flights_table,
            'ret_first_flights_table': ret_first_flights_table,
            'ret_second_flights_table': ret_second_flights_table,
        })


class FlightCreate(BaseItemCreateWithPopup):
    model = Flight
    form_class = FlightForm
    template_name = template_path + 'flight_form.html'
    template_name_popup = template_path + 'flight_form_popup.html'
    cancel_button_url = reverse_lazy('trips:flight_list')     


class FlightEdit(BaseItemEdit):
    model = Flight
    form_class = FlightForm
    template_name = template_path + 'flight_form.html'


class FlightDelete(DeleteView):
    model = Flight
    success_url = reverse_lazy('trips:flight_list')
    template_name = confirm_delete_template

    def get_dependencies(self):

        deps = []

        out_first_flights_deps = []
        for flight in self.object.out_first_flights.all():
            out_first_flights_deps.append(flight)        
        if out_first_flights_deps:
            deps.append({'Outgoing First Flights': out_first_flights_deps})

        out_second_flights_deps = []
        for flight in self.object.out_second_flights.all():
            out_second_flights_deps.append(flight)        
        if out_second_flights_deps:
            deps.append({'Outgoing Second Flights': out_second_flights_deps})

        ret_first_flights_deps = []
        for flight in self.object.ret_first_flights.all():
            ret_first_flights_deps.append(flight)        
        if ret_first_flights_deps:
            deps.append({'Returning First Flights': ret_first_flights_deps})

        ret_second_flights_deps = []
        for flight in self.object.ret_second_flights.all():
            ret_second_flights_deps.append(flight)        
        if ret_second_flights_deps:
            deps.append({'Returning Second Flights': ret_second_flights_deps})

        seats_deps = []
        for seat in self.object.seats.all():
            seats_deps.append(seat)        
        if seats_deps:
            deps.append({'Seats': seats_deps})

        return deps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        deps = self.get_dependencies()

        context['obj_type'] = self.model._meta.verbose_name
        context['deps'] = deps
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error = (f"<p> <strong>{self.object}</strong> cannot be deleted. </p>"
                         f"<p> Try delete the dependencies first, then delete <strong> {self.object}. </strong></p>")
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# TripSource Views ##############################################

class TripSourceList(BaseItemsList):
    model = TripSource
    paginate_by = 18        


class TripSourceSearchResults(BaseItemsSearchResults):
    model = TripSource
    table = TripSourceTable
    filter = TripSourceFilter
    queryset = TripSource.objects.all()


class TripSourceDetail(DetailView):
    template_name = template_path + 'tripsource_detail.html'
    model = TripSource

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        trips = self.object.trips.all().prefetch_related(
            'orig', 'dest', 'source_found', 
              'out_class', 
            'out_first_flight', 'out_first_flight_dep_term', 'out_first_flight_arr_term',
            'out_second_flight', 'out_second_flight_dep_term', 'out_second_flight_arr_term',
             'ret_class', 
            'ret_first_flight', 'ret_first_flight_dep_term', 'ret_first_flight_arr_term',
            'ret_second_flight', 'ret_second_flight_dep_term', 'ret_second_flight_arr_term',
        )
        
        table_trips = TripTable(trips)

        context['trips'] = trips
        context['table_trips'] = table_trips

        return context


class TripSourceCreate(BaseItemCreateWithPopup):
    model = TripSource
    form_class = TripSourceForm
    template_name = template_path + 'tripsource_form.html'
    template_name_popup = template_path + 'tripsource_form_popup.html'
    cancel_button_url = reverse_lazy('trips:tripsource_list')     


class TripSourceEdit(BaseItemEdit):
    model = TripSource
    form_class = TripSourceForm
    template_name = template_path + 'tripsource_form.html' 


class TripSourceDelete(DeleteView):
    model = TripSource
    success_url = reverse_lazy('trips:tripsource_list')
    template_name = confirm_delete_template

    def get_dependencies(self):

        deps = []

        trips_deps = []
        for trip in self.object.trips.all():
            trips_deps.append(trip)
        if trips_deps:
            deps.append({'Trips': trips_deps})

        return deps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name

        deps = self.get_dependencies()
        context['deps'] = deps        
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error = (f"<p> <strong>{self.object}</strong> cannot be deleted. </p>"
                         f"<p> Try delete the dependencies first, then delete <strong> {self.object}. </strong></p>")
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# TripClass Views ##############################################

class TripClassList(BaseItemsList):
    model = TripClass
    paginate_by = 18


class TripClassSearchResults(BaseItemsSearchResults):
    model = TripClass
    table = TripClassTable
    filter = TripClassFilter
    queryset = TripClass.objects.all()


class TripClassDetail(DetailView):
    template_name = template_path + 'tripclass_detail.html'
    model = TripClass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        out_trips = self.object.out_trips.all()
        ret_trips = self.object.ret_trips.all()

        table_out_trips = TripTable(out_trips)
        table_ret_trips = TripTable(ret_trips)

        context['out_trips'] = out_trips
        context['ret_trips'] = ret_trips
        context['table_out_trips'] = table_out_trips
        context['table_ret_trips'] = table_ret_trips

        return context


class TripClassCreate(BaseItemCreateWithPopup):  
    model = TripClass
    form_class = TripClassForm
    template_name = template_path + 'tripclass_form.html'
    template_name_popup = template_path + 'tripclass_form_popup.html'
    cancel_button_url = reverse_lazy('trips:tripclass_list')


class TripClassEdit(BaseItemEdit):
    model = TripClass
    form_class = TripClassForm
    template_name = template_path + 'tripclass_form.html'


class TripClassDelete(DeleteView):
    model = TripClass
    success_url = reverse_lazy('trips:tripclass_list')
    template_name = confirm_delete_template

    def get_dependencies(self):

        deps = []

        out_trips_deps = []
        for trip in self.object.out_trips.all():
            out_trips_deps.append(trip)        
        if out_trips_deps:
            deps.append({'Outgoing Trips': out_trips_deps})

        ret_trips_deps = []
        for trip in self.object.ret_trips.all():
            ret_trips_deps.append(trip)        
        if ret_trips_deps:
            deps.append({'Returning Trips': ret_trips_deps})

        return deps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        deps = self.get_dependencies()

        context['obj_type'] = self.model._meta.verbose_name
        context['deps'] = deps
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error = (f"<p> <strong>{self.object}</strong> cannot be deleted. </p>"
                         f"<p> Try delete the dependencies first, then delete <strong> {self.object}. </strong></p>")
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# Trip Views ##############################################

class TripList(View):
    model = Trip
    table = TripTable
    filter = TripFilter
    template_name = template_path + 'trip_list.html'

    def is_valid_queryparam(self, param):
        return param != '' and param is not None
    
    def get(self, request):
        queryset = Trip.objects.all()
        queryset = Trip.objects.all().prefetch_related(
            'orig', 'dest', 'source_found', 
              'out_class', 
            'out_first_flight', 'out_first_flight_dep_term', 'out_first_flight_arr_term',
            'out_second_flight', 'out_second_flight_dep_term', 'out_second_flight_arr_term',
             'ret_class', 
            'ret_first_flight', 'ret_first_flight_dep_term', 'ret_first_flight_arr_term',
            'ret_second_flight', 'ret_second_flight_dep_term', 'ret_second_flight_arr_term',
        )
        
        trip_name_contains_query = request.GET.get('trip_name_contains')

        trip_date_min = request.GET.get('trip_date_min')
        trip_date_max = request.GET.get('trip_date_max')

        out_stop_dur_min_hours = request.GET.get('out_stop_dur_min_hours')
        out_stop_dur_min_mins = request.GET.get('out_stop_dur_min_mins')
        out_stop_dur_max_hours = request.GET.get('out_stop_dur_max_hours')
        out_stop_dur_max_mins = request.GET.get('out_stop_dur_max_mins') 

        ret_stop_dur_min_hours = request.GET.get('ret_stop_dur_min_hours')
        ret_stop_dur_min_mins = request.GET.get('ret_stop_dur_min_mins')
        ret_stop_dur_max_hours = request.GET.get('ret_stop_dur_max_hours')
        ret_stop_dur_max_mins = request.GET.get('ret_stop_dur_max_mins')    

        cities = City.objects.all()
        out_first_stop_city = request.GET.get('out_first_stop_city')
        ret_first_stop_city = request.GET.get('ret_first_stop_city')

        trip_orig = request.GET.get('trip_orig')
        trip_dest = request.GET.get('trip_dest')   

        if self.is_valid_queryparam(trip_name_contains_query):
            queryset = queryset.filter(name__icontains=trip_name_contains_query)   

        if self.is_valid_queryparam(trip_date_min):
            queryset = queryset.filter(out_dep_date__gte=trip_date_min)
                 
        if self.is_valid_queryparam(trip_date_max):
            queryset = queryset.filter(out_dep_date__lt=trip_date_max)
                      
        if self.is_valid_queryparam(out_stop_dur_min_hours) and self.is_valid_queryparam(out_stop_dur_min_mins):
            out_stop_dur_min = int(out_stop_dur_min_hours) * 60 + int(out_stop_dur_min_mins)
            queryset = queryset.filter(out_stop_duration__gte=out_stop_dur_min)
            
        if self.is_valid_queryparam(out_stop_dur_max_hours) and self.is_valid_queryparam(out_stop_dur_max_mins):
            out_stop_dur_max = int(out_stop_dur_max_hours) * 60 + int(out_stop_dur_max_mins)
            queryset = queryset.filter(out_stop_duration__lt=out_stop_dur_max)
            
        if self.is_valid_queryparam(ret_stop_dur_min_hours) and self.is_valid_queryparam(ret_stop_dur_min_mins):
            ret_stop_dur_min = int(ret_stop_dur_min_hours) * 60 + int(ret_stop_dur_min_mins)
            queryset = queryset.filter(ret_stop_duration__gte=ret_stop_dur_min)
            
        if self.is_valid_queryparam(ret_stop_dur_max_hours) and self.is_valid_queryparam(ret_stop_dur_max_mins):
            ret_stop_dur_max = int(ret_stop_dur_max_hours) * 60 + int(ret_stop_dur_max_mins)
            queryset = queryset.filter(ret_stop_duration__lt=ret_stop_dur_max)
            
        # Stops Cities
        if out_first_stop_city:
            queryset = queryset.filter(
                out_first_flight__arrive_airport__city__name=out_first_stop_city)
            
        if ret_first_stop_city:
            queryset = queryset.filter(
                ret_first_flight__arrive_airport__city__name=ret_first_stop_city)

        # Orig and Dest
        if trip_orig:
            queryset = queryset.filter(orig__name=trip_orig)

        if trip_dest:
            queryset = queryset.filter(dest__name=trip_dest)
                     
        trip_table = self.table(queryset)
        paginate = {'paginator_class': Paginator, 'per_page': 10}
        RequestConfig(request, paginate).configure(trip_table)
        
        app_name = self.model._meta.app_label
        obj_name = self.model._meta.verbose_name.lower().replace(" ", "")

        return render(request, self.template_name, {
            'trip_table': trip_table,
            'queryset': queryset,
            'cities': cities,
            'model': self.model,
            'app_name': app_name,
            'obj_name': obj_name,
        })


class TripSearchResults(BaseItemsSearchResults):
    model = Trip
    table = TripTable
    filter = TripFilter
    queryset = Trip.objects.all()
    queryset = Trip.objects.all().prefetch_related(
            'orig', 'dest', 'source_found', 
              'out_class', 
            'out_first_flight', 'out_first_flight_dep_term', 'out_first_flight_arr_term',
            'out_second_flight', 'out_second_flight_dep_term', 'out_second_flight_arr_term',
             'ret_class', 
            'ret_first_flight', 'ret_first_flight_dep_term', 'ret_first_flight_arr_term',
            'ret_second_flight', 'ret_second_flight_dep_term', 'ret_second_flight_arr_term',
        )


class TripDetail(DetailView):
    model = Trip
    template_name = template_path + 'trip_detail.html'


class TripCreate(CreateView):
    model = Trip
    form_class = TripForm
    template_name = template_path + 'trip_form.html'
    cancel_button_url = reverse_lazy('trips:trip_list') 
    

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial_data = {k: self.request.GET[k] for k in self.request.GET}
        initial = initial_data
      
        return initial

    def get_context_data(self, **kwargs):      
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name
        context['cancel_button_url'] = self.cancel_button_url
        return context
        

class TripEdit(BaseItemEdit):
    model = Trip
    form_class = TripForm
    template_name = template_path + 'trip_form.html'

    def get_queryset(self):
        self.queryset = Trip.objects.all().prefetch_related(
            'orig', 'dest', 'source_found', 
              'out_class', 
            'out_first_flight', 'out_first_flight_dep_term', 'out_first_flight_arr_term',
            'out_second_flight', 'out_second_flight_dep_term', 'out_second_flight_arr_term',
             'ret_class', 
            'ret_first_flight', 'ret_first_flight_dep_term', 'ret_first_flight_arr_term',
            'ret_second_flight', 'ret_second_flight_dep_term', 'ret_second_flight_arr_term',
        )

        return self.queryset


class TripDelete(DeleteView):
    model = Trip
    success_url = reverse_lazy('trips:trip_list')
    template_name = confirm_delete_template

    def get_dependencies(self):

        deps = []

        seats_deps = []
        for seat in self.object.seats.all():
            seats_deps.append(seat)
        if seats_deps:
            deps.append({'Seats': seats_deps})

        return deps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name

        deps = self.get_dependencies()
        context['deps'] = deps        
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error = (f"<p> <strong>{self.object}</strong> cannot be deleted. </p>"
                         f"<p> Try delete the dependencies first, then delete <strong> {self.object}. </strong></p>")
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# Traveller Views #########################################################

class TravellerList(BaseItemsList):
    model = Traveller
    paginate_by = 18


class TravellerSearchResults(BaseItemsSearchResults):
    model = Traveller
    table = TravellerTable
    filter = TravellerFilter
    queryset = Traveller.objects.all()


class TravellerDetail(DetailView):
    model = Traveller
    trav_trips_table = TravellerSeatsTable
    template_name = template_path + 'traveller_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.object = self.get_object()

        seats = self.object.seats.all()
        seats_table = self.trav_trips_table(seats)
        
        context['seats_table'] = seats_table
        context['seats'] = seats
        
        return context


class TravellerCreate(BaseItemCreateWithPopup):
    model = Traveller
    form_class = TravellerForm
    template_name = template_path + 'traveller_form.html'
    template_name_popup = template_path + 'traveller_form_popup.html'
    cancel_button_url = reverse_lazy('trips:traveller_list')         


class TravellerEdit(BaseItemEdit):
    model = Traveller
    form_class = TravellerForm
    template_name = template_path + 'traveller_form.html'


class TravellerDelete(DeleteView):
    model = Traveller
    success_url = reverse_lazy('trips:traveller_list')
    template_name = confirm_delete_template

    def get_dependencies(self):

        deps = []

        seats_deps = []
        for seat in self.object.seats.all():
            seats_deps.append(seat)
        if seats_deps:
            deps.append({'Seats': seats_deps})

        return deps

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name

        deps = self.get_dependencies()
        context['deps'] = deps        
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error = (f"<p> <strong>{self.object}</strong> cannot be deleted. </p>"
                         f"<p> Try delete the dependencies first, then delete <strong> {self.object}. </strong></p>")
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# Seat Views #########################################################

class SeatTable(BaseItemsTable):
    model = Seat
    table = SeatTable
    filter = SeatFilter
    queryset = Seat.objects.all().prefetch_related('traveller', 'trip', 'flight')    


class SeatSearchResults(BaseItemsSearchResults):
    model = Seat
    table = SeatTable
    filter = SeatFilter
    queryset = Seat.objects.all()


class SeatDetail(DetailView):
    model = Seat
    template_name = template_path + 'seat_detail.html'


class SeatCreate(CreateView):
    model = Seat
    form_class = SeatForm
    template_name = template_path + 'seat_form.html'
    cancel_button_url = reverse_lazy('trips:seat_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name
        context['cancel_button_url'] = self.cancel_button_url

        return context


class SeatEdit(BaseItemEdit):
    model = Seat
    form_class = SeatForm
    template_name = template_path + 'seat_form.html'


class SeatDelete(DeleteView):
    model = Seat
    success_url = reverse_lazy('trips:seat_list')
    template_name = confirm_delete_template

