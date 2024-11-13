from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from config.settings.s3_client import s3_client


@csrf_exempt
def custom_upload_function(request):
    file_data = request.FILES.get("upload")
    if file_data is None:
        return JsonResponse({"error": "No file uploaded"}, status=400)
    filename = file_data.name
    return JsonResponse({"success": f"File {filename} uploaded successfully!"})


@login_required
def serve_s3_file(request, file_key):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    try:
        # Get the file from S3
        file_obj = s3_client.get_object(Bucket=bucket_name, Key=f"media/{file_key}")
        # Get the file content and content type
        file_content = file_obj["Body"].read()
        content_type = file_obj["ContentType"]
        # Create an HTTP response to serve the file
        response = HttpResponse(file_content, content_type=content_type)
        response["Content-Disposition"] = (
            f'attachment; filename={file_key.split("/")[-1]}'
        )
        return response  # noqa: TRY300
    except s3_client.exceptions.NoSuchKey:
        return HttpResponse(f"Error: File not found with key {file_key}", status=404)
    except Exception as e:  # noqa: BLE001
        return HttpResponse(f"Error: {e!s}", status=500)
