# Generated by Django 5.0.6 on 2024-05-23 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_alter_todo_options_alter_todo_content_tag_todo_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['-created_at']},
        ),
    ]
