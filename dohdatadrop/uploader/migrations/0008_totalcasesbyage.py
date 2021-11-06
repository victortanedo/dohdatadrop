# Generated by Django 3.2.9 on 2021-11-05 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0007_auto_20211104_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalCasesByAge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('age', models.IntegerField()),
                ('recovered_count', models.IntegerField()),
                ('died_count', models.IntegerField()),
                ('on_going', models.IntegerField()),
            ],
        ),
    ]
