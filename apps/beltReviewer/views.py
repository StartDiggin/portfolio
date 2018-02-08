# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import User
from models import Book
from models import Review
from django.contrib import messages

# Create your views here.
#Route to main register/login page --> '/'
def dashboard(req):
    return render(req, 'beltReviewer/login.html')

#Route to home --> '/home'
def home(req):
    context={
    'curUser': req.session['first_name'],
    'users': User.objects.all(),
    'books': [],
    'otherBooks': []
    }
    books = Book.objects.all()
    books_len = len(books)
    for i in range(books_len - 3, books_len):
        context['books'].append(books[i])
    for i in range(0, books_len - 3 ):
        context['otherBooks'].append(books[i])
    return render(req, 'beltReviewer/home.html', context)

#Route to new book form --> '/new'
def new(req):
    context = {
    'authors': []
    }
    books = Book.objects.all()
    for book in books:
        context['authors'].append(book.author)
    return render(req, 'beltReviewer/new.html', context)


#Route to create a user --> '/register'
def register(req):
    results = User.objects.validate(req.POST)
    if results['status'] == True:
        user = User.objects.creator(req.POST)
        messages.success(req, 'User created')
        return redirect('/')
    else:
        for error in results['errors']:
            messages.error(req, error)
    return redirect('/')

#Route to login a user --> '/login'
def login(req):
    results = User.objects.loginValidation(req.POST)
    if results['status'] == False:
        messages.error(req, 'Check credentails!')
        return redirect('/')
    req.session['email'] = results['user'].email
    req.session['first_name'] = results['user'].first_name
    return redirect('/home')

#Route to create a book and book review --> '/create'
def create(req):
    user = User.objects.get(email = req.session['email'])
    book = Book.objects.create(title = req.POST['title'], author = req.POST['author'], rate = req.POST['rate'], user = user)
    book.save()
    bookReview = Review.objects.create(comment = req.POST['comment'], book = book, writer = user)
    id = str(book.id)
    return redirect('/review/'+id)

#Route to book reviews --> '/review'
def review(req, id):
    context = {
    'book': Book.objects.get(id=id),
    'allReviews': Review.objects.filter(book__id=id)
    }
    return render(req, 'beltReviewer/review.html', context)

#Route to add a review to a book --> '/addReview'
def addReview(req, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(email = req.session['email'])
    Review.objects.create(book=Book.objects.get(id=id), comment=req.POST['review'], writer = user)
    return redirect('/review/'+id)

#Route to user profile --> '/user'
def user(req, id):
    context = {
    'user': User.objects.get(id=id),
    'booksReviewed': Book.objects.filter(books__writer_id=id)
    }
    return render(req, 'beltReviewer/user.html', context)

#Route to registration and login --> '/logout'
def logout(req):
    req.session.flush()
    return redirect('/')

#Route to delete a user --> '/delete'
def delete(req, id):
    User.objects.get(id=id).delete()
    return redirect('/home')

#Route to delete a book --> '/deleteBook'
def deleteBook(req, id):
    Book.objects.get(id=id).delete()
    return redirect('/home')
