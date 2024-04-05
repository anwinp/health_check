
from django import forms
from .models import FileUpload
from django.forms import FileInput



class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('file_path',)
        widgets = {
            'file_path': FileInput(attrs={'name': 'file_path'}),
        }

    def is_valid(self):
        valid = super().is_valid()
        print('is valid', valid)
        if not valid:
            # Add custom error handling or logging here
            raise forms.ValidationError("Form is not valid")
        return valid