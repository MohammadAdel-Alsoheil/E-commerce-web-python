# Generated by Django 5.0 on 2024-01-13 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_bids_alter_listing_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='num_of_bids',
            field=models.IntegerField(default=0),
        ),
    ]
