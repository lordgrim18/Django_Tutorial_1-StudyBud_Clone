from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Topic(models.Model):              #room is a  child of a topic 
    name = models.CharField(max_length=200)

    def __str__(self):
        return  self.name


class Room(models.Model):           #room child of topic
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)     #set_null doesnt delete the entire data and just sets the data as null in the database  which can later be changed      #here we need only Topic as the clss Topic is defined above Room but if it is defined below room then topic should be called as a string as 'Topic'
    #null=True allows the database to have null values
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants' , blank=True)     
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']          # - shows that the order is reversed

    def __str__(self):                          #controls the name of object of Room displayed in admin page
        return  self.name


class Message(models.Model):         #message child of room       #message to be displayed when necessary or on each page
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  #where Room is the parent class name and we know what is connected to what   #also cascade means that when  a room is deleted all data associated with it is also deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]                  #ie the the preview only needs to show the first 50 characters

    class Meta:
        ordering = ['-updated','-created']          # orders the entire class instead of ordering each function