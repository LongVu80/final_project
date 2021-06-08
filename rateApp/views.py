from django.shortcuts import render, redirect
import requests
from .secret import API_KEY
from django.contrib import messages
from .models import * 
import bcrypt

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


def success(request):
    if 'user_id' in request.session:
        context = {
            'name' : User.objects.get(id=request.session['user_id']),
            'opinions' : Opinion.objects.all().order_by('-created_at')
        }
        return render(request, 'zipcode.html', context)
    return redirect ('/')

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
        # official = Official.objects.create(
        #     elected_office = 'elect_office',
        #     name = 'name',
        #     party = 'party'
        #         )
        # context = {
        #     "official": Official.objects.get()
        # }
        # request.session['official'] = official
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
    # official = Official.objects.get()
    # user_id = request.session['user_id']
    # comment = request.POST['comment']
    # reply = request.POST['message']
    # user = User.objects.get(id=user_id)
    # Reply.objects.create(reply=reply, user=user, official=official)
    # Comment.objects.create(comment = comment, user=user, official=official)
    # rating = request.POST['rating']
    # Rating.objects.create(rating=rating, user=user, official=official)
    return render(request, 'rate.html', context)

def rate(request):
    Rating.objects.create(
        rating = request.POST['rating'],
        user = User.objects.get(id=request.session['user_id'])
    )
    # official = Official.objects.get()
    # user_id = request.session['user_id']
    # comment = request.POST['comment']
    # reply = request.POST['message']
    # user = User.objects.get(id=user_id)
    # Reply.objects.create(reply=reply, user=user, official=official)
    # Comment.objects.create(comment = comment, user=user, official=official)
    # rating = request.POST['rating']
    # Rating.objects.create(rating=rating, user=user, official=official)
    return redirect('/rating/')

def opinion(request):
    Opinion.objects.create(
        opinion = request.POST['opinion'], 
        user = User.objects.get(id=request.session['user_id']))
    return redirect('rate/')

def reply(request):
    print(request.POST['opinion_id'])
    Reply.objects.create(
        reply = request.POST['reply'], 
        user = User.objects.get(id=request.session['user_id']), 
        opinion = Opinion.objects.get(id = request.POST['opinion_id'])
    )
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
