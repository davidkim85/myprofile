# Generated by Django 4.1.7 on 2023-03-25 18:15

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment_author'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='comment',
            managers=[
                ('commented', django.db.models.manager.Manager()),
            ],
        ),
    ]
