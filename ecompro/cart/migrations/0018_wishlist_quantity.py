# Generated by Django 4.2.6 on 2023-12-12 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0017_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
