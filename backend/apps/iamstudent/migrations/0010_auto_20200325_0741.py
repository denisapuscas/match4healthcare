# Generated by Django 3.0.4 on 2020-03-25 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamstudent', '0009_auto_20200325_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='ausbildung_typ_pflege',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='ausbildung_typ_pflege_abschnitt',
            field=models.IntegerField(choices=[(0, 'Keine Angabe'), (1, '1. Jahr'), (2, '2. Jahr'), (3, '3. Jahr'), (4, 'Berufstätig')], default=0, null=True),
        ),
    ]
