# Generated by Django 5.1.2 on 2024-10-17 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_name_booking_full_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Booking',
            new_name='Booking_Now',
        ),
        migrations.RenameField(
            model_name='booking_now',
            old_name='Full_Name',
            new_name='Name',
        ),
    ]