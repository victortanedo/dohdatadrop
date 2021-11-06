from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validate_file_extension(value):
    if not value.name.endswith('.csv'):
        raise ValidationError(u'Only upload CSV files')

# Create your models here.
class UploaderModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    row_count = models.IntegerField(null=True)
    file_upload = models.FileField(upload_to='data/', validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    file_size = models.TextField(max_length=50)

class CovidData(models.Model):
    case_code = models.CharField(max_length=20)
    age = models.FloatField(null=True)
    age_group = models.CharField(max_length=20,null=True)
    sex = models.CharField(max_length=6,null=True)
    date_specimen = models.DateField(null=True)
    date_result_release = models.DateField(null=True)
    date_rep_conf = models.DateField(null=True)
    date_died = models.DateField(null=True)
    date_recovered = models.DateField(null=True)
    removal_type = models.CharField(max_length=20, null=True)
    admitted = models.CharField(max_length=20, null=True)
    region_res = models.CharField(max_length=20, null=True)
    prov_res = models.CharField(max_length=20, null=True)
    city_mun_res = models.CharField(max_length=20, null=True)
    city_muni_psgc = models.CharField(max_length=20, null=True)
    barangay_res = models.CharField(max_length=20, null=True)
    barangay_psgc = models.CharField(max_length=20, null=True)
    health_status = models.CharField(max_length=50)
    quarantined = models.CharField(max_length=20, null=True)
    date_onset = models.DateField(null=True)
    pregnant = models.CharField(max_length=20, null=True)
    validation_status = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return self.case_code

class TotalCasesByAge(models.Model):
    date = models.DateField()
    age = models.IntegerField()
    recovered_count = models.IntegerField()
    died_count = models.IntegerField()
    on_going = models.IntegerField()

class ListCasesByAge(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=50)
    case_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    date_reported = models.DateField()    