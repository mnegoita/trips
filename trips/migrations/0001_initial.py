# Generated by Django 4.1.2 on 2022-11-21 16:29

import ckeditor_uploader.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('country', models.CharField(max_length=30)),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Airline',
                'verbose_name_plural': 'Airlines',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Airplane',
                'verbose_name_plural': 'Airplanes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('code', models.CharField(max_length=3, unique=True)),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Airport',
                'verbose_name_plural': 'Airports',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='AirportTerminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='terminals', to='trips.airport')),
            ],
            options={
                'verbose_name': 'Airport terminal',
                'verbose_name_plural': 'Airport Terminals',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('country', models.CharField(max_length=30)),
                ('prov_st', models.CharField(blank=True, max_length=30, null=True, verbose_name='Province/State')),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Add the Flight name', max_length=40, verbose_name='Flight Name')),
                ('duration', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Duration')),
                ('depart_time', models.TimeField(blank=True, default=None, null=True, verbose_name='Departure Time')),
                ('arrive_time', models.TimeField(blank=True, default=None, null=True, verbose_name='Arrival Time')),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flights', to='trips.airline', verbose_name='Airline Name')),
                ('airplane', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='flights', to='trips.airplane', verbose_name='Airplane Name')),
                ('arrive_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flightsarrive', to='trips.airport', verbose_name='Arrival Airport')),
                ('depart_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flightsdepart', to='trips.airport', verbose_name='Departure Airport')),
            ],
            options={
                'verbose_name_plural': 'Flights',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Traveller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Traveller',
                'verbose_name_plural': 'Travellers',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TripSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Trip Source',
                'verbose_name_plural': 'Trip Sources',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TripClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trip_classes', to='trips.airline', verbose_name='Airline')),
            ],
            options={
                'verbose_name': 'Trip Class',
                'verbose_name_plural': 'Trip Classes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('trav', models.PositiveSmallIntegerField(default=1, verbose_name='Travellers')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Price')),
                ('currency', models.CharField(blank=True, choices=[('CAD', 'CAD'), ('USD', 'USD'), ('EUR', 'EUR')], default='', max_length=5, null=True, verbose_name='Currency')),
                ('date_found', models.DateField(blank=True, null=True, verbose_name='Date Found')),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('out_dep_date', models.DateField(help_text='Outgoing Trip Departure Date', verbose_name='Departure Date')),
                ('out_dep_day', models.CharField(blank=True, choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], default='', help_text='Outgoing Trip Departure Day', max_length=10, null=True, verbose_name='Departure Day')),
                ('out_arr_date', models.DateField(verbose_name='Arrival Date')),
                ('out_arr_day', models.CharField(blank=True, choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], default='', help_text='Outgoing Trip Arrival Day', max_length=10, null=True, verbose_name='Arrival Day')),
                ('out_stop_duration', models.PositiveSmallIntegerField(blank=True, default=0, help_text='Outgoing Trip Stop Duration', null=True, verbose_name='Stop Duration')),
                ('out_duration', models.PositiveSmallIntegerField(blank=True, default=0, help_text='Outgoing Trip Duration', null=True, verbose_name='Duration')),
                ('out_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Price')),
                ('ret_dep_date', models.DateField(blank=True, help_text='Returning Trip Departure Date', null=True, verbose_name='Departure Date')),
                ('ret_dep_day', models.CharField(blank=True, choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], default='', help_text='Returning Trip Departure Day', max_length=10, null=True, verbose_name='Departure Day')),
                ('ret_arr_date', models.DateField(blank=True, null=True, verbose_name='Arrival Date')),
                ('ret_arr_day', models.CharField(blank=True, choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], default='', help_text='Returning Trip Arrival Day', max_length=10, null=True, verbose_name='Arrival Day')),
                ('ret_stop_duration', models.PositiveSmallIntegerField(blank=True, default=0, help_text='Returning Trip Stop Duration', null=True, verbose_name='Stop Duration')),
                ('ret_duration', models.PositiveSmallIntegerField(blank=True, default=0, help_text='Returning Trip Duration', null=True, verbose_name='Duration')),
                ('ret_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Price')),
                ('dest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trips_dest', to='trips.city', verbose_name='Trip To')),
                ('orig', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trips_orig', to='trips.city', verbose_name='Trip From')),
                ('out_class', models.ForeignKey(blank=True, default='', help_text='Outgoing Trip Flight Class', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='out_trips', to='trips.tripclass', verbose_name='Class')),
                ('out_first_flight', models.ForeignKey(help_text='Outgoing Trip First Flight Name', on_delete=django.db.models.deletion.PROTECT, related_name='out_first_flights', to='trips.flight', verbose_name='First Flight')),
                ('out_first_flight_arr_term', models.ForeignKey(blank=True, help_text='Outgoing Trip First Flight Arrival Terminal', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='out_first_flights_arr_term', to='trips.airportterminal', verbose_name='Arrival Terminal')),
                ('out_first_flight_dep_term', models.ForeignKey(blank=True, help_text='Outgoing Trip First Flight Departure Terminal', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='out_first_flights_dep_term', to='trips.airportterminal', verbose_name='Departure Terminal')),
                ('out_second_flight', models.ForeignKey(blank=True, help_text='Outgoing Trip Second Flight Name', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='out_second_flights', to='trips.flight', verbose_name='Second Flight')),
                ('out_second_flight_arr_term', models.ForeignKey(blank=True, help_text='Outgoing Trip Second Flight Arrival Terminal', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='out_second_flights_arr_term', to='trips.airportterminal', verbose_name='Arrival Terminal')),
                ('out_second_flight_dep_term', models.ForeignKey(blank=True, help_text='Outgoing Trip Second Flight Departure Terminal', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='out_second_flights_dep_term', to='trips.airportterminal', verbose_name='Arrival Terminal')),
                ('ret_class', models.ForeignKey(blank=True, default='', help_text='Returning Trip Flight Class', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ret_trips', to='trips.tripclass', verbose_name='Class')),
                ('ret_first_flight', models.ForeignKey(blank=True, help_text='Returning Trip First Flight Name', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ret_first_flights', to='trips.flight', verbose_name='First Flight')),
                ('ret_first_flight_arr_term', models.ForeignKey(blank=True, help_text='Returning Trip First Flight Arrival Terminal', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ret_first_flights_arr_term', to='trips.airportterminal', verbose_name='Arrival Terminal')),
                ('ret_first_flight_dep_term', models.ForeignKey(blank=True, help_text='Returning Trip First Flight Departure Terminal', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ret_first_flights_dep_term', to='trips.airportterminal', verbose_name='Departure Terminal')),
                ('ret_second_flight', models.ForeignKey(blank=True, help_text='Returning Trip Second Flight Name', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ret_second_flights', to='trips.flight', verbose_name='Second Flight')),
                ('ret_second_flight_arr_term', models.ForeignKey(blank=True, help_text='Returning Trip Second Flight Arrival Terminal', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ret_second_flights_arr_term', to='trips.airportterminal', verbose_name='Arrival Terminal')),
                ('ret_second_flight_dep_term', models.ForeignKey(blank=True, help_text='Returning Trip Second Flight Departure Terminal', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ret_second_flights_dep_term', to='trips.airportterminal', verbose_name='Arrival Terminal')),
                ('source_found', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trips', to='trips.tripsource', verbose_name='Trip Source')),
            ],
            options={
                'verbose_name': 'Trip',
                'verbose_name_plural': 'Trips',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.CharField(max_length=4)),
                ('notes', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seats', to='trips.flight')),
                ('traveller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seats', to='trips.traveller')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seats', to='trips.trip')),
            ],
            options={
                'verbose_name': 'Seat',
                'verbose_name_plural': 'Seats',
                'ordering': ['seat_number'],
            },
        ),
        migrations.AddField(
            model_name='airport',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='airports', to='trips.city'),
        ),
    ]