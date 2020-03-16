from django.db import models
from django.utils import timezone

# Create your models here.

#operative comes before we define AWTeam
class Operative(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=200, help_text='Please enter an email, max 200 characters')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class AWTeam(models.Model):
    awteam_name = models.CharField(max_length=100)
    #leader = models.ForeignKey(Operative, null=True, blank=True, default=None, on_delete=models.SET_NULL)
        #when the REFERENCED object is deleted, do on_delete, set this field to null
        #Basically blank allows you to pass it a null value, but null tells the database to accept null values. 
    op_team = models.ManyToManyField(Operative)
    #https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/
    #why declare manytomany here, not in operative? Bc we need to create the operatives before we can create a team


    class Meta:
        ordering = ['awteam_name']

    def __str__(self):
        return self.awteam_name

class Mission(models.Model):
    mission_name = models.CharField(max_length=100, null=False, blank=False)
    awteam = models.ForeignKey(AWTeam, null=False, blank=False, default=None, on_delete=models.CASCADE)
    #we don't specify what to do on_delete

    type_choices = [
        ('intel', 'Gather intel'),
        ('retrieve', 'Retrieve'),
        ('lockdown', 'Lock down area'),
        ('rescue', 'Rescue target'),
    ]
    #The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name

    type = models.CharField(max_length=20, choices=type_choices, default='intel')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField()

    class Meta:
        ordering = ['mission_name']

    def __str__(self):
        return self.mission_name



    


