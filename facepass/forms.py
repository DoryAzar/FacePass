from django import forms
from .models import *


class PersonalInformationForm(forms.ModelForm):
    """
    PersonalInformationForm Form class for generating a form
    for manipulating personal

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PersonalInformation
        fields = Information.get_information(Information, False)
        widgets = {
            'birthdate': forms.DateInput({
                "type": "date"
            })
        }


def set_method(input="POST"):
    """
    Method that sets the form method
    for spoofing PUT and DELETE requests

    """

    methods = {
        "html_method": "POST"
    }
    SPOOF_METHODS = {
        "POST": "POST",
        "GET":  "GET",
        "DELETE": "POST",
        "PUT": "POST"
    }
    method = input if type(input) == str and input.upper(
    ) in SPOOF_METHODS.keys() else "POST"

    # If PUT or DELETE return both the html and spoof methods
    if method and method != SPOOF_METHODS[method]:
        methods['html_method'] = "POST"
        methods['spoof_method'] = method
    else:
        methods['html_method'] = method

    return methods
