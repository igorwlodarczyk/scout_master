# Generated by Django 4.2.6 on 2023-12-02 17:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scouting", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="player",
            old_name="first_name",
            new_name="name",
        ),
        migrations.RemoveField(
            model_name="player",
            name="last_name",
        ),
        migrations.RemoveField(
            model_name="player",
            name="weight",
        ),
        migrations.AddField(
            model_name="scoutreport",
            name="minutes_played",
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="scoutreport",
            name="scout_name",
            field=models.CharField(default="user", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="player",
            name="height",
            field=models.IntegerField(),
        ),
    ]