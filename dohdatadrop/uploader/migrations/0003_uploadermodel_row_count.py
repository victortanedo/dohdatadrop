# Generated by Django 3.2.7 on 2021-11-04 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0002_uploadermodel_file_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadermodel',
            name='row_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
