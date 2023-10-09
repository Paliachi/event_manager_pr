# Generated by Django 4.2.6 on 2023-10-09 12:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="participants_quantity",
            new_name="max_participants_capacity",
        ),
        migrations.AddField(
            model_name="event",
            name="occupied_capacity",
            field=models.IntegerField(default=0),
        ),
    ]
