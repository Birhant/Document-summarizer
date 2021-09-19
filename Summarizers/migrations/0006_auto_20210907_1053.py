# Generated by Django 3.2.6 on 2021-09-07 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Summarizers', '0005_pickledmodel_args'),
    ]

    operations = [
        migrations.CreateModel(
            name='summarize_input',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('input', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='summary_output',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='pickledmodel',
            name='args',
            field=models.CharField(default='0000', max_length=100, null=True),
        ),
    ]