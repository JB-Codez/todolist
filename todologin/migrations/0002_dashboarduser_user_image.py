# Generated by Django 4.2.3 on 2023-08-19 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todologin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboarduser',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]