from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
import requests
from .secret import API_KEY
# from django.contrib.auth import authenticate,login, logout
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .forms import UserRegistrationForm
# from django.contrib.auth.models import User
# from django.views.decorators.csrf import csrf_exempt
# from .forms import ImageForm




# def profile(request):
#     if request.user.is_authenticated:
#         return render(request, 'profile.html')
#     else:
#         return redirect('/signin/')

# def signup(request):

#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)

#         if form.is_valid():
#             form.save()

            
#             return redirect('/signin/')
        
#     else:
#         form = UserRegistrationForm()
#     return render(request,'signup.html',{'form':form})

# def signin(request):
#     if request.user.is_authenticated:
#         return redirect('/')
     
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username =username, password = password)
 
#         if user is not None:
#             login(request,user)
#             request.session['user_id'] = userLogin.id
#             return redirect('/')
#         else:
#             form = AuthenticationForm()
#             return render(request,'signin.html',{'form':form})
     
#     else:
#         form = AuthenticationForm()
#         return render(request, 'signin.html', {'form':form})

# def signout(request):
#     logout(request)
#     return redirect('/signin/')

# def delete(request):
#     return render(request, 'delete.html')


# @csrf_exempt
# def delete_user(request, username):
    
#     if request.method == 'POST':
#         try:
#             user = User.objects.get(username=username)
#             user.delete()
#             return HttpResponse('Bye bye')
#         except Exception as e: 
#             return HttpResponse('Something went wrong!')
#     return redirect('/')

def index(request):
    return render(request, 'index.html')

def login(request):
    user = User.objects.filter(username = request.POST['username'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            messages.success(request, "you have successfully logged in!!")
            return redirect('/success/')
        messages.error(request, 'Invalid Username or Password!')
        return redirect ('/')
    messages.error(request, 'That username is not in our system, please check the spelling or register for an account.')
    return redirect('/')


def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect ('/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        email = request.POST['email'],
        username = request.POST['username'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    return redirect('/success/')


def logout(request):
    request.session.clear()
    return redirect ('/')

def daily(request):
    return render(request, ('daily.html'))

def success(request):
    
    if 'user_id' in request.session:
        context = {
            'name' : User.objects.get(id=request.session['user_id']),
            'messages' : Message.objects.all().order_by('-created_at'),
            'opinions' : Opinion.objects.all().order_by('-created_at'),
        }
        return render(request, 'daily.html', context)
    return redirect ('/')

def zipcode(request):
    return render(request, 'zipcode.html')




def view_officials(request):
    if request.method == "POST":
        zipcode = request.POST['zipcode']
        response = requests.get(f"https://www.googleapis.com/civicinfo/v2/representatives?key={API_KEY}&address={zipcode}&includeOffices=true")
        json = response.json()
        offices = json['offices']
        officials = json['officials']
    # add elected office to officials
        for i in offices:
            for j in i['officialIndices']:
                officials[j]['elected_office'] = i['name']
                # officials[j]['photo']= officials['photoUrl']
        context = {
            "officials": officials
        }
        request.session['officials'] = officials
        return redirect('/show_officials/', context)


def show_officials(request):
    context = {
        "officials": request.session['officials']
    }
    return render(request, 'officials.html', context)

def rate_official(request, name, elected_office):
    print('User wants to rate', name, elected_office)
    context = {
    "official_name": name,
    "elected_office": elected_office,
}

    return render(request, 'rate.html', context)



def addRate(request, name, elected_office):
    # if request.method == "POST":
    #     user_id = request.session['user_id']
    #     user = User.objects.get(id=user_id)
    #     rating = request.POST['rating']
    #     Rating.objects.create(rating=rating, user=user, name=name, elected_office=elected_office)
        
    # return redirect(f"/rate_official/{name}/{elected_office}".format(name = name, elected_office = elected_office))
    
    context={
        'ratings' : Rating.objects.create(
        rating = request.POST['rating'], 
        user = User.objects.get(id=request.session['user_id']))
    }
    return redirect(f"/rate_official/{name}/{elected_office}".format(name = name, elected_office = elected_office), context)



def addOpinion(request, name, elected_office):
    if request.method == "POST":
        opinion = request.POST['opinion'], 
        reply = request.POST['reply'],
        user = User.objects.get(id=request.session['user_id'])
        Opinion.objects.create(opinion=opinion, reply=reply, user=user, name=name, elected_office=elected_office)
        # Reply.objects.create(opinion=opinion, reply=reply, user=user, name=name, elected_office=elected_office)
        
    return redirect(f"/rate_official/{name}/{elected_office}".format(name = name, elected_office = elected_office))

def addReply(request):
    print(request.POST['opinion_id'])
    if request.method == "POST":
        opinion = request.POST['opinion'], 
        reply = request.POST['reply'],
        user = User.objects.get(id=request.session['user_id'])
        Opinion.objects.create(opinion=opinion, reply=reply, user=user, name=name, elected_office=elected_office)
        Reply.objects.create(opinion=opinion, reply=reply, user=user, name=name, elected_office=elected_office)
        
    return redirect('/rate/')

def deleteOpinion(request, opinion_id):
    opinionDelete = Opinion.objects.get(id = opinion_id)
    if opinionDelete.user.id == request.session['user_id']:
        opinionDelete.delete()
        return redirect('/rate/')
    return redirect('/rate/')

def deleteReply(request, reply_id):
    replyDelete = Reply.objects.get(id= reply_id)
    if replyDelete.user.id == request.session['user_id']:
        replyDelete.delete()
        return redirect('/rate/')
    return redirect('/rate/')

# Create your views here.

def profile(request):
    return render(request, ('profile.html'))

def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, '/success/', {'form': form})

def message(request):
    Message.objects.create(
        message = request.POST['message'], 
        user = User.objects.get(id=request.session['user_id']))
    return redirect('/success/')

def comment(request):
    print(request.POST['message_id'])
    Comment.objects.create(
        comment = request.POST['comment'], 
        user = User.objects.get(id=request.session['user_id']), 
        message = Message.objects.get(id = request.POST['message_id'])
    )
    return redirect('/success/')

def editMessage(request, message_id):
    messEd = Message.objects.get(id=message_id)
    context = {
        'editMessage':messEd,
        'users': User.objects.all().values(),
    }
    return render(request, 'editMessage.html', context)

def updateMessage(request, message_id):
    toUpdate = Message.objects.get(id=message_id)
    toUpdate.message = request.POST['message']
    #toUpdate.user_id = request.POST['user_id']
    toUpdate.save()

    return redirect('/success/')

def deleteMessage(request, message_id):
    messageDelete = Message.objects.get(id = message_id)
    if messageDelete.user.id == request.session['user_id']:
        messageDelete.delete()
        return redirect('/success/')
    return redirect('/success/')

def editComment(request, comment_id):
    commEd = Comment.objects.get(id=comment_id)
    context = {
        'editComment':commEd,
        'users': User.objects.all().values(),
    }
    return render(request, 'editComment.html', context)

def updateComment(request, comment_id):
    toUpdate = Comment.objects.get(id=comment_id)
    toUpdate.comment = request.POST['comment']
    #toUpdate.user_id = request.POST['user_id']
    toUpdate.save()

    return redirect('/success/')

def deleteComment(request, comment_id):
    commentDelete = Comment.objects.get(id= comment_id)
    if commentDelete.user.id == request.session['user_id']:
        commentDelete.delete()
        return redirect('/success/')
    return redirect('/success/')


def delUser(self):
    User.objects.all().delete()

# def delUser(request, user_id):
#     toDelete = User.objects.get(id=user_id)
#     toDelete.delete()

#     return redirect('/')

def updateUser(request, user_id):
    toUpdate = User.objects.get(id=user_id)
    toUpdate.firstName = request.POST['firstName']
    toUpdate.lastName = request.POST['lastName']
    toUpdate.email = request.POST['email']
    toUpdate.username = request.POST['username']
    toUpdate.acct_id = request.POST['acct_id']
    toUpdate.save()
    return redirect(f'/users/{user_id}/editUser/')
    
def editUser(request, user_id):
    oneUser = User.objects.get(id=user_id)
    context = {
        'editUser': oneUser,
    }
    return render(request, 'editUser.html', context)