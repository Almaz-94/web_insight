# Generated by Django 5.0.6 on 2024-06-04 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_summary_session_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='script',
            field=models.CharField(choices=[(1, 'Assistant One'), (2, 'Assistant Two')], max_length=40, verbose_name='сценарий обработки'),
        ),
    ]
