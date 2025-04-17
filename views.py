from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm, LoginForm
from myproject.settings import users_collection, survey_collection
from django.contrib.auth.hashers import make_password, check_password
from .surveyform import SurveyForm
# from django.conf import settings  # To access MONGO_COLLECTION
# from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .models import User
from .models import SurveyResponse
from django.conf import settings
from pymongo import MongoClient
from bson import ObjectId
from django.http import HttpResponseRedirect
from django.urls import reverse

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB_NAME = "mydatabase"
# LOGIN_REDIRECT_URL = '/dashboard/'

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
users_collection = db["users"]
survey_collection = db["surveyforms"]


def index(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        User.objects.create(name=name, email=email)
        return redirect('/')
    
    users = User.objects.all()
    return render(request, 'myapp/index.html', {'users': users})

def signup(request):
    print(type(request))  # See what type of object `request` is
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Check if user already exists
            if users_collection.find_one({"email": email}):
                messages.error(request, "Email already registered.")
                return redirect("signup")

            # Hash password
            hashed_password = make_password(password)

            # Save to MongoDB
            users_collection.insert_one({
                "username": username,
                "email": email,
                "password": hashed_password
            })

            messages.success(request, "Signup successful! Please login.")
            return redirect("login")

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})
def login(request):
    print(type(request))  # Debugging: Check the request type
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Fetch user from the database
            user = users_collection.find_one({"email": email})

            if user and check_password(password, user["password"]):  # Ensure password verification is correct
                messages.success(request, f"Welcome {user['username']}!")
                return redirect("surveyform")  # Redirect to the survey page instead of the dashboard
            else:
                messages.error(request, "Invalid credentials.")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

# View to display dashboard with DataTable
def dashboard(request):
    responses = list(survey_collection.find())
    # Convert ObjectId to string so it works in templates
    for res in responses:
        res['id'] = str(res['_id'])  # Rename _id to id
        del res['_id']  # Optionally, remove the original _id

    return render(request, "dashboard.html", {"responses": responses})

def surveyform(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print("✅ Cleaned Data to Insert:", data)

            # Insert into MongoDB
            try:
                insert_result = survey_collection.insert_one(data)
                print("✅ Inserted to MongoDB with ID:", insert_result.inserted_id)
            except Exception as e:
                print("❌ MongoDB insert failed:", e)

            # Save to database
            SurveyResponse.objects.create(
                first_name=data['first_name'],
                middle_name=data.get('middle_name', ''),
                last_name=data['last_name'],
                email=data['email'],
                country_code=data['country_code'],
                phone_number=data['phone_number'],
                gender=data['gender'],
                favorite_color=data['favorite_color'],
                favorite_fruit=data['favorite_fruit'],
                description=data['description']
            )
            return redirect('viewform')  # or wherever
        else:
            print("❌ Form is not valid:", form.errors)
    else:
        form = SurveyForm()

    return render(request, 'surveyform.html', {'form': form})

def success(request):
    return render(request, 'success.html')


# def index(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         email = request.POST['email']
#         User.objects.create(name=name, email=email)
#         return redirect('/')
    
#     users = User.objects.all()
#     return render(request, 'index.html')
# def base(request):
#     return render(request, 'base.html')

def datatab(request):
    responses = SurveyResponse.objects.all()
    return render(request, 'datatab.html', {'responses': responses})

def edit_response(request, response_id):
    response = survey_collection.find_one({'_id': ObjectId(response_id)})

    if not response:
        return redirect('dashboard')  # Handle invalid ID gracefully

    if request.method == "POST":
        updated_data = {
            'first_name': request.POST.get('first_name', ''),
            'middle_name': request.POST.get('middle_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'email': request.POST.get('email', ''),
            'country_code': request.POST.get('country_code', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'gender': request.POST.get('gender', ''),
            'favorite_color': request.POST.get('favorite_color', ''),
            'favorite_fruit': request.POST.getlist('favorite_fruit'),
            'description': request.POST.get('description', ''),
        }

        survey_collection.update_one({'_id': ObjectId(response_id)}, {'$set': updated_data})

        return redirect('dashboard')

    # If GET request, just render the form
    return render(request, 'edit.html', {'response': response})

def delete_response(request, response_id):
    survey_collection.delete_one({'_id': ObjectId(response_id)})
    return redirect('dashboard')

def viewform(request):
    responses = SurveyResponse.objects.all()
    return render(request, 'viewform.html', {'responses': responses})
