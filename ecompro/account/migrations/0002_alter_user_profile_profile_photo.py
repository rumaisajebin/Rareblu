# Generated by Django 4.2.6 on 2023-11-27 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='product/profile'),
        ),
    ]
