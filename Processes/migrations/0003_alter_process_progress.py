# Generated by Django 3.2.6 on 2021-08-25 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Processes', '0002_alter_process_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='progress',
            field=models.CharField(choices=[('start', 'start'), ('extract', 'extract'), ('get_text', 'get_text'), ('summary', 'summary'), ('finished', 'finished'), ('summarized', 'summarized'), ('error', 'error'), ('corrected', 'corrected')], max_length=30),
        ),
    ]