from django.shortcuts import render
from .forms import MyForm
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def check_mongodb_connection():
    try:
        client = MongoClient(os.getenv('MONGODB_URI'))
        return client['django-mongo']
    except ConnectionFailure:
        return False


def index(request):
    """
    Handle the index view for processing form submissions.

    This view function handles both GET and POST requests. If the request method 
    is POST, it attempts to process the submitted form data. It validates the form 
    and prints debug information regarding the form's validity and any errors 
    encountered. If the form is valid, it prints the POST data. If the form is 
    invalid, it prints the form errors and specific error related to the 'dob' 
    field.

    For GET requests, it initializes an empty form for the user to fill out.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'index.html' template with the form context.
    """
    database = check_mongodb_connection()
    if database is False:
        return render(request, 'index.html', {'error': 'MongoDB connection failed'})

 
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():

            file = request.FILES['file']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            
            database['modelfield'].insert_one({
                "name" : request.POST.get('name'),
                "email" : request.POST.get('email'),
                "password" : request.POST.get('password'),
                "gender" : request.POST.get('gender'),
                "dob" : request.POST.get('dob'),
                "country" : request.POST.get('country'),
                "hobbies" : ",".join(request.POST.getlist('hobbies')),
                "message" : request.POST.get('message'),
                "file" : file_url,
            })
            form = MyForm()
            return render(request, 'index.html', {'form': MyForm()})
        else:
            form = MyForm(request.POST, request.FILES)
    else:
        form = MyForm()
    

    return render(request, 'index.html', {'form': form})