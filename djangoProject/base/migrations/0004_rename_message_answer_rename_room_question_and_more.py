# Generated by Django 4.1.5 on 2023-01-22 13:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_message_topic_delete_user_room_host_message_room_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='Answer',
        ),
        migrations.RenameModel(
            old_name='Room',
            new_name='Question',
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='room',
            new_name='question',
        ),
    ]
