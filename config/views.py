from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def custom_upload_function(request):
    # Assuming 'file' is the name of the form field
    file_data = request.FILES.get("upload")  # Get the file from the request

    if file_data is None:
        # Return a meaningful error if no file is uploaded
        return JsonResponse({"error": "No file uploaded"}, status=400)

    # Now, safe to access file_data.name since we know file_data is not None
    filename = file_data.name

    # Process the file here (e.g., save it, etc.)
    # For example, you could save the file to a model or file system

    return JsonResponse({"success": f"File {filename} uploaded successfully!"})
