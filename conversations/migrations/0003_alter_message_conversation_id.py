# Generated by Django 5.1.6 on 2025-02-26 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0002_rename_type_message_direction_remove_conversation_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='conversation_id',
            field=models.CharField(max_length=36),
        ),
    ]
