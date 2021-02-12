# Generated by Django 3.1.6 on 2021-02-12 19:07

import datetime

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("profile", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(default="chat", max_length=50)),
                (
                    "profiles",
                    models.ManyToManyField(related_name="chats", to="profile.Profile"),
                ),
                (
                    "talker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profile.profile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=datetime.datetime.now)),
                ("content", models.TextField(default="content")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profile.profile",
                    ),
                ),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.chat"
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
    ]
