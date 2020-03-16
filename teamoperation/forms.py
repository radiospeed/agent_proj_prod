from django import forms
from .models import AWTeam, Operative, Mission
from django.contrib.admin.widgets import FilteredSelectMultiple

# class AWTeamForm(forms.ModelForm):
#     class Meta:
#         model = AWTeam
#         fields = [
#             'awteam_name',
#             'op_team',
#         ]

class OperativeForm(forms.ModelForm):
    class Meta:
        model = Operative
        fields = [
            'name',
            'email',        
        ]

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = [
            'mission_name',
            'awteam',
            'type',
            'notes',
            #'start_date',
            #'end_date',
        ]

    def __init__(self, *args, **kwargs):
        #get initial arguements(there may be NONE though)
        initial_argum = kwargs.get('initial', None)
        updated_initial={}
        if initial_argum:
            #if we HAVE arguements with (keyword = 'initial'), 
            # then fetch 'myAwteam' placeholder variable (though we may not have this keyword, in which
            # case it's NONE )
            myinitTeam = initial_argum.get('myAwteam', None)
            if myinitTeam:
                print("in mission form init, the myinitTeam is: ", myinitTeam)
                #First we name a team object, then we can access all its members via op_team
                myTeam = AWTeam.objects.get(id=myinitTeam)
                list_of_ops = myTeam.op_team.all()
                #GET returns ONE thing, filter and ALL() returns a queryset
                myStr = ', '.join([str(x) for x in list_of_ops])
                updated_initial['notes'] = "The agents on this mission are: " + myStr
                updated_initial['awteam'] = myTeam
        kwargs.update(initial=updated_initial)
        super(MissionForm, self).__init__(*args, **kwargs)




    
class TeamForm(forms.ModelForm):
    op_team = forms.ModelMultipleChoiceField(
        queryset=Operative.objects.all(),
        widget=FilteredSelectMultiple(
            "Operatives", 
            is_stacked=False,
            attrs={'size': 7},
        )
    )

    class Meta:
        model = AWTeam
        fields = [
            'awteam_name',
            'op_team', 
        ]
        #we list the field then override field's widget
        #https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#overriding-the-default-fields
        #https://docs.djangoproject.com/en/3.0/ref/forms/widgets/#selectmultiple
        # widgets = {
        #     'op_team': forms.SelectMultiple(attrs={'size': 7})
        # }

        class Media:
            # Django also includes a few javascript files necessary
            # for the operation of this form element. You need to
            # include <script src="/admin/jsi18n"></script> or <script type="text/javascript" src="{% url 'admin:jsi18n' %}"></script>
            # in the template.
            #see https://stackoverflow.com/questions/24572289/how-to-properly-render-filteredselectmultiple
            #for what we need in templates
            css = {'all':('/admin/css/widgets.css', '/admin/css/overrides.css', 'static/teamoperation/style3.css',),}
            js = ('/admin/jquery.js','/admin/jsi18n/')


        

