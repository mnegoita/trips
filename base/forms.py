from django import forms 



### Search Form #####################################

SEARCH_TYPE_CHOICES = (
    ('', 'All Objects'),
    ('Trips', (
        ('city', 'City'),
        ('airline', 'Airline'),
        ('airplane', 'Airplane'),
        ('airport', 'Airport'),
        ('airportterminal', 'AirportTerminal'),
        ('flight', 'Flight'),
        ('tripsource', 'TripSource'),
        ('tripclass', 'TripClass'),
        ('trip', 'Trip'),
        ('traveller', 'Traveller'),
        ('seat', 'Seat'),
    )),
)

class SearchForm(forms.Form):
    q = forms.CharField(label='Search')
    obj_type = forms.ChoiceField(choices=SEARCH_TYPE_CHOICES, required=False, label='Type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        for field_name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = ' '.join([css, 'form-control']).strip()            
            field.widget.attrs['placeholder'] = field.label


