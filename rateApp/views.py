from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
import bcrypt
import requests
from .secret import API_KEY

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
    if 'user_id' not in request.session:
        messages.error(request, 'You need to be logged in to post a comment!!')
        return redirect('/')
    else:
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
        for i in offices:
            for j in i['officialIndices']:
                officials[j]['elected_office'] = i['name']
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
    'ratings': Rating.objects.all()
}

    return render(request, 'rate.html', context)

def addRate(request, name, elected_office):
    Rating.objects.create(
        rating = request.POST['rating'], 
        user = User.objects.get(id=request.session['user_id']))
    return redirect(f"/rate_official/{name}/{elected_office}".format(name = name, elected_office = elected_office))


def opinion_official(request, name, elected_office):
    print('User wants to rate', name, elected_office)
    context = {
        "official_name": name,
        "elected_office": elected_office,
        'opinions': Opinion.objects.all()
}
    return render(request, 'rate.html', context)

def addOpinion(request, name, elected_office):
    Opinion.objects.create(
        opinion = request.POST['opinion'], 
        user = User.objects.get(id=request.session['user_id']))
    return redirect(f"/rate_official/{name}/{elected_office}".format(name = name, elected_office = elected_office))


def editOpinion(request, message_id):
    opinionEd = Message.objects.get(id=message_id)
    context = {
        'editOpinion':opinionEd,
        'users': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'editOpinion.html', context)

def deleteOpinion(request, opinion_id):
    opinionDelete = Opinion.objects.get(id = opinion_id)
    if opinionDelete.user.id == request.session['user_id']:
        opinionDelete.delete()
        return redirect('/rate/')
    return redirect('/rate/')

def addReply(request, name, elected_office):
    Reply.objects.create(
        reply = request.POST['reply'],
        opinion = Message.objects.get(id = request.POST['opinion_id']),
        user = User.objects.get(id=request.session['user_id']))
    return redirect(f"/rate_official/{name}/{elected_office}".format(name = name, elected_office = elected_office))
# def addReply(request):
#     print(request.POST['opinion_id'])
#     if request.method == "POST":
#         opinion = request.POST['opinion'], 
#         reply = request.POST['reply'],
#         user = User.objects.get(id=request.session['user_id'])
#         Opinion.objects.create(opinion=opinion, reply=reply, user=user, name=name, elected_office=elected_office)
#         Reply.objects.create(opinion=opinion, reply=reply, user=user, name=name, elected_office=elected_office)
        
#     return redirect('/rate/')
def opinion_official(request, name, elected_office):
    print('User wants to rate', name, elected_office)
    context = {
    "official_name": name,
    "elected_office": elected_office,
    'opinions': Opinion.objects.all()
}
    return render(request, 'rate.html', context)

def deleteReply(request, reply_id):
    replyDelete = Reply.objects.get(id= reply_id)
    if replyDelete.user.id == request.session['user_id']:
        replyDelete.delete()
        return redirect('/rate/')
    return redirect('/rate/')

# def image_upload_view(request):
#     """Process images uploaded by users"""
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             # Get the current instance object to display in the template
#             img_obj = form.instance
#             return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
#     else:
#         form = ImageForm()
#     return render(request, '/success/', {'form': form})

def addMessage(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You need to be logged in to post a message')
        return redirect('/login/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
        }
        return render(request, 'daily.html', context)

def message(request):
    Message.objects.create(
        message = request.POST['message'], 
        user = User.objects.get(id=request.session['user_id']))
    return redirect('/success/')



def editMessage(request, message_id):
    messEd = Message.objects.get(id=message_id)
    context = {
        'editMessage':messEd,
        'users': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'editMessage.html', context)

def updateMessage(request, message_id):
    toUpdate = Message.objects.get(id=message_id)
    toUpdate.message = request.POST['message']
    #toUpdate.user_id = request.POST['user_id']
    toUpdate.save()

    return redirect('/success/')

def deleteMessage(request, message_id):
    delete = Message.objects.get(id=message_id)
    delete.delete()
    return redirect('/success/')


def like_message(request):
    user = request.session['user_id']
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        message_obj = Message.objects.get(id=message_id)

        if user in message_obj.likes.all():
            message_obj.likes.remove(user)
        else:
            message_obj.likes.add(user)

        like, created= Like.objects.get_or_create(user=user, id=message_id)

        if not created:

            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
    return redirect('/success/')

def addComment(request, message_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You need to be logged in to post a comment!!')
        return redirect('/login/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        theMess = Message.objects.get(id=message_id)
        comment = Comment.objects.all()
        context = {
            'theMess': theMess,
            'comment': comment,
            'user': user,
        }     
    return render(request, 'daily.html', context)

def comment(request):
    print(request.POST['message_id'])
    Comment.objects.create(
        comment = request.POST['comment'], 
        user = User.objects.get(id=request.session['user_id']), 
        message = Message.objects.get(id = request.POST['message_id'])
    )
    return redirect('/success/')

def editComment(request, comment_id):
    commEd = Comment.objects.get(id=comment_id)
    context = {
        'editComment':commEd,
        'users': User.objects.get(id=request.session['user_id']),
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

def like_comment(request):
    user = request.session['user_id']
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment_obj = Comment.objects.get(id=comment_id)

        if user in comment_obj.likes.all():
            comment_obj.likes.remove(user)
        else:
            comment_obj.likes.add(user)

        like, created = Like.objects.get_or_create(user=user, comment_id=comment_id)

        if not created:

            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
    return redirect('/success/')

def editUser(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user':user
    }
    return render(request, 'editUser.html', context)

def users(request):
    if 'user_id' not in request.session:
        return redirect('/login/')
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'users.html', context)

def editUser(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user,
    }
    return render(request, 'editUser.html', context)

def updateUser(request, user_id):
    update = User.objects.get(id=user_id)
    update.firstName = request.POST['firstName']
    update.lastName = request.POST['lastName']
    update.email = request.POST['email']
    update.username = request.POST['username']
    update.save()
    return redirect('/users/')

def deleteUser(request, user_id):
    delete = User.objects.get(id=user_id)
    delete.delete()

    return redirect('/')



