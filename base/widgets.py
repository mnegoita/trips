from django import forms 
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings




class RelatedFieldWidgetSingle(widgets.Select):

    def __init__(self, related_model, related_url=None, *args, **kw):
        super().__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = '%s:%s_add' % info

        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super().render(name, value, *args, **kwargs)]
        output.append('<a href="%s?_to_field=id&_popup=1" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
            (self.related_url, name))
        output.append('<img src="%sadmin/img/icon-addlink.svg" width="20" height="20" alt="%s"/></a>' % (settings.STATIC_URL, 'Add Another'))
        return mark_safe(''.join(output))
      

class SplitDurationWidget(forms.MultiWidget):
    """
    A Widget that splits duration input into two number input boxes.
    """

    def __init__(self, attrs=None):
        widgets = (forms.NumberInput(attrs={'style': "width: 4em", 'min': 0, 'max': 24 }),
                   forms.NumberInput(attrs={'style': "width: 4em", 'min': 0, 'max': 60 }))
        super(SplitDurationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            d = int(value)
            if d:
                hours = d // 60
                minutes = d % 60
                return [int(hours), int(minutes)]
        return [0, 0]
        

class MultiValueDurationField(forms.MultiValueField):
    widget = SplitDurationWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField()
        )
        super(MultiValueDurationField, self).__init__(
            fields=fields,
            require_all_fields=True, *args, **kwargs)


    def compress(self, data_list):
        hours=int(data_list[0])
        minutes=int(data_list[1])
        duration = hours * 60 + minutes
        return(duration) 
