# Generated by Django 5.0.6 on 2024-06-28 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_transaction_sender_alter_transaction_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='cnic',
        ),
        migrations.AddField(
            model_name='account',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='postel_code',
            field=models.CharField(max_length=50),
        ),
    ]
