# Generated by Django 5.1.7 on 2025-03-25 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasedetails',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='purchasedetails',
            name='balance_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selldetails',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selldetails',
            name='balance_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='selldetails',
            name='unit_price',
            field=models.IntegerField(default=0),
        ),
    ]
