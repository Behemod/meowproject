# Generated by Django 4.0.4 on 2022-05-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catprofile', '0004_signup'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
