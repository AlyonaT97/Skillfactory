# Generated by Django 4.2.1 on 2023-08-13 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='posts',
            new_name='post_category',
        ),
    ]
