# Generated by Django 3.1.2 on 2020-10-10 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20201010_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.city'),
        ),
    ]
