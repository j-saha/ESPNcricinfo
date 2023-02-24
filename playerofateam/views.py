import datetime

from django.shortcuts import render, redirect
import cx_Oracle, json

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.

players_fullname = []


def playerofateam(request):
    if request.method == "GET":
        team_name=request.GET['team']
        players_fullname.clear()
        cursor = connection.cursor()
        sql="SELECT * FROM (SELECT * FROM PERSON P1, PLAYER P2  WHERE P1.PERSON_ID=P2.PLAYER_ID) P LEFT OUTER JOIN PLAYER_STAT PS ON (P.PLAYER_ID=PS.PLAYER_ID) LEFT OUTER JOIN STAT S ON (PS.STAT_ID=S.STAT_ID) JOIN TEAM_PLAYER TP ON (TP.PLAYER_ID=P.PLAYER_ID) WHERE TP.TEAM_ID=(SELECT TEAM_ID FROM TEAM WHERE NAME='"+team_name+"') ORDER BY S.RATING DESC NULLS LAST, PS.TOTAL_RUN DESC NULLS LAST"
        #sql = "SELECT * FROM TEAM T JOIN TEAM_PLAYER TP ON(T.TEAM_ID=TP.TEAM_ID) JOIN PERSON P ON(P.PERSON_ID=TP.PLAYER_ID) WHERE T.NAME='"+team_name+"'"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        dict_result = []
        first_name_list = []
        last_name_list = []
        rank=0
        for r in result:
            rank=rank+1
            id = r[0]
            first_name = r[1]
            last_name = r[2]
            full_name = first_name + " " + last_name
            players_fullname.append(full_name)
            first_name_list.append(first_name)
            last_name_list.append(last_name)
            nationality = r[3]
            dob = r[4]
            format = "%B %d, %Y"  # The format
            dob2 = datetime.datetime.strptime(str(dob)[:-9], '%Y-%m-%d').strftime(format)
            image_link = r[5]
            if image_link is None:
                image_link = "default.jpg"
            row = {'id': id, 'first_name': first_name, 'last_name': last_name, 'full_name': full_name,
                   'nationality': nationality, 'date_of_birth': dob2, 'image_link': image_link, 'rank':rank}
            dict_result.append(row)

        json_names = json.dumps(players_fullname)
        json_fname = json.dumps(first_name_list)
        json_lname = json.dumps(last_name_list)
        return render(request, 'playersall/index.html',
                      {'persons': dict_result, 'names': json_names, 'fname': json_fname, 'lname': json_lname})

    else:
        name = request.POST['search2']
        # print(players_fullname)
        if str(name) in players_fullname:
            part = name.split(" ")
            first_name = part[0]
            last_name = part[1]
            cursor = connection.cursor()
            sql = "SELECT * FROM PERSON WHERE FIRST_NAME='" + first_name + "' AND LAST_NAME='" + last_name + "'"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()

            dict_result = []

            for r in result:
                id = r[0]
                first_name = r[1]
                last_name = r[2]
                full_name = first_name + " " + last_name
                nationality = r[3]
                dob = r[4]
                image_link = r[5]
                if image_link is None:
                    image_link = "default.jpg"
                row = {'id': id, 'first_name': first_name, 'last_name': last_name, 'full_name': full_name,
                       'nationality': nationality, 'date_of_birth': dob, 'image_link': image_link}
                dict_result.append(row)

            return render(request, 'playersingle/playersingle.html', {'name': name, 'details': dict_result[0]})
        else:
            return redirect('playersall')
