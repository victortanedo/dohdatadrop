from django.shortcuts import get_object_or_404, render
from .forms import UploaderForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
import pandas as pd
from .parser import parse_covid_data
from rest_framework.decorators import api_view
from .models import TotalCasesByAge, CovidData, ListCasesByAge, UploaderModel
from .serializers import CaseSerializer, TotalCasesByAgeSerializer, ListCasesByAgeSerializer
from rest_framework.response import Response
import datetime

# Create your views here.
@login_required
def uploader_view(request):
    form = UploaderForm()

    context = {
        'form': form,
    }
    return render(request, 'uploader/uploader.html', context)

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create new user object but prevent from saving it yet
            new_user = user_form.save(commit=False)

            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])

            # Save the user object
            new_user.save()
            context = {
                'new_user': new_user,
            }
            return render(request, 'uploader/register_done.html', context)
    else:
        user_form = UserRegistrationForm()

    context = {
        'user_form': user_form,
    }

    return render(request, 'uploader/register.html', context)

@login_required
def audit(request):
    uploads = UploaderModel.objects.all()

    if request.method == 'POST':
        form = UploaderForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data.get('file_upload')
            
            file.seek(0, 2)    

            instance = form.save(commit=False)
            instance.user = request.user
            instance.file_size = file.tell()

            instance.save()

            df = pd.read_csv(instance.file_upload)
            instance.row_count = len(df)            
          
            parse_covid_data(df)
            instance.save()
            file.close()
            
    context = {
        'uploads': uploads,
    }
    return render(request, 'uploader/audit.html', context)

@api_view(['GET'])
def total_cases_by_age(request, year, month, day, age):
    if request.method == 'GET':
        t = TotalCasesByAge()
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            return Response(r'{"detail": "Invalid Date Format."}')

        t.date = f'{year}/{month}/{day}'

        t.age = age

        t.recovered_count =  CovidData.objects.filter(date_recovered=f'{year}-{month}-{day}').filter(age=age).count()      
        t.died_count =  CovidData.objects.filter(date_died=f'{year}-{month}-{day}').filter(age=age).count()
        t.on_going =  CovidData.objects.filter(date_recovered=None).filter(date_died=None).filter(age=age).count()
        
        serializer = TotalCasesByAgeSerializer(t)
        return Response(serializer.data)

@api_view(['GET'])
def list_cases_by_age(request, year, month, day, age):
    if request.method == 'GET':
        lists = []

        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            return Response(r'{"detail": "Invalid Date Format."}')
            
        cc = CovidData.objects.filter(date_recovered=f'{year}-{month}-{day}').filter(age=age)

        for c in cc:
            l = ListCasesByAge()
            l.date = f'{year}-{month}-{day}'
            l.status = 'Recovered'
            l.case_number = c.case_code
            l.gender = c.sex
            l.date_reported = c.date_rep_conf
            lists.append(l)

        cc = CovidData.objects.filter(date_died=f'{year}-{month}-{day}').filter(age=age)

        for c in cc:
            l = ListCasesByAge()
            l.date = f'{year}-{month}-{day}'
            l.status = 'Died'
            l.case_number = c.case_code
            l.gender = c.sex
            l.date_reported = c.date_rep_conf
            lists.append(l)

        cc = CovidData.objects.filter(date_recovered=None).filter(date_died=None).filter(age=age)

        for c in cc:
            l = ListCasesByAge()
            l.date = f'{year}-{month}-{day}'
            l.status = 'Ongoing'
            l.case_number = c.case_code
            l.gender = c.sex
            l.date_reported = c.date_rep_conf
            lists.append(l)
        

        serializer = ListCasesByAgeSerializer(lists, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def case_search(request, case_number):
    case = get_object_or_404(CovidData, case_code=case_number)

    serializer = CaseSerializer(case)

    return Response(serializer.data)