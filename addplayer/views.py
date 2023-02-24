from django.shortcuts import render, redirect
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.


def addplayer(request):
    if request.method == 'GET':
        if request.session['loginstatus']:
            return render(request, 'addplayer/index.html')
        else:
            return redirect('login')

    else:
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        country = request.POST['company']
        ROLE = request.POST['ROLE']
        bat_style = request.POST['bat_style']
        bowl_style = request.POST['bowl_style']
        dob = request.POST['phone_number']
        uid = country + "_" + lname + "_" + dob
        file = request.FILES['image']
        print(fname, lname,country,dob, file.name)
        print(ROLE,bat_style, bowl_style)
        handle_uploaded_file(file)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO PERSON VALUES(:UmID,:FNAME,:LNAME,:uCOUNTRY,TO_DATE(:DOB,'YYYY-MM-DD'),:uIMAGE)", UmID=uid, FNAME=fname, LNAME=lname, uCOUNTRY=country, DOB=dob, uIMAGE=file.name)
        cursor.execute("INSERT INTO PLAYER VALUES(:PlID,:PROLE,:BAT_STYLE,:BOWL_STYLE)", PlID=uid, PROLE=ROLE, BAT_STYLE=bat_style, BOWL_STYLE=bowl_style)
        connection.commit()
        cursor.close()
        # return HttpResponse("File uploaded successfuly")
        return render(request, 'adminpage/index.html')


def handle_uploaded_file(f):
    with open('static/playersingle/images/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)