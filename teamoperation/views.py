from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Operative, AWTeam, Mission
from .forms import OperativeForm, TeamForm, MissionForm
from . import forms
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    agent_list = ["a", "b", "c"]
    stuff_for_frontend = {'agent_list': agent_list}
    return render(request, 'teamoperation/index.html', stuff_for_frontend)

def operative_create_view(request):
    #when we go to http://127.0.0.1:8000/teamoperation/create_operative/ it will either be to RETRIEVE the 
    # page and display a blank form, in which case it will be a GET request. In this instancem else: form = forms.OperativeForm()
    #will run. This line of code just creates a blank form to render in create_operative.html
    #if we have filled in data on this page and hit SUBMIT, this sends a POST request to this function:
    # <form class ="operativeForm" ... action="{% url 'teamoperation:create_operative' %}" method="POST">
    #this time, we run the if request.method == 'POST': block of code, not the else: block
           
    if request.method == 'POST':
        form = forms.OperativeForm(request.POST)
        #form = forms.OperativeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("success valid form")
            return redirect('teamoperation:index')

    else:
        #else it's a get request
        form = forms.OperativeForm()
        #form = forms.OperativeForm(initital={'name': 'steve', 'email': 'steve@g.com'})
        #this would set the initial value of the form

    context = {
        'operativeForm': form
    }
    return render(request, 'teamoperation/create_operative.html', context)


def mission_create_view(request):
    if request.method == 'POST':
        form = forms.MissionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            #form.save() returns us that instance of the mission form. We put it in an instance 
            #(commit=False) means I dont want to commit to the action just yet. I just want that instance (which  will be saved) 
            # and i'll do something with it
            instance.start_date = timezone.now()
            instance.save()
            print("success create mission")
            return redirect('teamoperation:index')
    else:
        form = forms.MissionForm()
        #form = forms.MissionForm(initial={'notes': 'hello here'})
    context = {
        'missionForm': form,
    }
    return render(request, 'teamoperation/create_mission.html', context)


def mission_create_for_team(request, team_id):
    if request.method == 'POST':
        form = forms.MissionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            #form.save() returns us that instance of the mission form. We put it in an instance 
            #(commit=False) means I dont want to commit to the action just yet. I just want that instance (which  will be saved) 
            # and i'll do something with it
            instance.start_date = timezone.now()
            instance.save()
            print("success create mission")
            return redirect('teamoperation:index')
    else:
        form = forms.MissionForm(initial={'myAwteam': team_id,})
    context = {
        'missionForm': form,
    }
    return render(request, 'teamoperation/create_mission.html', context)


def team_create_view(request):
    if request.method == 'POST':
        form = forms.TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teamoperation:index')

    else:
        form = forms.TeamForm()
    
    context = {
        'teamForm': form,
    }
    return render(request, 'teamoperation/create_team2.html', context)

def operative_list_view(request):
    list_of_operatives = Operative.objects.order_by('id')

    context = {
        'list_operatives': list_of_operatives,
    }
    return render(request, 'teamoperation/search_operatives.html', context)

def team_list_view(request):
    list_of_teams = AWTeam.objects.order_by('id')
    return render(request, 'teamoperation/search_teams.html', {'list_teams': list_of_teams} )


# def operative_edit_view(request, get_operative):
#     get_op = Operative.objects.get(id=get_operative)
#     #get for one returned object, .filter to return a query set
#     context = {
#         'editAgent': get_op,
#     }
#     return render(request, 'teamoperation/edit_operative.html', context)

def operative_edit_display(request, get_operative):
    get_op = Operative.objects.get(id=get_operative)
    #get for one returned object, .filter to return a query set
    form = OperativeForm(instance=get_op)
    # form = OperativeForm(data={
    #     'name': 'myname',
    #     'email': 'myemail',
    # })
    context = {
        'editForm': form,
        'operative_id': get_op.id,
    }
    print("in operative_edit_display, get_op id is: ", get_op.id)
    return render(request, 'teamoperation/edit_operative.html', context)

def operative_edit_submit(request, op_id):
    if request.method == 'POST':
        instance = get_object_or_404(Operative, id=op_id)
        form = OperativeForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            message = "Successfully edited operative"
            context = {
                'message': message,
            }
            return render(request, 'teamoperation/index.html', context)
        else:
            message = "Please review and try again"
            context = {
                'message': message,
            }
            return render(request, 'teamoperation/edit_operative.html', context)


def team_edit_display(request, get_team):
    get_te = AWTeam.objects.get(id=get_team)
    op_names = get_te.op_team.all()
    context = {
        'viewTeam': get_te,
        'viewOp': op_names,
    }
    return render(request, 'teamoperation/edit_team.html', context)
