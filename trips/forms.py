from django import forms 

from tempus_dominus.widgets import DatePicker, TimePicker

from .models import (
    City, Airline, Airplane, Airport, AirportTerminal, Flight, 
    TripSource, TripClass, Trip, Seat, Traveller )

from base.widgets import RelatedFieldWidgetSingle, MultiValueDurationField




### City Form ############################################

class CityForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )
    country = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )
    prov_st = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    class Meta:
        model = City
        fields = ['name', 'prov_st', 'country', 'notes', ]


### Airline Form #########################################

class AirlineForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )
    country = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    class Meta:
        model = Airline
        fields = ['name', 'country', 'notes', ]
        

### Airplane Form ###########################################

class AirplaneForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    class Meta:
        model = Airplane
        fields = ['name', 'notes', ]


### Airport Form #########################################

class AirportForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )
    code = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    city = forms.ModelChoiceField(
        required=True, 
        queryset=City.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            City, 
            related_url="trips:city_add", 
            attrs={'class': 'select2-trips form-control',
                'style': 'width:90%'},  
            )
        )

    class Meta:
        model = Airport
        fields = ['name', 'code', 'city', 'notes', ]


### Airport Terminal Form ##################################

class AirportTerminalForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    airport = forms.ModelChoiceField(
        required=True, 
        queryset=Airport.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Airport, 
            related_url="trips:airport_add", 
            attrs={'class': 'select2-trips form-control',
                'style': 'width:90%'},  
            )
        )


    class Meta:
        model = AirportTerminal
        fields = ['name', 'airport', 'notes', ]


# Flight Form ################################################

class FlightForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    airline = forms.ModelChoiceField(
        required=True, 
        queryset=Airline.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Airline, 
            related_url="trips:airline_add", 
            attrs={'class': 'select2-trips form-control',
                'style': 'width:90%'},  
            )
        )

    airplane = forms.ModelChoiceField(
        required=False, 
        queryset=Airplane.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Airplane, 
            related_url="trips:airplane_add", 
            attrs={'class': 'select2-trips form-control',
                'style': 'width:90%'},  
            )
        )

    depart_airport = forms.ModelChoiceField(
        required=True,  
        queryset=Airport.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Airport, 
            related_url="trips:airport_add", 
            attrs={'class': 'select2-trips form-control',
                'style': 'width:90%'},  
            )
        )

    arrive_airport = forms.ModelChoiceField(
        required=True,  
        queryset=Airport.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Airport, 
            related_url="trips:airport_add", 
            attrs={'class': 'select2-trips form-control',
                'style': 'width:90%'},  
            )
        )

    depart_time = forms.TimeField(
        required = False,
        widget=TimePicker(
            options={'format': 'HH:mm'},            
            )
        )

    arrive_time = forms.TimeField(
        required = False,
        widget=TimePicker(
            options={'format': 'HH:mm'},
            )
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['duration'] = MultiValueDurationField()

    class Meta:
        model = Flight
        fields = [
            'name', 
            'airline', 
            'airplane', 
            'duration', 
            'depart_airport', 
            'depart_time', 
            'arrive_airport', 
            'arrive_time', 
            'notes',
        ]
 

# Trip Source Form #########################################

class TripSourceForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    class Meta:
        model = TripSource
        fields = ['name', 'notes', ]


### Trip Class Form #####################################

class TripClassForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    airline = forms.ModelChoiceField(
        required=True, 
        queryset=Airline.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Airline, 
            related_url="trips:airline_add", 
            attrs={'class': 'select2-trips form-control',
                'style': 'width:90%'},  
            )
        )

    class Meta:
        model = TripClass
        fields = ['name', 'airline', 'notes', ]


### Trip Form #############################################

class TripForm(forms.ModelForm):

    TRIPDAY_MON = 'mon'
    TRIPDAY_TUE = 'tue'
    TRIPDAY_WED = 'wed'
    TRIPDAY_THU = 'thu'
    TRIPDAY_FRI = 'fri'
    TRIPDAY_SAT = 'sat'
    TRIPDAY_SUN = 'sun'

    TRIPDAY_CHOICES = (
        (TRIPDAY_MON, 'Monday'),
        (TRIPDAY_TUE, 'Tuesday'),
        (TRIPDAY_WED, 'Wednesday'),
        (TRIPDAY_THU, 'Thursday'),
        (TRIPDAY_FRI, 'Friday'),
        (TRIPDAY_SAT, 'Saturday'),
        (TRIPDAY_SUN, 'Sunday'),
    )

    # Currency Choices
    CAD = 'CAD'
    USD = 'USD'
    EUR = 'EUR'

    CURRENCY_CHOICES = (
        (CAD, 'CAD'),
        (USD, 'USD'),
        (EUR, 'EUR'),
    )

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    orig = forms.ModelChoiceField(
        required=True, 
        queryset=City.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            City, 
            related_url="trips:city_add", 
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'},  
        )
    )

    dest = forms.ModelChoiceField(
        required=True, 
        queryset=City.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            City, 
            related_url="trips:city_add", 
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'},  
        )
    )

    date_found = forms.DateField(
        widget=DatePicker())

    source_found = forms.ModelChoiceField(
        required=False, 
        queryset=TripSource.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            TripSource, 
            related_url="trips:tripsource_add", 
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'},  
        )
    )

    currency = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'select2-trips form-control', 'style': 'width:4rem'}),
        choices=CURRENCY_CHOICES
    )

    # Outgoing Trip
    out_dep_date = forms.DateField(
        required=True,
        widget=DatePicker())

    out_dep_day = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'select2-trips form-control'}),
        choices=TRIPDAY_CHOICES
    )

    out_arr_date = forms.DateField(
        required=True,
        widget=DatePicker())

    out_arr_day = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'select2-trips form-control'}),
        choices=TRIPDAY_CHOICES
    )

    out_class = forms.ModelChoiceField(
        required=False, 
        queryset=TripClass.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            TripClass, 
            related_url="trips:tripclass_add", 
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'}, 
            )
        )

    out_first_flight = forms.ModelChoiceField(
        required=True, 
        queryset = Flight.objects.all().prefetch_related(
                        'airline', 'airplane', 'depart_airport', 'arrive_airport', ),
        widget=RelatedFieldWidgetSingle(
            Flight, 
            related_url="trips:flight_add", 
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'},  
        )
    )

    out_first_flight_dep_term = forms.ModelChoiceField(
        required=False, 
        queryset = AirportTerminal.objects.all().prefetch_related(
                        'airport',),
        widget=RelatedFieldWidgetSingle(
            AirportTerminal, 
            related_url="trips:airportterminal_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'},  
        )
    )

    out_first_flight_arr_term = forms.ModelChoiceField(
        required=False, 
        queryset = AirportTerminal.objects.all().prefetch_related(
                        'airport',), 
        widget=RelatedFieldWidgetSingle(
            AirportTerminal, 
            related_url="trips:airportterminal_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'} 
            )
        )

    out_second_flight = forms.ModelChoiceField(
        required=False, 
        queryset = Flight.objects.all().prefetch_related(
                        'airline', 'airplane', 'depart_airport', 'arrive_airport', ), 
        widget=RelatedFieldWidgetSingle(
            Flight, 
            related_url="trips:flight_add", 
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'},  
        )
    )

    out_second_flight_dep_term = forms.ModelChoiceField(
        required=False, 
        queryset = AirportTerminal.objects.all().prefetch_related(
                        'airport',), 
        widget=RelatedFieldWidgetSingle(
            AirportTerminal, 
            related_url="trips:airportterminal_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'} 
            )
        )

    out_second_flight_arr_term = forms.ModelChoiceField(
        required=False, 
        queryset = AirportTerminal.objects.all().prefetch_related(
                        'airport',), 
        widget=RelatedFieldWidgetSingle(
            AirportTerminal, 
            related_url="trips:airportterminal_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'} 
            )
        )    

    # Returning Trip
    ret_dep_date = forms.DateField(
        required=False,
        widget=DatePicker())

    ret_dep_day = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'select2-trips form-control'}),
        choices=TRIPDAY_CHOICES
    )

    ret_arr_date = forms.DateField(
        required=False,
        widget=DatePicker())

    ret_arr_day = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'select2-trips form-control'}),
        choices=TRIPDAY_CHOICES
    )

    ret_class = forms.ModelChoiceField(
        required=False, 
        queryset=TripClass.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            TripClass, 
            related_url="trips:tripclass_add", 
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'}, 
            )
        )

    ret_first_flight = forms.ModelChoiceField(
        required=False, 
        queryset = Flight.objects.all().prefetch_related(
                        'airline', 'airplane', 'depart_airport', 'arrive_airport', ), 
        widget=RelatedFieldWidgetSingle(
            Flight, 
            related_url="trips:flight_add", 
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'},  
        )
    )

    ret_first_flight_dep_term = forms.ModelChoiceField(
        required=False, 
        queryset = AirportTerminal.objects.all().prefetch_related(
                        'airport',),
        widget=RelatedFieldWidgetSingle(
            AirportTerminal, 
            related_url="trips:airportterminal_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'},  
        )
    )

    ret_first_flight_arr_term = forms.ModelChoiceField(
        required=False, 
        queryset = AirportTerminal.objects.all().prefetch_related(
                        'airport',),
        widget=RelatedFieldWidgetSingle(
            AirportTerminal, 
            related_url="trips:airportterminal_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'} 
            )
        )

    ret_second_flight = forms.ModelChoiceField(
        required=False, 
        queryset = Flight.objects.all().prefetch_related(
                        'airline', 'airplane', 'depart_airport', 'arrive_airport', ), 
        widget=RelatedFieldWidgetSingle(
            Flight, 
            related_url="trips:flight_add", 
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'},  
        )
    )

    ret_second_flight_dep_term = forms.ModelChoiceField(
        required=False, 
        queryset = AirportTerminal.objects.all().prefetch_related(
                        'airport',), 
        widget=RelatedFieldWidgetSingle(
            AirportTerminal, 
            related_url="trips:airportterminal_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'} 
            )
        )

    ret_second_flight_arr_term = forms.ModelChoiceField(
        required=False, 
        queryset = AirportTerminal.objects.all().prefetch_related(
                        'airport',), 
        widget=RelatedFieldWidgetSingle(
            AirportTerminal, 
            related_url="trips:airportterminal_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'} 
            )
        )    


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['out_stop_duration'] = MultiValueDurationField(required=False)
        self.fields['out_duration'] = MultiValueDurationField(required=False)
        self.fields['ret_stop_duration'] = MultiValueDurationField(required=False)
        self.fields['ret_duration'] = MultiValueDurationField(required=False)
                
    class Meta:
        model = Trip
        fields = [
            'name',
            'orig',
            'dest',
            'trav',
            'price',
            'currency',
            'date_found',
            'source_found',
            'notes',
            # Outgoing
            'out_dep_date',
            'out_dep_day',
            'out_arr_date',
            'out_arr_day',
            'out_stop_duration',
            'out_duration',
            'out_price',
            'out_class',
            'out_first_flight',
            'out_first_flight_dep_term',
            'out_first_flight_arr_term',
            'out_second_flight',
            'out_second_flight_dep_term',
            'out_second_flight_arr_term',
            # Returning
            'ret_dep_date',
            'ret_dep_day',
            'ret_arr_date',
            'ret_arr_day',
            'ret_stop_duration',
            'ret_duration',
            'ret_price',
            'ret_class',
            'ret_first_flight',
            'ret_first_flight_dep_term',
            'ret_first_flight_arr_term',
            'ret_second_flight',
            'ret_second_flight_dep_term',
            'ret_second_flight_arr_term', 
        ]
        widgets = {
            'trav': forms.NumberInput(attrs={'class': 'select2-bankexp form-control', 'style': 'width:4rem' }),
            'price': forms.NumberInput(attrs={'class': 'select2-bankexp form-control', 'style': 'width:8rem' }),
            'out_price': forms.NumberInput(attrs={'class': 'select2-bankexp form-control', 'style': 'width:8rem' }),
            'ret_price': forms.NumberInput(attrs={'class': 'select2-bankexp form-control', 'style': 'width:8rem' }),
        }
        
### Traveller Form ##################################

class TravellerForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    class Meta:
        model = Traveller
        fields = ['name',  'notes',]


### Seat Form #####################################

class SeatForm(forms.ModelForm):

    seat_number = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            ),
        )

    traveller = forms.ModelChoiceField(
        required=True, 
        queryset=Traveller.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Traveller, 
            related_url="trips:traveller_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'} 
            )
        )

    trip = forms.ModelChoiceField(
        required=True, 
        queryset=Trip.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Trip, 
            related_url="trips:trip_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'} 
            )
        )

    flight = forms.ModelChoiceField(
        required=True, 
        queryset=Flight.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Flight, 
            related_url="trips:flight_add",  
            attrs={'class': 'select2-trips form-control',
            'style': 'width:90%'} 
            )
        )


    class Meta:
        model = Seat
        fields = [
            'seat_number', 
            'traveller', 
            'trip',
            'flight', 
            'notes',
            ]


