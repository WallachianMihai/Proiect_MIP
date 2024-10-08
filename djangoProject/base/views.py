import array

import django.http
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from .models import Question, Topic, Answer, Comment
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import QuestionForm
from django.template.defaulttags import register

def registerUser(request):
    page = 'register'
    context = {
        'page': page
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if password != re_password:
            messages.error(request, 'Passwords dont match')
        user = User.objects.create_user(username, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'base/login_register.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
    return render(request, 'base/login_register.html', {'page': page})

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    questions = Question.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    answers = Answer.objects.all().order_by('-created')
    context = {
        'questions': questions,
        'question_count': questions.count(),
        'topics': topics,
        'answers': answers,
    }
    return render(request, 'base/home.html', context)

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)

def question(request, pk):
    question = Question.objects.get(id=pk)
    answers = question.answer_set.all().order_by('-created')
    bestAnswer = Answer.objects.filter(bestAnswer=True, question=question)

    answers_comments = {}
    for answer in answers:
        answers_comments[answer.id] = answer.comment_set.all().order_by('created')

    context = {
        'question': question,
        'answers': answers,
        'answer_count': answers.count() if answers.count() != 0 else 0,
        'answers_comments': answers_comments,
        'bestAnswer': 0 if bestAnswer.count() == 0 else bestAnswer[0].id
    }

    if request.method == 'POST':
        if request.POST.get('answer_body') is None:
            comment = Comment.objects.create(
                user = request.user,
                answer = Answer.objects.get(id=request.POST.get('answer')),
                body = request.POST.get('comment_body')
            )
        else:
            answer = Answer.objects.create(
                user = request.user,
                question = question,
                body = request.POST.get('answer_body')
            )
        return redirect('question', pk=question.id)

    return render(request, 'base/question.html', context)


@login_required(login_url='login')
def createQuestion(request):
    topics = Topic.objects.all()
    print(request.path)

    if request.method == 'POST':
        topicName = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topicName)

        question = Question.objects.create(
            host=request.user,
            name=request.POST.get('question_name'),
            topic=topic,
            description=request.POST.get('description')
        )
        return redirect('home')

    context = {'topics': topics}
    return render(request, 'base/question_form.html', context)

@login_required(login_url='login')
def updateQuestion(request, pk):
    question = Question.objects.get(id=pk)
    topic = question.topic
    name = question.name
    description = question.description

    if request.user != question.host:
        return redirect('home')

    if request.method == 'POST':
        topicName = request.POST.get('topic')
        name = request.POST.get('question_name')
        description = request.POST.get('description')
        topic, created = Topic.objects.get_or_create(name=topicName)
        Question.objects.filter(id=pk).update(name=name, description=description, topic=topic)
        return redirect('home')

    context = {
        'topic': topic,
        'name': name,
        'description': description
    }
    return render(request, 'base/question_form.html', context)

@login_required(login_url='login')
def delete(request, pk):
    question = Question.objects.get(id=pk)

    if request.user != question.host:
        return redirect('home')

    if request.method == 'POST':
        question.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': question})

@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return redirect('home')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': comment})

@login_required(login_url='login')
def deleteAnswer(request, pk):
    answer = Answer.objects.get(id=pk)

    if request.user != answer.user:
        return redirect('home')

    if request.method == 'POST':
        answer.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': answer})

@login_required(login_url='login')
def likeAnswer(request, pk):
    answer = Answer.objects.get(id=pk)
    likes = answer.likes + 1
    Answer.objects.filter(id=pk).update(likes=likes)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def dislikeAnswer(request, pk):
    answer = Answer.objects.get(id=pk)
    likes = answer.likes - 1
    Answer.objects.filter(id=pk).update(likes=likes)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def markAnswer(request, pk):
    answer = Answer.objects.get(id=pk)
    bestAnswer = answer.bestAnswer
    Answer.objects.filter(id=pk).update(bestAnswer=(not bestAnswer))
    return redirect(request.META.get('HTTP_REFERER'))