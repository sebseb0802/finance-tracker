# Generated by Django 5.2.1 on 2025-07-20 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0009_budget"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="budget",
            name="frequency",
        ),
        migrations.AddField(
            model_name="budget",
            name="yearlyValue",
            field=models.IntegerField(default=1),
        ),
    ]
