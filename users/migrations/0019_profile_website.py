# Generated by Django 2.1.4 on 2020-06-07 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_status_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='website',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
