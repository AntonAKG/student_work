# Generated by Django 5.1.1 on 2024-10-29 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('save_work', '0003_alter_studentwork_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='URL'),
        ),
    ]
