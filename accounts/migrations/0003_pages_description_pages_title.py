# Generated by Django 4.2.4 on 2023-10-27 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='description',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pages',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
