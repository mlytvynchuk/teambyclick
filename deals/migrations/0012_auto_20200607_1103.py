# Generated by Django 2.1.4 on 2020-06-07 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0011_auto_20200607_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='presentation_link',
            field=models.URLField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='deal',
            name='website_link',
            field=models.URLField(blank=True, max_length=128),
        ),
    ]
