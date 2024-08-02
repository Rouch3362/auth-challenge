# Generated by Django 5.0.7 on 2024-08-02 08:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_otp_userlockout_alter_user_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='otp',
            name='valid_until',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 2, 9, 10, 59, 912405, tzinfo=datetime.timezone.utc)),
        ),
    ]