# Generated by Django 4.2.4 on 2023-10-23 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0005_alter_sentence_translate'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentence',
            name='helpText',
            field=models.TextField(default='Нема'),
        ),
        migrations.AddField(
            model_name='sentence',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='sentence_photos/'),
        ),
    ]
