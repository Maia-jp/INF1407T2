# Generated by Django 4.1.3 on 2022-11-21 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgLang",
            fields=[
                (
                    "name",
                    models.CharField(max_length=24, primary_key=True, serialize=False),
                ),
                ("helloWorld", models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name="Snippet",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=1024)),
                ("title", models.CharField(max_length=36)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "lang",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="snippet.proglang",
                    ),
                ),
            ],
        ),
    ]
