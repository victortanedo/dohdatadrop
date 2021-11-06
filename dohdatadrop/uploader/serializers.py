from rest_framework import serializers
from .models import CovidData, TotalCasesByAge, ListCasesByAge

class TotalCasesByAgeSerializer(serializers.Serializer):
    date = serializers.DateField()
    age = serializers.IntegerField()
    recovered_count = serializers.IntegerField()
    died_count = serializers.IntegerField()
    on_going = serializers.IntegerField()

class ListCasesByAgeSerializer(serializers.Serializer):
    date = serializers.DateField()
    status = serializers.CharField(max_length=50)
    case_number = serializers.CharField(max_length=20)
    gender = serializers.CharField(max_length=6)
    date_reported = serializers.DateField() 

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CovidData
        fields = '__all__'