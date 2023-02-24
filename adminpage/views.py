from django.shortcuts import render, redirect, HttpResponse
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)

# Create your views here.


def adminpage(request):
    print(str(request.session['loginstatus']))
    if request.session['loginstatus']:
        #name=request.user.first_name
        name = request.session['username']
        print(name)
        return render(request, 'adminpage/index.html', {'name': name})
    else:
        return redirect('login')
