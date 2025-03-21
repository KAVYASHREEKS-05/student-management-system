# Generated by Django 5.1.7 on 2025-03-12 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0003_assignment"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignment",
            name="student_submission",
            field=models.FileField(blank=True, null=True, upload_to="submissions/"),
        ),
        migrations.AddField(
            model_name="assignment",
            name="submitted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
