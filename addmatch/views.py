from django.shortcuts import render, redirect
import csv, io
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.


def addmatch(request):
    if request.method == 'GET':
        if request.session['loginstatus']:

            cursor = connection.cursor()
            sql = "SELECT * FROM PLAYER PR, PERSON P WHERE P.PERSON_ID=PR.PLAYER_ID"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            fullname=""
            player = []
            for r in result:
                player_id=r[4]
                first_name = r[5]
                second_name = r[6]
                fullname=first_name+" "+second_name

                row = {'player_id': player_id, 'fullname': fullname}
                player.append(row)
            cursor = connection.cursor()
            sql = "SELECT * FROM UMPIRE U, PERSON P WHERE P.PERSON_ID=U.UMPIRE_ID"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()

            umpire = []
            for r in result:
                umpire_id = r[0]
                first_name = r[3]
                second_name = r[4]
                fullname = first_name + " " + second_name

                row = {'umpire_id': umpire_id, 'fullname': fullname}
                umpire.append(row)

            cursor = connection.cursor()
            sql = "SELECT * FROM TEAM"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()

            team = []
            for r in result:
                team_id=r[0]
                team_name=r[1]

                row = {'team_id': team_id, 'team_name':team_name}
                team.append(row)
            cursor = connection.cursor()
            sql = "SELECT * FROM SERIES"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()

            series = []
            for r in result:
                series_id=r[0]
                series_name=r[1]

                row = {'series_id': series_id, 'series_name': series_name}
                series.append(row)

            cursor = connection.cursor()
            sql = "SELECT * FROM GROUND"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()

            ground = []
            for r in result:
                ground_id=r[0]
                ground_name=r[1]

                row = {'ground_id': ground_id, 'ground_name':ground_name}
                ground.append(row)
            return render(request, 'addmatch/index.html', {'team':team,'player':player,'series':series, 'ground':ground, 'umpire':umpire})
        else:
            return redirect('login')

    else:
        team1 = request.POST['team1']
        team2 = request.POST['team2']
        series_name = request.POST['s_name_in']
        ground_name =request.POST['in_ground']
        match_type =""
        weather = request.POST['weather']
        winner= request.POST['winner']
        motm = request.POST['motm']
        ump1 = request.POST['ump1']
        partu1 = ump1.split(" ")
        first_nameu1 = partu1[0]
        last_nameu1 = partu1[1]
        ump2 = request.POST['ump2']
        partu2 = ump2.split(" ")
        first_nameu2 = partu2[0]
        last_nameu2 = partu2[1]
        ump3 = request.POST['ump3']
        partu3 = ump3.split(" ")
        first_nameu3 = partu3[0]
        last_nameu3 = partu3[1]

        match_date = request.POST['match_date']
        part = motm.split(" ")
        first_name = part[0]
        last_name = part[1]

        odi = request.POST.get('match_type_ODI', False)
        test = request.POST.get('match_type_TEST', False)
        t20 = request.POST.get('match_type_T20', False)

        if odi:
            match_type = "ODI"
        if test:
            match_type = "TEST"
        if t20:
            match_type = "T20"
        print(match_type)
        cursor = connection.cursor()
        sql = "SELECT PERSON_ID FROM PERSON WHERE (FIRST_NAME = '" + first_nameu1 + "' AND LAST_NAME='" + last_nameu1 + "') OR (FIRST_NAME = '" + first_nameu2 + "' AND LAST_NAME='" + last_nameu2 + "') OR (FIRST_NAME = '" + first_nameu3 + "' AND LAST_NAME='" + last_nameu3 + "')"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        umpire_id = []

        for r in result:
            um_id = r[0]
            row={'um_id':um_id}
            umpire_id.append(row)
        print(umpire_id)
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
        cursor = connection.cursor()
        sql = "SELECT GROUND_ID FROM GROUND WHERE NAME = '" + ground_name + "'"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        ground_id = ""
        for r in result:
            ground_id = r[0]
        cursor = connection.cursor()
        sql = "SELECT SERIES_ID FROM SERIES WHERE NAME = '" + series_name + "'"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        series_id = ""
        for r in result:
            series_id = r[0]
        cursor = connection.cursor()
        sql = "SELECT PERSON_ID FROM PERSON WHERE FIRST_NAME = '" + first_name + "' AND LAST_NAME='"+last_name+"'"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        motm_id=""

        for r in result:
            motm_id = r[0]

        date_refine=match_date.split("-")
        new_date=date_refine[2]+"-"+date_refine[1]+"-"+date_refine[0][2:4]
        in_match_id=str(team1_id)+str(team2_id)+"_"+str(new_date)

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO MATCH VALUES(:mID,:gID,:sID,:mType,:mmotm_id,:mweather,:mwinner,:mteam1id,:mteam2id, NULL)",
            mID=in_match_id, gID=ground_id, sID=series_id, mType=match_type, mmotm_id=motm_id, mweather=weather,
            mwinner=winner, mteam1id=team1_id, mteam2id=team2_id)

        connection.commit()
        cursor.close()

        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO TEAM_MATCH VALUES(:T_ID,:M_ID,TO_DATE(:M_DATE,'YYYY-MM-DD'))",
            T_ID=team1_id, M_ID=in_match_id, M_DATE=match_date)
        connection.commit()
        cursor.close()
        for r in umpire_id:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO UMPIRE_MATCH VALUES(:U_ID,:M_ID)",
                U_ID=r['um_id'], M_ID=in_match_id)
            connection.commit()
            cursor.close()

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO TEAM_MATCH VALUES(:T_ID,:M_ID,TO_DATE(:M_DATE,'YYYY-MM-DD'))",
            T_ID=team2_id, M_ID=in_match_id, M_DATE=match_date)
        connection.commit()
        cursor.close()

        file = request.FILES['player_score']
        dataset=file.read().decode('UTF-8')
        io_string=io.StringIO(dataset)
        next(io_string)
        for col in csv.reader(io_string, delimiter=',', quotechar="|"):
            print(col)
            match_id=col[0]
            person_id=col[1]
            scored_run=col[2]
            balls_batted=col[3]
            fours=col[4]
            sixes=col[5]
            not_out=col[6]
            balls_bowled=col[7]
            given_run=col[8]
            wicket=col[9]
            print(match_id)
            print(in_match_id)
            if match_id == in_match_id:
                print(match_id)
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO PLAYER_SCORE VALUES(:mID,:PID,:S_RUN,:B_BATTED,:B_FOURS,:B_SIXES,:B_NOTOUT,:B_BOWLED,:B_RUN, :WICKET)",
                    mID=match_id, PID=person_id, S_RUN=scored_run, B_BATTED=balls_batted, B_FOURS=fours, B_SIXES=sixes,
                    B_NOTOUT=not_out, B_BOWLED=balls_bowled, B_RUN=given_run, WICKET=wicket)

                connection.commit()
                cursor.close()



        # print(name, country, Address, street_no, zip_code, city)
        # return HttpResponse("File uploaded successfuly")
        return render(request, 'adminpage/index.html')
