# Generated by Django 4.1.7 on 2023-03-31 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_remove_visitor_host'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='body',
            new_name='message',
        ),
    ]
