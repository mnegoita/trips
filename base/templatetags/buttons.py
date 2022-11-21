from django import template
from django.urls import reverse

register = template.Library()

template_path = 'base/buttons/'




def get_view_name(instance, action):
    
    assert action in ('add', 'edit', 'delete', 'list')
    view_name = "{}:{}_{}".format(
        instance._meta.app_label, instance._meta.model_name, action
    )

    return view_name


# List View URL template tag ##########################

@register.simple_tag
def list_view_url(instance):
    
    view_name = get_view_name(instance, 'list')    
    url = '{}'.format(reverse(view_name))

    return url
    

# Edit Button ############################################

@register.inclusion_tag(template_path + 'edit.html')
def edit_button(instance):
    view_name = get_view_name(instance, 'edit')

    if hasattr(instance, 'slug'):
        kwargs = {'slug': instance.slug}
    else:
        kwargs = {'pk': instance.pk}

    url = reverse(view_name, kwargs=kwargs)

    return {
        'url': url,
    }


# Delete Button #############################################

@register.inclusion_tag(template_path + 'delete.html')
def delete_button(instance, use_pk=False):
    view_name = get_view_name(instance, 'delete')

    if hasattr(instance, 'slug') and not use_pk:
        kwargs = {'slug': instance.slug}
    else:
        kwargs = {'pk': instance.pk}

    url = reverse(view_name, kwargs=kwargs)

    return {
        'url': url,
    }


# Add Button ##########################################

@register.inclusion_tag(template_path + 'add.html')
def add_button(app_name, obj_name):

    add_url = reverse(f"{app_name}:{obj_name}_add")

    return {
        'url': add_url,
    }


# Clone Button ################################################

def prepare_cloned_fields(instance):

    params = {}
    for field_name in getattr(instance, 'clone_fields', []):
        field = instance._meta.get_field(field_name)
        field_value = field.value_from_object(instance)

        # Swap out False with URL-friendly value
        if field_value is False:
            field_value = ''

        # Omit empty values
        if field_value not in (None, ''):
            params[field_name] = field_value

    # Concatenate parameters into a URL query string
    param_string = '&'.join(
        ['{}={}'.format(k, v) for k, v in params.items()]
    )

    return param_string

@register.inclusion_tag(template_path + 'clone.html')
def clone_button(instance):
    view_name = get_view_name(instance, 'add')

    # Populate cloned field values
    param_string = prepare_cloned_fields(instance)
    if param_string:
        url = '{}?{}'.format(reverse(view_name), param_string)

    return {
        'url': url,
    }
