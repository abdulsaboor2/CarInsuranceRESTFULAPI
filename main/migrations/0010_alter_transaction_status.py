# Generated by Django 5.0.6 on 2024-06-07 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_transaction_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('success', 'success'), ('cancel', 'Cancel')], default='pending', max_length=10),
        ),
    ]
