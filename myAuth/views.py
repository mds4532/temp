from django.shortcuts import render
from django.template import RequestContext, Template
from .forms import LoginForm, RegistrationForm
from django.http import HttpResponse, HttpResponseRedirect
import psycopg2
# from myAuth.models import User
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserUUID, Texts
from django.contrib.auth import logout
from datetime import datetime
# Create your views here.


def auth(request):

    s_uuid = None
    s_uuid = request.session.get('UUID')

    if s_uuid is None:
        if request.method == "POST":                    # Аутентификация
            login = request.POST.get("login")
            password = request.POST.get("password")

            user = authenticate(username=login, password=password)

            if user is not None:
                user_uuid = UserUUID.objects.get(user=user)
                request.session['UUID'] = user_uuid.uuid.hex    # Выдача UUID

                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("/?err=1")          # Неверный вход
        else:
            loginForm = LoginForm()
            return render(request, "auth/auth.html", {"form": loginForm})   # Вывод страницы аутентификации
    else:
        return HttpResponseRedirect("/")


def registration(request):
    if request.method == "POST":                            # Получение значений из POST
        login = request.POST.get("login")
        password = request.POST.get("password")
        email = request.POST.get("email")

        user = User.objects.create_user(login, email, password)

        user.save()                                         # Создание пользователя

        user_uiid = UserUUID()
        user_uiid.user = user
        user_uiid.uuid = uuid.uuid4()

        user_uiid.save()                                    # Создание UUID пользователю

        request.session["UUID"] = user_uiid.uuid.hex

        return HttpResponseRedirect('/')

    else:
        registrationForm = RegistrationForm()
        return render(request, "registration/registration.html", {"form": registrationForm})


def index(request):
    if request.POST:
        if 'account' in request.POST:
            return HttpResponseRedirect("account/")
    else:
        news = Texts.objects.all()
        data = {"news": news}
        return render(request, "index.html", context=data)
    

def editText(request, pk):

    s_uuid = request.session.get("UUID")

    if s_uuid is not None:
        text = Texts.objects.get(id=pk)
        if text is not None:
            if str(text.user_uuid.uuid.hex) == s_uuid:
                if request.POST:
                    nameText = request.POST["nameText"]
                    dataText = request.POST["dataText"]
                    text.name = nameText
                    text.text = dataText
                    text.date = datetime.now()
                    text.save()
                    return HttpResponseRedirect('/')
                else:
                    data = {"nameText": text.name, "dataText": text.text}
                    return render(request, "editable/editText.html", context=data)
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def createText(request):
    s_uuid = request.session.get("UUID")
    if s_uuid is not None:
        if request.POST:

            user = UserUUID.objects.get(uuid=s_uuid)
            nameText = request.POST["nameText"]
            dataText = request.POST["dataText"]

            Texts.objects.create(user_uuid=user, name=nameText, text=dataText, date=datetime.now())

            return HttpResponseRedirect('/')
        else:
            return render(request, "editable/editText.html")
    else:
        return HttpResponseRedirect('/')

def account(request):
    if request.POST:
        if 'exit_btn' in request.POST:
            del request.session["UUID"]
            return HttpResponseRedirect("/")
        elif 'create_btn' in request.POST:
            return HttpResponseRedirect("/editable")
    else:
        s_uuid = request.session.get("UUID")
        if s_uuid is None:
            return HttpResponseRedirect("/auth/")
        else:
            user = UserUUID.objects.get(uuid=s_uuid)
            texts = Texts.objects.filter(user_uuid=user)

            data = {"texts": texts, "s_uuid": s_uuid}

            return render(request, "editable/account.html", context=data)