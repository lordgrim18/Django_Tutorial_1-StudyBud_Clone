# not everything can be converted into jason format
#things like dictionaries and stuff can be converted but not objects
#to convert things into  jason format we use serializers

from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'