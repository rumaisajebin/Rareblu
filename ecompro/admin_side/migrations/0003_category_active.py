# Generated by Django 4.2.6 on 2023-10-31 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0002_remove_brand_brand_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
