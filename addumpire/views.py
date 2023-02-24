from django.shortcuts import render, redirect
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.


def addumpire(request):
    if request.method == 'GET':
        if request.session['loginstatus']:
            cursor = connection.cursor()
            sql = "SELECT * FROM TEAM"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()

            team = []
            for r in result:
                team_id = r[0]
                team_name = r[1]

                row = {'team_id': team_id, 'team_name': team_name}
                team.append(row)
            return render(request, 'addumpire/index.html', {'team':team})
        else:
            return redirect('login')

    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        country = request.POST['nationality']
        bday = request.POST['phone_number']
        file = request.FILES['image']
        uid = country+"_"+last_name+"_"+bday
        print(first_name, last_name, country, bday)
        handle_uploaded_file(file)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO PERSON VALUES(:UmID,:FNAME,:LNAME,:uCOUNTRY,TO_DATE(:DOB,'YYYY-MM-DD'),:uIMAGE)", UmID=uid, FNAME=first_name, LNAME=last_name, uCOUNTRY=country, DOB=bday, uIMAGE=file.name)
        cursor.execute("INSERT INTO UMPIRE VALUES (:UmID,NULL)", UmID=uid)
        connection.commit()
        cursor.close()
        # return HttpResponse("File uploaded successfuly")
        return render(request, 'adminpage/index.html')


def handle_uploaded_file(f):
    with open('static/umpiresingle/images/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)