# Generated by Django 4.1.5 on 2023-01-17 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="clicked_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]