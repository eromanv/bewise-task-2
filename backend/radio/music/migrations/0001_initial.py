# Generated by Django 4.2.2 on 2023-06-09 15:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("user_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("access_token", models.CharField(max_length=255)),
            ],
        ),
    ]