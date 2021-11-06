import pandas as pd
from .models import CovidData


def parse_covid_data(df):
    df = df.where(pd.notnull(df), None)
    for i in range(len(df)):
        try:
            covid = CovidData.objects.get(case_code = df.loc[i, 'CaseCode'])
        except CovidData.DoesNotExist:            
            covid = CovidData(case_code=df.loc[i, 'CaseCode'], age=float(df.loc[i, 'Age']), age_group=df.loc[i, 'AgeGroup'], sex=df.loc[i, 'Sex'])
            covid.date_specimen = None if type(df.loc[i, 'DateSpecimen']) == float else df.loc[i, 'DateSpecimen']
            covid.date_result_release = None if type(df.loc[i, 'DateResultRelease']) == float else df.loc[i, 'DateResultRelease']
            covid.date_rep_conf = None if type(df.loc[i, 'DateRepConf']) == float else df.loc[i, 'DateRepConf']
            covid.date_died = None if type(df.loc[i, 'DateDied']) == float else df.loc[i, 'DateDied']
            covid.date_recovered = None if type(df.loc[i, 'DateRecover']) == float else df.loc[i, 'DateRecover']
            covid.removal_type = df.loc[i, 'RemovalType']
            covid.admitted = df.loc[i, 'Admitted']
            covid.region_res = df.loc[i, 'RegionRes']
            covid.prov_res = df.loc[i, 'ProvRes']
            covid.city_mun_res = df.loc[i, 'CityMunRes']
            covid.city_muni_psgc = df.loc[i, 'CityMuniPSGC']
            covid.barangay_res = None if type(df.loc[i, 'BarangayRes']) == float else df.loc[i, 'BarangayRes']
            covid.barangay_psgc = None if type(df.loc[i, 'BarangayPSGC']) == float else df.loc[i, 'BarangayPSGC']
            covid.health_status = df.loc[i, 'HealthStatus']
            covid.quarantined = df.loc[i, 'Quarantined']
            covid.date_onset = None if type(df.loc[i, 'DateOnset']) == float else df.loc[i, 'DateOnset']
            covid.pregnant = df.loc[i, 'Pregnanttab']
            covid.validation_status = df.loc[i, 'ValidationStatus']
            covid.save()
