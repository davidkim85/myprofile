# Generated by Django 4.1.7 on 2023-03-29 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_comment_managers_rename_processor_visitor_host_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitor',
            name='host',
        ),
    ]
