# Generated by Django 4.2.4 on 2023-11-01 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basegamemodel',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('de', 'German')], default='en', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='basegamemodel',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='baseGame_photos/'),
        ),
    ]