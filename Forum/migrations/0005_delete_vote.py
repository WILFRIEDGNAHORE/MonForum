# Generated by Django 5.1.2 on 2024-11-11 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0004_vote'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
