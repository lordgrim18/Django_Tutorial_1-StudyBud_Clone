from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q      #allows us to use & and | by using Q
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login , logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic,Message
from .forms import RoomForm

#rooms= [
#    {'id' : 1,'name' : 'lets learn python'},
#    {'id' : 2,'name' : 'design with me'},
#    {'id' : 3,'name' : 'frontend developers'},
#]

def loginPage(request):                 #do not use the name login as there  is a function with that name
    page = 'login'
    if request.user.is_authenticated:         #this if ensures that an already logged in user cannot go to the login pg again unless they have logged out
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page' : page }
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  #commit is set to false so tht it is not automatically updated, this is done so that we can clean things like username using lower()
            user.username = user.username.lower()   
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'an error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request): 
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|        #only topic__name is needed for sidebar
        Q(name__icontains=q)|                #Q is introduced to use the | and & function
        Q(description__icontains=q)             # name and description are used together with topic for seacrh
        )
          #icontains check if q is present in any part of topic name and is   used for the ALL component of side bar #icontains and conains defer based on their case sensitiviy
          

        
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    #room_messages = Message.objects.all() #displays activity of every topic even if a particular topic is selected from the side bar
    room_messages = Message.objects.filter(room__topic__name__icontains=q) # __ means tht the right object is a subset of the left one

    context= {'rooms' : rooms, 'topics': topics, 'room_count':rooms_count , 'room_messages': room_messages }
    return render(request, 'base/home.html', context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages = room.message_set.all()      #here message is a child of rooom and its name is called in lowercase     # -created gives the descending order   
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)         #we can set the code without redirect but redirect should be used to reload the page and apply all changes

    context = {'room':room, 'room_messages' : room_messages , 'participants' : participants}

    return render(request, 'base/room.html',context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()           #we can get all the children of a specific object by using the code format        modelname_set.condition()
    room_messages = user.message_set.all()
    topics = Topic.objects.all() 
    context = {'user' : user , 'rooms': rooms ,'room_messages': room_messages , 'topics': topics} 
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')            #only users can create rooms and hence login is required
def createRoom(request):
    form = RoomForm()

    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)      #gives us an instant of the room so tht we can set values
            room.host = request.user
            room.save()
            return redirect('home')

    context= {'form':form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login') 
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    
    if request.user != room.host:                   #restrictions are placed so that only the user wwho created the room can update it
        return HttpResponse('you are not allowed here!! ')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home') 

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login') 
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:                        
        return HttpResponse('you are not allowed here!! ')

    if request.method == 'POST':
        room.delete() 
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room}) 


@login_required(login_url='login') 
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:                        
        return HttpResponse('you are not allowed here!! ')

    if request.method == 'POST':
        message.delete() 
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':message}) 