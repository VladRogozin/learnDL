# Generated by Django 4.2.4 on 2023-10-29 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_savedpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='description',
            field=models.TextField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='description',
            field=models.TextField(default='', max_length=100, null=True),
        ),
    ]
