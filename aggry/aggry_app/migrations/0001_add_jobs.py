# Generated by Django 4.1.7 on 2023-03-07 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('job', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('mod_location', models.CharField(max_length=255)),
                ('price', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('agent', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
                ('label1', models.IntegerField(blank=True, null=True)),
                ('label2', models.IntegerField(blank=True, null=True)),
                ('data_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
