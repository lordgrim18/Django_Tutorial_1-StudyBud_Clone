from django.forms import  ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        #here RoomForm takes all the attributes from room inside models.py
        exclude = ['host', 'participants']
        