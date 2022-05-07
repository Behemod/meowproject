# Generated by Django 4.0.4 on 2022-05-01 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('message', 'Message'), ('follower', 'Follower'), ('like', 'Like'), ('mention', 'Mention')], max_length=20),
        ),
    ]