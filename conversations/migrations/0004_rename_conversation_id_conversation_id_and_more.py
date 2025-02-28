# Generated by Django 5.1.6 on 2025-02-27 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0003_alter_message_conversation_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversation',
            old_name='conversation_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='message',
            name='message_id',
        ),
        migrations.AddField(
            model_name='message',
            name='id',
            field=models.TextField(default='12345', primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
