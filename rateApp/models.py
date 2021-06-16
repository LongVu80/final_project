from django.db import models
import re
import datetime
import os

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['firstName']) < 2:
            error['firstName'] = "First Name must be at least 2 characters"

        if len(form['lastName']) < 2:
            error['lastName'] = "Last Name must be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Format'

        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email addres is already in use'

        usernameCheck = self.filter(username=form['username'])
        if usernameCheck:
            errors['username'] ='Sorry that username has been taken please chose a different one'

        if len(form['password']) < 5:
            errors['password'] = 'Password must be at least 5 characters long'
        
        if form['password'] != form['confirm']:
            errors['password'] = 'Password do not match'

        return errors

def filepath(request, filename):
    old_filename=filename
    timeNow =datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

class User(models.Model):
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__ (self):
        return f"{self.username}"


class Opinion(models.Model):
    opinion = models.TextField()
    elected_office = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    user = models.ForeignKey(User, related_name="opinions", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reply(models.Model):
    reply = models.TextField()
    elected_office = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    user = models.ForeignKey(User, related_name="userReply", on_delete = models.CASCADE)
    opinion = models.ForeignKey(Opinion, related_name="replies", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Official(models.Model):
#     elected_office = models.CharField(max_length=255)
#     name = models.CharField(max_length=45)
#     state = models.CharField(max_length=45)
#     party = models.CharField(max_length=45)
#     website = models.CharField(max_length=255)
#     socialNetwork = models.CharField(max_length=255)
#     def __str__(self):
#         return f"{self.name} {self.party}"

class RatingManager(models.Manager):
    def validate_oneUser_oneOfficial(self, user, official):
        for i in user.ratings.all():
            if i.official.office == official.office:
                print ("Get here!")
                return False
        return True


class Rating(models.Model):
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    elected_office = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = RatingManager()


class Message(models.Model):
    message = models.TextField()
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
    user = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='user_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment = models.TextField()
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
    user_likes = models.ManyToManyField(User, related_name='comment_likes')
    user = models.ForeignKey(User, related_name="users", on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

