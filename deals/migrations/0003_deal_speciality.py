# Generated by Django 2.1.4 on 2018-12-08 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20181207_1442'),
        ('deals', '0002_remove_deal_speciality'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='speciality',
            field=models.ManyToManyField(blank=True, related_name='deals', to='users.Speciality'),
        ),
    ]
