from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import FileUploadForm
import os
import datetime
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import FileUploadForm
import os
import datetime
from django.utils import timezone
from django.urls import reverse
# from .data_processing import process_data
from django.conf import settings
# Create your views here.
from .models import FileUpload
from django.db import IntegrityError
from django.contrib import messages
import logging
from django.http import JsonResponse
log = logging.getLogger(__name__)
from .libs import process_data
from .models import Report
from django.http import HttpResponse, Http404


def report_catalog(request):
    return render(request, 'report/report_catalog.html')


def report_config(request):
    # print something to the console
    print('Hello, this is a test')
    return render(request, 'report/report_config.html')


def file_list(request):
    files = []
    file_uploads = FileUpload.objects.all()
    for file_upload in file_uploads:
        file_id = file_upload.id  # Add file_id
        file_name = file_upload.file_name
        file_path = file_upload.file_path
        file_size = file_upload.get_size_with_units()
        file_date = file_upload.uploaded_at.strftime("%Y-%m-%d %H:%M:%S")
        checksum = file_upload.checksum  # Add checksum column
        file_info = {
            'file_id': file_id,  # Include file_id in file_info dictionary
            'file_name': file_name,
            'file_path': file_path,
            'checksum': checksum,
            'file_size': file_size,
            'file_date': file_date,
        }
        files.append(file_info)
    
    return render(request, 'report/file_list.html', {'files': files})


def file_upload_view(request):
    if request.method == 'POST':
        files = {'file_path': request.FILES['file']}

        form = FileUploadForm(request.POST, files)
        if form.is_valid():
            try:
                file_upload = form.save()
                messages.success(request, 'File uploaded successfully.')
                # Process the uploaded file
                process_data(file_upload.file_path.path)
                # Redirect to the files_list URL
                return HttpResponseRedirect(reverse('files_list'))
            except IntegrityError:
                messages.error(request, 'File with this checksum already exists.')
        else:
            print(form.errors)
    else:
        form = FileUploadForm()
    return render(request, 'report/file_upload.html', {'form': form})


def delete_file(request, file_id):
    try:
        file_upload = FileUpload.objects.get(id=file_id)
        file_path = file_upload.file_path.path
        # Delete the file from the file system
        if os.path.exists(file_path):
            os.remove(file_path)
            log.info(f"File deleted: {file_path}")
        else:
            log.warning(f"File not found: {file_path}")
        # Delete the file from the database
        file_upload.delete()
        log.info("File record deleted from the database.")
        response = {'status': 'success', 'message': 'File deleted successfully.'}
        return JsonResponse(response, status=200)
    except FileUpload.DoesNotExist:
        logging.error("File not found.")
        response = {'status': 'error', 'message': 'File not found.'}
        return JsonResponse(response, status=404)
    
    
def report_catalog_view(request):
    # Use the manager method to get reports with size
    reports_with_size = Report.objects.get_all_reports_with_size()
    print('REPORTS WITH SIZE', reports_with_size)   
    return render(request, 'report/report_catalog.html', {'reports': reports_with_size})


def download_report(request, report_id):
    try:
        report = Report.objects.get(id=report_id)
        file_path = report.file_path  # Assuming `file_path` is the field storing the path

        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
                return response
        raise Http404
    except Report.DoesNotExist:
        raise Http404("Report does not exist")