from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import HttpResponse
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.


# def login(request):
#     if request.method == 'GET':
#         request.session['loginstatus'] = False
#         return render(request, 'loginpage/index.html')
#     else:
#         username = request.POST['username']
#         password = request.POST['pass']
#         if(username =="sayem" and password=='sayem'):
#             request.session['loginstatus'] = True
#             return render(request, 'adminpage/index.html')
#         else:
#             return render(request, 'loginpage/index.html', {"error": "*username or password is wrong"})


def loginuser(request):
    if request.method == 'GET':
        request.session["loginstatus"] = False
        return render(request, 'loginpage/index.html')
    else:
        user = authenticate(request, username=request.POST['name'], password=request.POST['password'])
        # print(user)
        if user is None:
            return render(request, 'loginpage/index.html', {"error": "*username or password is wrong"})
        else:
            request.session['loginstatus'] = True
            # login(request, user)
            data = {'name': user}
            print(str(user))
            request.session['username'] = str(user)
            return redirect('adminpage')
