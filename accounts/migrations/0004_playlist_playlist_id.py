# Generated by Django 4.2.4 on 2023-10-07 17:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_playlistitem_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='playlist_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]