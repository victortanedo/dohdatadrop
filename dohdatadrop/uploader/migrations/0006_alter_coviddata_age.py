# Generated by Django 3.2.9 on 2021-11-04 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0005_coviddata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coviddata',
            name='age',
            field=models.FloatField(),
        ),
    ]
