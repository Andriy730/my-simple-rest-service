# Generated by Django 2.2.6 on 2019-11-01 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='creation_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
