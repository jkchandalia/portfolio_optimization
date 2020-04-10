import bcrypt

from apps.login_app.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse


# Create your views here.
def index(request):
    return redirect("/portfolio/index")

def main_login(request):
    return render(request, 'login_app/index.html')

def register(request):

    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/main_login')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # create the hash    
        check_existing_email = User.objects.filter(email=request.POST['email'])
        #if not(check_existing_email):
        #    messages.error(request, "The given email already has an account")
        #    return redirect("/")
        #else:
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash) 
        logged_user = User.objects.get(email=request.POST['email'])
        request.session['userid'] = logged_user.id
        request.session['logged_in'] = True
        request.session['first_name'] = request.POST['first_name']
        return redirect("/success")

def login(request):
    # see if the username provided exists in the database
    user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
    if user: # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0] 
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            # if we get True after checking the password, we may put the user id in session
            request.session['userid'] = logged_user.id
            request.session['logged_in'] = True
            request.session['first_name'] = logged_user.first_name
            # never render on a post, always redirect!
            return redirect('/success')
        else:
            messages.error(request, "Password is not correct")
            return redirect("/main_login")
    # if we didn't find anything in the database by searching by username or if the passwords don't match, 
    # redirect back to a safe route
    else:
        print('no email')
        messages.error(request, "The email was not found")
        return redirect("/main_login")

def success(request):
    if 'logged_in' in request.session:
        logged_user = User.objects.get(id=request.session['userid'])
        context = {
            'first_name': logged_user.first_name
        }
        return redirect("/portfolio/main")
    else:
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")
