from django.db import models
import os
from uuid import uuid4
import hashlib

# Create your models here.
class FileUploadManager(models.Manager):
    def get_rows(self):
        return self.all()

class FileUpload(models.Model):
    def get_upload_path(instance, filename):
        # Optionally, use a UUID or similar strategy to ensure unique filenames
        # and avoid relying on `uploaded_at` for directory naming.
        uuid_name = uuid4()
        extension = os.path.splitext(filename)[1]
        file_name = os.path.splitext(filename)[0]
        return f"data/files/{file_name}_{uuid_name}{extension}"

    @staticmethod
    def calculate_checksum(file):
        # Calculate the checksum of the file
        hasher = hashlib.md5()
        for chunk in file.chunks():
            hasher.update(chunk)
        return hasher.hexdigest()

    file_path = models.FileField(upload_to=get_upload_path)
    file_name = models.CharField(max_length=255)
    checksum = models.CharField(max_length=32, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField(null=True)

    objects = FileUploadManager()

    def save(self, *args, **kwargs):
        print('file path', self.file_path)
        # Calculate and store the checksum before saving the file
        if not self.checksum:
            self.checksum = FileUpload.calculate_checksum(self.file_path)
        # Store the file size
        if not self.size:
            self.size = self.file_path.size
        
        # Set the file name
        if not self.file_name:
            self.file_name = os.path.basename(self.file_path.name)
        super().save(*args, **kwargs)

    def get_size_with_units(self):
        # Convert the size to human-readable units
        size = self.size
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        index = 0
        while size >= 1024 and index < len(units) - 1:
            size /= 1024
            index += 1
        return f"{size:.2f} {units[index]}"

    def __str__(self):
        return self.file_name
    


class ReportManager(models.Manager):
    def get_all_reports_with_size(self):
            # Get all reports with file size
        reports = self.get_queryset().all()
        reports_with_size = []
        for report in reports:
            report_with_size = {
                'title': report.title,
                'report_type': report.report_type,
                'file_path': report.file_path,
                'file_size': report.get_size_with_units(),
                'created_at': report.created_at,
                'report_id': report.id
            }
            reports_with_size.append(report_with_size)
        return reports_with_size

class Report(models.Model):
    REPORT_TYPES = (
        ('pdf', 'PDF'),
        ('xlsx', 'Excel'),
    )

    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=4, choices=REPORT_TYPES)
    file_path = models.CharField(max_length=255)  # Storing the path as a string
    file_size = models.PositiveIntegerField(null=True)  # Add file size field
    created_at = models.DateTimeField(auto_now_add=True)
   
    objects = ReportManager()

    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"

    def save(self, *args, **kwargs):
        # Calculate and store the file size before saving the report
        if not self.file_size:
            self.file_size = os.path.getsize(self.file_path)
        super().save(*args, **kwargs)
        
    def get_size_with_units(self):
        if self.file_size is None:
            return "Unknown size"
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0




