from mongoengine.fields import StringField
from django.forms.fields import TextInput

class UpperStringField(StringField):
    def to_python(self, value):
        return unicode(value).upper()

    def get_custom_widget(self):
        """
        retorna o widget desse field
        """
        return TextInput(attrs={'class': 'upper'})
