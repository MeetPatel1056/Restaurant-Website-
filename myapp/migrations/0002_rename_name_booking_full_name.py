# Generated by Django 5.1.2 on 2024-10-16 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='name',
            new_name='Full_Name',
        ),
    ]
