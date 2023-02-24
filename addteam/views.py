from django.shortcuts import render, redirect
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.


def addteam(request):
    # return render(request, 'addteam/index.html')
    if request.method == 'GET':
        if request.session['loginstatus']:
            return render(request, 'addteam/index.html')
        else:
            return redirect('login')
    else:
        name = request.POST['full_name']
        short_name = request.POST['short_name']
        file = request.FILES['file_image']
        fname = file.name
        print(file.name)
        handle_uploaded_file(file)
        cursor = connection.cursor()
        # sql ="INSERT INTO TEAM VALUES(TEAM_ID=:tid,NAME=:tname,IMAGE=:timage);"
        cursor.execute("INSERT INTO TEAM VALUES(:tid,:tname,:timage)", tid=short_name, tname=name, timage=fname)
        connection.commit()
        cursor.close()
        # return HttpResponse("File uploaded successfuly")
        return render(request, 'adminpage/index.html')


def handle_uploaded_file(f):
    with open('static/homepage/img/speakers/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)