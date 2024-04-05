from django.db import models
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
    


