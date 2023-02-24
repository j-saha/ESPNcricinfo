from django.shortcuts import render, redirect
import cx_Oracle
import datetime
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.


def addseries(request):
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

            cursor = connection.cursor()
            sql = "SELECT * FROM PLAYER PR, PERSON P WHERE P.PERSON_ID=PR.PLAYER_ID"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            fullname = ""
            player = []
            for r in result:
                player_id = r[4]
                first_name = r[5]
                second_name = r[6]
                fullname = first_name + " " + second_name

                row = {'player_id': player_id, 'fullname': fullname}
                player.append(row)
            return render(request, 'addseries/index.html', {'team':team, 'player':player})
        else:
            return redirect('login')
    else:
        name = request.POST['name']

        winner = request.POST['winner']
        mots = request.POST['motm']
        team1= request.POST['team1']
        team2 = request.POST['team2']
        team3 = request.POST['team3']
        team4 = request.POST['team4']
        part = mots.split(" ")
        first_name = part[0]
        last_name = part[1]
        start_date=request.POST['start_date']
        end_date = request.POST['end_date']
        s_id=str(team1)+str(team2)+str(team3)+str(team4)+str(start_date)
        print(mots)
        file = request.FILES['image']

        cursor = connection.cursor()
        sql = "SELECT TEAM_ID FROM TEAM WHERE NAME = '" + team1 + "'"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        team1_id = ""
        for r in result:
            team1_id = r[0]
        cursor = connection.cursor()
        sql = "SELECT TEAM_ID FROM TEAM WHERE NAME = '" + team2 + "'"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        team2_id = ""
        for r in result:
            team2_id = r[0]

        if team3!="":
            cursor = connection.cursor()
            sql = "SELECT TEAM_ID FROM TEAM WHERE NAME = '" + team3 + "'"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            team3_id = ""
            for r in result:
                team3_id = r[0]
        if team4!="":
            cursor = connection.cursor()
            sql = "SELECT TEAM_ID FROM TEAM WHERE NAME = '" + team4 + "'"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            team4_id = ""
            for r in result:
                team4_id = r[0]


        cursor = connection.cursor()
        sql = "SELECT PERSON_ID FROM PERSON WHERE FIRST_NAME = '" + first_name + "' AND LAST_NAME='"+last_name+"'"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        mots_id=""

        for r in result:
            mots_id = r[0]


        handle_uploaded_file(file)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO SERIES VALUES(:S_ID,:S_NAME,:S_HOST,:S_MOTS,:S_WINNER,:S_IMAGE)",
                S_ID=s_id, S_NAME=name, S_HOST=team1, S_MOTS=mots_id, S_WINNER=winner, S_IMAGE=file.name)

        cursor.execute(
            "INSERT INTO TEAM_SERIES VALUES(:T_ID,:S_ID,TO_DATE(:S_DATE,'YYYY-MM-DD'),TO_DATE(:E_DATE,'YYYY-MM-DD'))",
            T_ID=team1_id, S_ID=s_id, S_DATE=start_date, E_DATE=end_date)
        cursor.execute(
            "INSERT INTO TEAM_SERIES VALUES(:T_ID,:S_ID,TO_DATE(:S_DATE,'YYYY-MM-DD'),TO_DATE(:E_DATE,'YYYY-MM-DD'))",
            T_ID=team2_id, S_ID=s_id, S_DATE=start_date, E_DATE=end_date)
        if team3 != "":
            cursor.execute(
                "INSERT INTO TEAM_SERIES VALUES(:T_ID,:S_ID,TO_DATE(:S_DATE,'YYYY-MM-DD'),TO_DATE(:E_DATE,'YYYY-MM-DD'))",
                T_ID=team3_id, S_ID=s_id, S_DATE=start_date, E_DATE=end_date)
        if team4 != "":
            cursor.execute(
                "INSERT INTO TEAM_SERIES VALUES(:T_ID,:S_ID,TO_DATE(:S_DATE,'YYYY-MM-DD'),TO_DATE(:E_DATE,'YYYY-MM-DD'))",
                T_ID=team4_id, S_ID=s_id, S_DATE=start_date, E_DATE=end_date)
        cursor.execute("INSERT INTO SERIES_PARTICIPANTS VALUES(:T_ID,:S_ID)",
                       T_ID=team1_id, S_ID=s_id)
        cursor.execute("INSERT INTO SERIES_PARTICIPANTS VALUES(:T_ID,:S_ID)",
                       T_ID=team2_id, S_ID=s_id)
        if team3 != "":
            cursor.execute("INSERT INTO SERIES_PARTICIPANTS VALUES(:T_ID,:S_ID)",
                           T_ID=team3_id, S_ID=s_id)
        if team4 != "":
            cursor.execute("INSERT INTO SERIES_PARTICIPANTS VALUES(:T_ID,:S_ID)",
                           T_ID=team4_id, S_ID=s_id)






        connection.commit()
        cursor.close()

        # return HttpResponse("File uploaded successfuly")
        return render(request, 'adminpage/index.html')


def handle_uploaded_file(f):
    with open('static/homepage/img/speakers/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)