from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        "GET/api",
        "GET/api/rooms" , 
        "GET/api/rooms/:id" ,
    ]

    return Response(routes)

    #return JsonResponse(routes , safe=False)       #safe=false shows that the context can have more types of values than python dictionaries


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)       #many=True implies that there are many objects to be serialized
    return Response(serializer.data)        #.data means that we dont need the object but instead its data


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)              #many=False implies that there is only  a sinlge object to be serialized
    return Response(serializer.data)         #.data means that we dont need the object but instead its data