# Generated by Django 3.0.4 on 2020-04-02 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamstudent', '0007_auto_20200402_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentlistfiltermodel',
            name='ausbildung_typ_ergotherapie_abschnitt_x_gt',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentlistfiltermodel',
            name='ausbildung_typ_ergotherapie_abschnitt_x_lt',
            field=models.IntegerField(default=0),
        ),
    ]
