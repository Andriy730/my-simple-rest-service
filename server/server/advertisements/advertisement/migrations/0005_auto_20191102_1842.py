# Generated by Django 2.2.6 on 2019-11-02 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0004_auto_20191102_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advertisements', to=settings.AUTH_USER_MODEL),
        ),
    ]
