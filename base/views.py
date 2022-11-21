from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, UpdateView
from django.urls import reverse
from django.http import HttpResponse
from django.utils.html import escape, escapejs
from collections import OrderedDict
from django.urls import reverse
from django.core.paginator import Paginator
from django_tables2 import RequestConfig


from .forms import SearchForm

from trips.models import (
    City, Airline, Airplane, Airport, AirportTerminal, Flight, 
    TripSource, TripClass, Trip, Seat, Traveller )

from trips.tables import (
    CityTable, AirlineTable, AirplaneTable, AirportTable, AirportTerminalTable,
    FlightTable, TripTable, TripSourceTable, TripClassTable, SeatTable, TravellerTable)

from trips.filters import (
    CityFilter, AirlineFilter, AirplaneFilter, AirportFilter, AirportTerminalFilter,
    FlightFilter, TripClassFilter, TripSourceFilter, TripFilter, SeatFilter, TravellerFilter)

# Paths for common templates
template_path = 'base/'
search_results_template = template_path + "base_search_results.html"




# Base Views #################################################

class BaseItemsList(ListView):
    """
    Base class view used to display the items as list or as boxes
    Subclassing ListView to make use of pagination.
    As template, it can use the template which displays the items as boxes
    or a template which displays the items as a list of links.
    """
    model = None
    template_name = template_path + 'base_items_list_boxes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['obj_name'] = self.model._meta.verbose_name.lower().replace(" ", "")
        context['app_name'] = self.model._meta.app_label
        context['model'] = self.model

        return context


class BaseItemsTable(View):
    """ 
    A class view to display the items in a table using
    django-tables2
    """
    model = None
    table = None
    filter = None
    queryset = None    
    template_name = template_path + 'base_items_list_table.html' 
    paginate_per_page = 14
    
    def get(self, request):

        if self.filter:
            self.queryset = self.filter(request.GET, self.queryset).qs

        table = self.table(self.queryset)
        paginate = {'paginator_class': Paginator, 'per_page': self.paginate_per_page}
        RequestConfig(request, paginate).configure(table)
        
        app_name = self.model._meta.app_label
        obj_name = self.model._meta.verbose_name.lower().replace(" ", "")

        return render(request, self.template_name, {
            'table': table,
            'queryset': self.queryset,
            'model': self.model,
            'app_name': app_name,
            'obj_name': obj_name,
        })


class BaseItemsSearchResults(View):
    """
    This view is used to display a table with django-tables2 from a specific queryset
    Used to display the global search results in tables.
    """
    
    queryset = None
    table = None
    filter = None
    template_name = search_results_template
    paginate_per_page = 14 

    def get(self, request):
        
        if self.filter:
            self.queryset = self.filter(request.GET, self.queryset).qs

        table = self.table(self.queryset, orderable=False)
        paginate = {'paginator_class': Paginator, 'per_page': self.paginate_per_page}
        RequestConfig(request, paginate).configure(table)
                
        return render(request, self.template_name, {
            'table': table,
            'model': self.queryset.model,
        }) 


class BaseItemCreateWithPopup(CreateView):
    """
    Base class view used for item creation with popup window.
    This is for those items that are ForeigKey for a model and can be created from 
    a popup window in the specific model
    """
    model = None
    form_class = None
    template_name = None
    template_name_popup = None
    cancel_button_url = None 
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name
        context['cancel_button_url'] = self.cancel_button_url

        if ('_popup' in self.request.GET):
            self.template_name = self.template_name_popup
            context['popup'] = self.request.GET['_popup'] 
        return context
      
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if "_popup" in request.POST:
            if self.object: 
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                    (escape(self.object.pk), escapejs(self.object)))

        return response


class BaseItemEdit(UpdateView):
    model = None
    form_class = None

    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name
        return context


# SearchView #############################################################

SEARCH_MAX_RESULTS = 10

class SearchView(View):
    template_name = template_path + "search/search.html"

    def get(self, request):

        SEARCH_TYPES = OrderedDict((
            ('trip', {
                    'queryset': Trip.objects.all().prefetch_related(
                        'orig', 'dest', 'source_found', 
                        'out_class', 
                        'out_first_flight', 'out_first_flight_dep_term', 'out_first_flight_arr_term',
                        'out_second_flight', 'out_second_flight_dep_term', 'out_second_flight_arr_term',
                        'ret_class', 
                        'ret_first_flight', 'ret_first_flight_dep_term', 'ret_first_flight_arr_term',
                        'ret_second_flight', 'ret_second_flight_dep_term', 'ret_second_flight_arr_term',
                    ),
                    'filter': TripFilter,
                    'table': TripTable,
                    'url': 'trips:trip_search'
            }),
            ('flight', {
                    'queryset': Flight.objects.all().prefetch_related(
                        'airline', 'airplane', 'depart_airport', 'arrive_airport', ),
                    'filter': FlightFilter,
                    'table': FlightTable,
                    'url': 'trips:flight_search'
            }),
            ('city', {
                    'queryset': City.objects.all(),
                    'filter': CityFilter,
                    'table': CityTable,
                    'url': 'trips:city_search'
            }),
            ('airline', {
                    'queryset': Airline.objects.all(),
                    'filter': AirlineFilter,
                    'table': AirlineTable,
                    'url': 'trips:airline_search'
            }),
            ('airplane', {
                    'queryset': Airplane.objects.all(),
                    'filter': AirplaneFilter,
                    'table': AirplaneTable,
                    'url': 'trips:airplane_search'
            }),
            ('airport', {
                    'queryset': Airport.objects.all().prefetch_related('city',),
                    'filter': AirportFilter,
                    'table': AirportTable,
                    'url': 'trips:airport_search'
            }),
            ('airportterminal', {
                    'queryset': AirportTerminal.objects.all().prefetch_related('airport',),
                    'filter': AirportTerminalFilter,
                    'table': AirportTerminalTable,
                    'url': 'trips:airportterminal_search'
            }),            
            ('tripsource', {
                    'queryset': TripSource.objects.all(),
                    'filter': TripSourceFilter,
                    'table': TripSourceTable,
                    'url': 'trips:tripsource_search'
            }),
            ('tripclass', {
                    'queryset': TripClass.objects.all().prefetch_related('airline'),
                    'filter': TripClassFilter,
                    'table': TripClassTable,
                    'url': 'trips:tripclass_search'
            }),
            ('traveller', {
                    'queryset': Traveller.objects.all(),
                    'filter': TravellerFilter,
                    'table': TravellerTable,
                    'url': 'trips:traveller_search'
            }),
            ('seat', {
                    'queryset': Seat.objects.all().prefetch_related('traveller', 'trip', 'flight'),
                    'filter': SeatFilter,
                    'table': SeatTable,
                    'url': 'trips:seat_search'
            }),
        ))

        if 'q' not in request.GET:
            return render(request, self.template_name, { 'form': SearchForm(), })

        form = SearchForm(request.GET)
        results = []

        if form.is_valid():

            if form.cleaned_data['obj_type']:
                obj_types = [form.cleaned_data['obj_type']]

            else:
                obj_types = SEARCH_TYPES.keys()

            for obj_type in obj_types:
                
                queryset = SEARCH_TYPES[obj_type]['queryset']
                filter_cls = SEARCH_TYPES[obj_type]['filter']
                table = SEARCH_TYPES[obj_type]['table']
                url = SEARCH_TYPES[obj_type]['url']

                filtered_queryset = filter_cls({'q': form.cleaned_data['q']}, queryset=queryset).qs
                table = table(filtered_queryset, orderable=False)
                table.paginate(per_page=SEARCH_MAX_RESULTS)

                if table.page:
                    results.append({
                        'name': queryset.model._meta.verbose_name_plural,
                        'table': table,
                        'url': '{}?q={}'.format(reverse(url), form.cleaned_data['q']),
                    })

        return render(request, self.template_name, {
            'form': form,
            'results': results,
        })


