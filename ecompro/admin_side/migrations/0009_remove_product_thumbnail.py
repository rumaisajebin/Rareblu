# Generated by Django 4.2.6 on 2023-11-14 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0008_product_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='thumbnail',
        ),
    ]
