# Generated by Django 5.0.6 on 2024-05-31 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_summary_user_alter_summary_youtube_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='сессия'),
        ),
    ]