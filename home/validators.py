from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

def textfield_not_empty(textfield):
   """
    Strip white space from textfield and raise validation error
    if field is left empty
    """
    cleaned_data = strip_tags( textfield ).replace('&nbsp;', "").strip()
    if cleaned_data == "":
        raise ValidationError("Please fill in this field")