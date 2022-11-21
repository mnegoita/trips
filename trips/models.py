from ckeditor_uploader.fields import RichTextUploadingField

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe




class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=30)
    prov_st = models.CharField(max_length=30, blank=True, null=True, verbose_name="Province/State")
    notes = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/cities/{0}/".format(self.id)


class Airline(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=30)
    notes = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = 'Airline'
        verbose_name_plural = 'Airlines'
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/airlines/{0}/".format(self.id)


class Airplane(models.Model):
    name = models.CharField(max_length=100, unique=True)
    notes = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = 'Airplane'
        verbose_name_plural = 'Airplanes'
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/airplanes/{0}/".format(self.id)


class Airport(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=3, unique=True)
    city = models.ForeignKey(
        City, 
        related_name='airports', 
        on_delete=models.PROTECT)
    notes = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = 'Airport'
        verbose_name_plural = 'Airports'
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/airports/{0}/".format(self.id)


class AirportTerminal(models.Model):
    name = models.CharField(max_length=200)
    airport = models.ForeignKey(
        Airport, 
        related_name='terminals', 
        on_delete=models.PROTECT)
    notes = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = 'Airport terminal'
        verbose_name_plural = 'Airport Terminals'
        ordering = ["name"]

    def __str__(self):
        return "{0} - {1}".format(self.name, self.airport)

    def get_absolute_url(self):
        return "/airportterminals/{0}/".format(self.id)


class Flight(models.Model):

    name = models.CharField(
        max_length=40, 
        verbose_name = "Flight Name",
        help_text = "Add the Flight name")
    duration = models.PositiveSmallIntegerField(
        blank=True, 
        null=True, 
        default=0, 
        verbose_name="Duration")
    airline = models.ForeignKey(
        Airline, 
        related_name = 'flights', 
        on_delete=models.PROTECT,
        verbose_name = "Airline Name")
    airplane = models.ForeignKey(
        Airplane, 
        related_name = 'flights', 
        blank=True, 
        null=True, 
        on_delete=models.PROTECT,
        verbose_name = "Airplane Name")  
    depart_airport = models.ForeignKey(
        Airport, 
        related_name = 'flightsdepart',
        on_delete=models.PROTECT,
        verbose_name = "Departure Airport")       
    depart_time = models.TimeField(
        null=True, 
        blank=True, 
        default=None, 
        verbose_name="Departure Time")                                                                          
    arrive_airport = models.ForeignKey(
        Airport, 
        related_name = 'flightsarrive', 
        on_delete=models.PROTECT,
        verbose_name = "Arrival Airport")       
    arrive_time = models.TimeField(
        null=True, 
        blank=True, 
        default=None, 
        verbose_name="Arrival Time")    
    notes = RichTextUploadingField(blank=True, null=True)

    clone_fields = [
        'name',
        'airline',
        'airplane',
        'depart_airport',
        'depart_time',
        'arrive_airport',
        'arrive_time',
    ]

    class Meta:
        verbose_name_plural = 'Flights'
        ordering = ["name"]

    def __str__(self):
        return "{0} ({1} - {2}) {3}".format(
            self.name, 
            self.depart_airport.code, 
            self.arrive_airport.code,
            self.depart_time
            )

    def get_absolute_url(self):
        return "/flights/{0}/".format(self.id)

    def clean(self):
        if self.depart_airport == self.arrive_airport:
            raise ValidationError("The departing and arriving airport for a flight are usually different.")


class TripSource(models.Model):
    """ 
    Model class to represent the source where the trip
    and notes about the trip was found
    """

    name = models.CharField(max_length=100, unique=True)
    notes = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = 'Trip Source'
        verbose_name_plural = 'Trip Sources'
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/tripsources/{0}/".format(self.id)


class TripClass(models.Model):

    name = models.CharField(max_length=100)
    airline = models.ForeignKey(
        Airline, 
        related_name = 'trip_classes', 
        on_delete=models.PROTECT,
        verbose_name = "Airline")
    notes = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = 'Trip Class'
        verbose_name_plural = 'Trip Classes'
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.airline})"

    def get_absolute_url(self):
        return "/tripclass/{0}/".format(self.id)


class Trip(models.Model):

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

    # Trip detail
    name = models.CharField(max_length=255)
    orig = models.ForeignKey(
        City, 
        related_name='trips_orig', 
        on_delete=models.PROTECT, 
        verbose_name="Trip From")
    dest = models.ForeignKey(
        City, 
        related_name='trips_dest', 
        on_delete=models.PROTECT, 
        verbose_name="Trip To")
    trav = models.PositiveSmallIntegerField(
        default=1, 
        verbose_name="Travellers")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null = True,
        blank = True,
        validators=[MinValueValidator(0.01)],
        verbose_name = "Price")
    currency = models.CharField(
        max_length=5, 
        choices = CURRENCY_CHOICES, 
        default="", 
        null = True,
        blank = True,
        verbose_name = "Currency")
    date_found = models.DateField( 
        null = True,
        blank = True,
        verbose_name="Date Found")
    source_found = models.ForeignKey(
        TripSource, 
        related_name='trips', 
        on_delete=models.PROTECT, 
        verbose_name="Trip Source")
    notes = RichTextUploadingField(
        blank=True, 
        null=True)

    # Outgoing Trip
    # Details
    out_dep_date = models.DateField(
        verbose_name="Departure Date",
        help_text = "Outgoing Trip Departure Date") 
    out_dep_day = models.CharField(
        max_length = 10,
        blank = True,
        null = True,
        choices = TRIPDAY_CHOICES,
        default = "",
        verbose_name = "Departure Day",
        help_text = "Outgoing Trip Departure Day")
    out_arr_date = models.DateField(verbose_name="Arrival Date")
    out_arr_day = models.CharField(
        max_length = 10,
        blank = True,
        null = True,
        choices = TRIPDAY_CHOICES,
        default = "",
        verbose_name = "Arrival Day",
        help_text = "Outgoing Trip Arrival Day")
    out_stop_duration = models.PositiveSmallIntegerField(
        blank=True, 
        null=True, 
        default=0, 
        verbose_name="Stop Duration",
        help_text = "Outgoing Trip Stop Duration")
    out_duration = models.PositiveSmallIntegerField(
        blank=True, 
        null=True, 
        default=0, 
        verbose_name="Duration",
        help_text = "Outgoing Trip Duration")
    out_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null = True,
        blank = True,
        validators=[MinValueValidator(0.01)],
        verbose_name = "Price")
    out_class = models.ForeignKey(
        TripClass, 
        default = "",
        null = True,
        blank = True,
        related_name='out_trips', 
        on_delete=models.SET_NULL, 
        verbose_name="Class",
        help_text = "Outgoing Trip Flight Class")
    # Flights and Terminals
    out_first_flight = models.ForeignKey(
        Flight, 
        related_name = 'out_first_flights', 
        on_delete=models.PROTECT, 
        verbose_name="First Flight",
        help_text = "Outgoing Trip First Flight Name")
    out_first_flight_dep_term = models.ForeignKey(
        AirportTerminal, 
        related_name = 'out_first_flights_dep_term', 
        blank = True, 
        null = True,
        on_delete=models.SET_NULL,
        verbose_name = "Departure Terminal",
        help_text = "Outgoing Trip First Flight Departure Terminal")
    out_first_flight_arr_term = models.ForeignKey(
        AirportTerminal, 
        related_name = 'out_first_flights_arr_term', 
        blank = True, 
        null = True,
        on_delete=models.SET_NULL,
        verbose_name = "Arrival Terminal",
        help_text = "Outgoing Trip First Flight Arrival Terminal")
    out_second_flight = models.ForeignKey(
        Flight, 
        blank = True, 
        null = True,
        related_name = 'out_second_flights', 
        on_delete=models.PROTECT, 
        verbose_name="Second Flight",
        help_text = "Outgoing Trip Second Flight Name")
    out_second_flight_dep_term = models.ForeignKey(
        AirportTerminal, 
        related_name = 'out_second_flights_dep_term', 
        blank = True, 
        null = True,
        on_delete=models.SET_NULL,
        verbose_name = "Arrival Terminal",
        help_text = "Outgoing Trip Second Flight Departure Terminal")
    out_second_flight_arr_term = models.ForeignKey(
        AirportTerminal, 
        related_name = 'out_second_flights_arr_term', 
        blank = True, 
        null = True,
        on_delete=models.SET_NULL,
        verbose_name = "Arrival Terminal",
        help_text = "Outgoing Trip Second Flight Arrival Terminal")

    # Returning Trip
    # Details
    ret_dep_date = models.DateField(
        null = True,
        blank = True,
        verbose_name="Departure Date",
        help_text = "Returning Trip Departure Date") 
    ret_dep_day = models.CharField(
        max_length = 10,
        blank = True,
        null = True,
        choices = TRIPDAY_CHOICES,
        default = "",
        verbose_name = "Departure Day",
        help_text = "Returning Trip Departure Day")
    ret_arr_date = models.DateField(
        null = True,
        blank = True,
        verbose_name="Arrival Date")
    ret_arr_day = models.CharField(
        max_length = 10,
        blank = True,
        null = True,
        choices = TRIPDAY_CHOICES,
        default = "",
        verbose_name = "Arrival Day",
        help_text = "Returning Trip Arrival Day")
    ret_stop_duration = models.PositiveSmallIntegerField(
        blank=True, 
        null=True, 
        default=0, 
        verbose_name="Stop Duration",
        help_text = "Returning Trip Stop Duration")
    ret_duration = models.PositiveSmallIntegerField(
        blank=True, 
        null=True, 
        default=0, 
        verbose_name="Duration",
        help_text = "Returning Trip Duration")
    ret_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null = True,
        blank = True,
        validators=[MinValueValidator(0.01)],
        verbose_name = "Price")
    ret_class = models.ForeignKey(
        TripClass, 
        default = "",
        null = True,
        blank = True,
        related_name='ret_trips', 
        on_delete=models.SET_NULL, 
        verbose_name="Class",
        help_text = "Returning Trip Flight Class")
    # Flights and Terminals
    ret_first_flight = models.ForeignKey(
        Flight, 
        blank = True, 
        null = True,
        related_name = 'ret_first_flights', 
        on_delete=models.PROTECT, 
        verbose_name="First Flight",
        help_text = "Returning Trip First Flight Name")
    ret_first_flight_dep_term = models.ForeignKey(
        AirportTerminal, 
        related_name = 'ret_first_flights_dep_term', 
        blank = True, 
        null = True,
        on_delete=models.SET_NULL,
        verbose_name = "Departure Terminal",
        help_text = "Returning Trip First Flight Departure Terminal")
    ret_first_flight_arr_term = models.ForeignKey(
        AirportTerminal, 
        related_name = 'ret_first_flights_arr_term', 
        blank = True, 
        null = True,
        on_delete=models.SET_NULL,
        verbose_name = "Arrival Terminal",
        help_text = "Returning Trip First Flight Arrival Terminal")
    ret_second_flight = models.ForeignKey(
        Flight, 
        blank = True, 
        null = True,
        related_name = 'ret_second_flights', 
        on_delete=models.PROTECT, 
        verbose_name="Second Flight",
        help_text = "Returning Trip Second Flight Name")
    ret_second_flight_dep_term = models.ForeignKey(
        AirportTerminal, 
        related_name = 'ret_second_flights_dep_term', 
        blank = True, 
        null = True,
        on_delete=models.SET_NULL,
        verbose_name = "Arrival Terminal",
        help_text = "Returning Trip Second Flight Departure Terminal")
    ret_second_flight_arr_term = models.ForeignKey(
        AirportTerminal, 
        related_name = 'ret_second_flights_arr_term', 
        blank = True, 
        null = True,
        on_delete=models.SET_NULL,
        verbose_name = "Arrival Terminal",
        help_text = "Returning Trip Second Flight Arrival Terminal")

    class Meta:
        verbose_name = 'Trip'
        verbose_name_plural = 'Trips'
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/trips/{0}/".format(self.id)    

    clone_fields = [
            'orig',
            'dest',
            'trav',
            'date_found',
            'out_dep_date',
            'out_dep_day',
            'out_arr_date',
            'out_arr_day',
            'out_stop_duration',
            'out_duration', 
            'out_first_flight',
            'out_second_flight',                     
            'ret_dep_date',
            'ret_dep_day',
            'ret_arr_date',   
            'ret_arr_day',                            
        ]

    def clean(self):

        # Checking if orig is the same as destination
        if self.dest == self.orig:
            raise ValidationError(mark_safe( f"Trip origin {self.orig} cannot be the saame \
                as trip destination {self.dest}" ))        

        # Outgoing Trip Validation
        # Outgoing First Flight Validations
        # Checking if the trip origin is the same like first flight departure
        if self.orig != self.out_first_flight.depart_airport.city:
            raise ValidationError(mark_safe( f"There is a mismatch between trip's origin {self.orig} \
                and the outgoing first flight's departing city {self.out_first_flight.depart_airport.city}" ))

        # Checking if the departing airport has the departing terminal
        if self.out_first_flight_dep_term:
            if self.out_first_flight.depart_airport != self.out_first_flight_dep_term.airport:
                raise ValidationError(mark_safe(f"{self.out_first_flight.depart_airport} \
                    doesn't have {self.out_first_flight_dep_term}"))

        # Checking if the arriving airport has the arriving terminal
        if self.out_first_flight_arr_term:
            if self.out_first_flight.arrive_airport != self.out_first_flight_arr_term.airport:
                raise ValidationError(mark_safe(f"{self.out_first_flight.arrive_airport} \
                    doesn't have {self.out_first_flight_arr_term}"))

        # Outgoing Second Flight Validations        
        if self.out_second_flight:

            # Checking if there is an Outgoing second flight without an Outgoing First flight
            if self.out_second_flight and self.out_first_flight == None:
                raise ValidationError("It cannot be an Outgoing Second Flight without an Outgoing First Flight.")

            # Checking if the First and Second Flights are the same
            if self.out_second_flight == self.out_first_flight:
                raise ValidationError("The Outgong Second Flight cannot be the same like the Outgong First Flight.")

            # Checking if the deparing city of the second flight 
            # matches the arriving city of the first flight            
            if self.out_second_flight.depart_airport.city != self.out_first_flight.arrive_airport.city:
                raise ValidationError(mark_safe( f"There is a mismatch between \
                    first flight's arrival city {self.out_first_flight.arrive_airport.city} \
                    and the second flight's departing city {self.out_second_flight.depart_airport.city}" ))

            # Checking if the departing airport has the departing terminal
            if self.out_second_flight_dep_term:
                if self.out_second_flight.depart_airport != self.out_second_flight_dep_term.airport:
                    raise ValidationError(mark_safe( f"{self.out_second_flight.depart_airport} \
                        doesn't have {self.out_second_flight_dep_term}" ))

            # Checking if the arrival airport has the arrival terminal
            if self.out_second_flight_arr_term:
                if self.out_second_flight.arrive_airport != self.out_second_flight_arr_term.airport:
                    raise ValidationError(mark_safe( f"{self.out_second_flight.arrive_airport} \
                        doesn't have {self.out_second_flight_arr_term}" ))

        # Returning Trip Validations
        # Returning First Flight Validations
        # Checking the trip destination is the same like returning first flight departure
        if self.dest != self.ret_first_flight.depart_airport.city:
            raise ValidationError(mark_safe( f"There is a mismatch between trip's destination {self.dest} \
                and the returning first flight's departing city {self.ret_first_flight.depart_airport.city}" ))

        # Checking if the departing airport has the departing terminal
        if self.ret_first_flight_dep_term:
            if self.ret_first_flight.depart_airport != self.ret_first_flight_dep_term.airport:
                raise ValidationError(mark_safe(f"{self.ret_first_flight.depart_airport} \
                    doesn't have {self.ret_first_flight_dep_term}"))

        # Checking if the arriving airport has the arriving terminal
        if self.ret_first_flight_arr_term:
            if self.ret_first_flight.arrive_airport != self.ret_first_flight_arr_term.airport:
                raise ValidationError(mark_safe(f"{self.ret_first_flight.arrive_airport} \
                    doesn't have {self.ret_first_flight_arr_term}"))

        # Returning Second Flight Validations        
        if self.ret_second_flight:

            # Checking if there is a Returning second flight without a Returning First flight
            if self.ret_second_flight and self.ret_first_flight == None:
                raise ValidationError("It cannot be a Returning Second Flight without a Returning First Flight.")

            # Checking if the First and Second Flights are the same
            if self.ret_second_flight == self.ret_first_flight:
                raise ValidationError("The Returning Second Flight cannot be the same like the Returning First Flight.")

            # Checking if the deparing city of the second flight 
            # matches the arriving city of the first flight            
            if self.ret_second_flight.depart_airport.city != self.ret_first_flight.arrive_airport.city:
                raise ValidationError(mark_safe( f"There is a mismatch between \
                    first flight's arrival city {self.ret_first_flight.arrive_airport.city} \
                    and the second flight's departing city {self.ret_second_flight.depart_airport.city}" ))

            # Checking if the departing airport matches with the departing terminal
            if self.ret_second_flight_dep_term:
                if self.ret_second_flight.depart_airport != self.ret_second_flight_dep_term.airport:
                    raise ValidationError(mark_safe( f"{self.ret_second_flight.depart_airport} \
                        doesn't have {self.ret_second_flight_dep_term}" ))

            # Checking if the arrival airport matches with the arrival terminal
            if self.ret_second_flight_arr_term:
                if self.ret_second_flight.arrive_airport != self.ret_second_flight_arr_term.airport:
                    raise ValidationError(mark_safe( f"{self.ret_second_flight.arrive_airport} \
                        doesn't have {self.ret_second_flight_arr_term}" ))


class Traveller(models.Model):
    name = models.CharField(max_length=200, unique=True)   
    notes = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = 'Traveller'
        verbose_name_plural = 'Travellers'
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/travellers/{0}/".format(self.id)


class Seat(models.Model):
    seat_number = models.CharField(max_length=4)
    traveller = models.ForeignKey(
        Traveller, 
        related_name = 'seats', 
        on_delete=models.PROTECT )
    trip = models.ForeignKey(
        Trip, 
        related_name = 'seats', 
        on_delete=models.PROTECT )
    flight = models.ForeignKey(
        Flight, 
        related_name = 'seats', 
        on_delete=models.PROTECT )
    notes = RichTextUploadingField(blank=True, null=True)

    class Meta:
        verbose_name = 'Seat'
        verbose_name_plural = 'Seats'
        ordering = ["seat_number"]

    def __str__(self):
        return self.seat_number

    def get_absolute_url(self):
        return "/seats/{0}/".format(self.id)

    def clean(self):

        trip_flights = []

        trip_flights.append(self.trip.out_first_flight)

        if self.trip.out_second_flight:
            trip_flights.append(self.trip.out_second_flight)

        if self.trip.ret_first_flight:
            trip_flights.append(self.trip.ret_first_flight)

        if self.trip.ret_second_flight:
            trip_flights.append(self.trip.ret_second_flight)

        if self.flight not in trip_flights:
            raise ValidationError(mark_safe( f"The flight {self.flight} is not \
                in the trip {self.trip}" ))     

