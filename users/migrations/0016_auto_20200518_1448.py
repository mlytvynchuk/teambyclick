# Generated by Django 2.1.4 on 2020-05-18 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_chat_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../static_root/images/users/default.png', upload_to='profile_pics'),
        ),
    ]
