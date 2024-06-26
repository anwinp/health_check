# Generated by Django 4.2.11 on 2024-04-07 18:13

from django.db import migrations, models
import report.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.FileField(upload_to=report.models.FileUpload.get_upload_path)),
                ('file_name', models.CharField(max_length=255)),
                ('checksum', models.CharField(max_length=32, unique=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('size', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('report_type', models.CharField(choices=[('pdf', 'PDF'), ('xlsx', 'Excel')], max_length=4)),
                ('file_path', models.CharField(max_length=255)),
                ('file_size', models.PositiveIntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
