# Generated by Django 4.2.4 on 2023-11-02 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0006_sentence_helptext_sentence_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentence',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('de', 'German')], default='en', max_length=2),
            preserve_default=False,
        ),
    ]
