# Generated by Django 5.0 on 2024-01-14 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_listing_num_of_bids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, default='None', on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.category'),
        ),
    ]
