# Generated by Django 4.2.6 on 2023-11-16 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0002_remove_orderitem_product_remove_orderitem_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('address1', models.CharField(blank=True, max_length=250, null=True)),
                ('address2', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('post_code', models.CharField(blank=True, max_length=20, null=True)),
                ('flag', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
