from django.shortcuts import render
from .forms import MyForm
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from django.shortcuts import redirect
from bson.objectid import ObjectId
import os
import math
from django.contrib import messages


def check_mongodb_connection():
    """
    Checks the connection to the MongoDB database.

    This function attempts to establish a connection to the MongoDB database using the URI specified in the `MONGODB_URI` environment variable. If the connection is successful, it returns the MongoDB database object named 'django-mongo'. If the connection fails, it returns False.

    Returns:
        - The MongoDB database object named 'django-mongo' if the connection is successful.
        - False if the connection fails.
    """
    try:
        client = MongoClient(os.getenv('MONGODB_URI'))
        return client['django-mongo']
    except ConnectionFailure:
        return False


def index(request):
    """
    Handles the index page request.

    This function is responsible for handling the index page request in the Django application. It takes a request object as a parameter.

    Parameters:
        - request: The HTTP request object.

    Returns:
        - If the request method is GET, it checks the MongoDB connection. If the connection fails, it renders the 'index.html' template with an error message. If the connection is successful, it retrieves the page number from the request query parameters and calls the 'pagination' function to get the page object. If the page object is not a dictionary, it redirects to the 'index' page. Finally, it renders the 'list-data.html' template with the page object as the context.
        - If the request method is not GET, it renders the 'list-data.html' template.

    """
    
    if request.method == "GET"  :
        database = check_mongodb_connection()
        if database is False:
            return render(request, 'index.html', {'error': 'MongoDB connection failed'})

        page_number = int(request.GET.get('page', 1))
        page_obj = pagination(database['modelfield'], page_number)
        if type(page_obj) != dict:
            return redirect("index")

        return render(request, 'list-data.html', {'page_obj' : page_obj})

    return render(request, 'list-data.html')



def pagination(table, curent_page):
    """
    Paginates a table of documents based on the current page.

    Args:
        table (pymongo.collection.Collection): The table to paginate.
        curent_page (int): The current page number.

    Returns:
        dict: A dictionary containing the paginated data, including the following keys:
            - 'data' (list): A list of documents for the current page.
            - 'prev_page' (int): The previous page number.
            - 'next_page' (int): The next page number.
            - 'curent_page' (int): The current page number.
            - 'total_pages' (int): The total number of pages.
            - 'total_documents' (int): The total number of documents.

    If the current page is greater than the total number of pages, an empty dictionary is returned.
    """
    # Define the number of items per page
    items_per_page = 10
    
    # Count the total number of documents
    total_documents = table.count_documents({})
    total_pages = math.ceil(total_documents / items_per_page)

    if curent_page > total_pages :
        return {'data': [], 'prev_page':0, 'next_page': 0, 'curent_page': 0, 'total_pages': 0, 'total_documents': 0}
    
    # Calculate the number of items to skip
    skip_items = (curent_page - 1) * items_per_page

    # Retrieve the documents for the current page
    documents = table.find().skip(skip_items).limit(items_per_page)
    prev_page = curent_page - 1
    if prev_page == 0:
        prev_page = 1

    next_page = curent_page + 1
    if next_page > total_pages:
        next_page = curent_page
    new_doc_list = []
    for i in documents:
        i["id"] = str(i["_id"])
        del i["_id"]
        new_doc_list.append(i)
    return {'data': new_doc_list, 'prev_page':prev_page, 'next_page':next_page, 'curent_page':curent_page, 'total_pages':total_pages, 'total_documents': total_documents}

def editTable(request, id=id):
    """
    Updates a table in the database with the data from the request form.

    Args:
        request (HttpRequest): The HTTP request object.
        id (str): The ID of the document to be updated.

    Returns:
        HttpResponse: The HTTP response object. If the MongoDB connection fails,
        it returns a rendered 'index.html' template with an error message. If the
        request method is 'POST' and the form data is valid, it updates the document
        with the given ID in the 'modelfield' collection and redirects to the 'index'
        page. If the request method is 'GET', it retrieves the document with the
        given ID from the 'modelfield' collection and populates the form with its data.
        It then returns a rendered 'index.html' template with the populated form.
    """
    database = check_mongodb_connection()
    if database is False:
        return render(request, 'index.html', {'error': 'MongoDB connection failed'})

 
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():

            database['modelfield'].update_one({
                    "_id": ObjectId(id)
                },
                {'$set' : {
                    "name" : request.POST.get('name'),
                    "email" : request.POST.get('email'),
                    "gender" : request.POST.get('gender'),
                    "dob" : request.POST.get('dob'),
                    "country" : request.POST.get('country'),
                    "hobbies" : ",".join(request.POST.getlist('hobbies')),
                    "message" : request.POST.get('message'),
                }
            })
            
            return redirect("index")
        else:
            form = MyForm(request.POST)
    else:
        
        data = database['modelfield'].find_one({"_id": ObjectId(id)})
        data["hobbies"] = data["hobbies"].split(",")
        form = MyForm(data)

    return render(request, 'index.html', {'form': form})


def deleteRecord(request, id=id):
    """
    Deletes a record from the 'modelfield' collection in the MongoDB database.

    Args:
        request (HttpRequest): The HTTP request object.
        id (str): The ID of the document to be deleted.

    Returns:
        HttpResponse: The HTTP response object. If the MongoDB connection fails,
        it returns a rendered 'index.html' template with an error message. If the
        document with the given ID is deleted successfully, it redirects to the
        'index' page. Otherwise, it redirects to the 'index' page.
    """
    database = check_mongodb_connection()
    if database is False:
        return render(request, 'index.html', {'error': 'MongoDB connection failed'})

    res = database['modelfield'].delete_one({ "_id": ObjectId(id) })
    if res.deleted_count > 0:
        return redirect("index")
    
    return redirect("index")



def addTable(request):
    """
    Adds a new record to the 'modelfield' collection in the MongoDB database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object. If the MongoDB connection fails,
        it returns a rendered 'index.html' template with an error message. If the
        request method is 'POST' and the form data is valid, it inserts a new document
        into the 'modelfield' collection and redirects to the 'index' page. If the
        request method is 'GET', it returns a rendered 'index.html' template with an
        empty form.
    """
   
    database = check_mongodb_connection()
    if database is False:
        return render(request, 'index.html', {'error': 'MongoDB connection failed'})

 
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():

            database['modelfield'].insert_one({
                "name" : request.POST.get('name'),
                "email" : request.POST.get('email'),
                "gender" : request.POST.get('gender'),
                "dob" : request.POST.get('dob'),
                "country" : request.POST.get('country'),
                "hobbies" : ",".join(request.POST.getlist('hobbies')),
                "message" : request.POST.get('message'),
            })
            # form = MyForm()
            # return render(request, 'index.html', {'form': MyForm()})
            return redirect("index")
        else:
            form = MyForm(request.POST)
    else:
        form = MyForm()
    

    return render(request, 'index.html', {'form': form})


