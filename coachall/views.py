import datetime
import time

from django.shortcuts import render, redirect
import cx_Oracle, json

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.

players_fullname = []


def coachall(request):
    if request.method == "GET":
        players_fullname.clear()
        cursor = connection.cursor()
        sql = "SELECT * FROM PERSON P JOIN COACH C ON(P.PERSON_ID=C.COACH_ID)"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        dict_result = []
        first_name_list = []
        last_name_list = []
        for r in result:
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
            dob2=datetime.datetime.strptime(str(dob)[:-9], '%Y-%m-%d').strftime(format)
            image_link = r[5]
            if image_link is None:
                image_link = "default.jpg"
            row = {'id': id, 'first_name': first_name, 'last_name': last_name, 'full_name': full_name,
                   'nationality': nationality, 'date_of_birth': dob2, 'image_link': image_link}
            dict_result.append(row)

        json_names = json.dumps(players_fullname)
        json_fname = json.dumps(first_name_list)
        json_lname = json.dumps(last_name_list)
        return render(request, 'coachall/index.html',
                      {'persons': dict_result, 'names': json_names, 'fname': json_fname, 'lname': json_lname})

    else:
        name = request.POST['search2']
        # print(players_fullname)
        if str(name) in players_fullname:
            part = name.split(" ")
            first_name = part[0]
            last_name = part[1]
            cursor = connection.cursor()
            sql = "SELECT * FROM PERSON P JOIN COACH C ON(P.PERSON_ID=C.COACH_ID) WHERE FIRST_NAME='" + first_name + "' AND LAST_NAME='" + last_name + "'"
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
                format = "%B %d, %Y"  # The format
                dob2 = datetime.datetime.strptime(str(dob)[:-9], '%Y-%m-%d').strftime(format)
                image_link = r[5]
                if image_link is None:
                    image_link = "default.jpg"
                row = {'id': id, 'first_name': first_name, 'last_name': last_name, 'full_name': full_name,
                       'nationality': nationality, 'date_of_birth': dob2, 'image_link': image_link}
                dict_result.append(row)

            cursor = connection.cursor()
            fun_age = cursor.callfunc('CALCULATE_AGE', float, [id])
            print(fun_age)
            year = int(fun_age)
            diff = float(fun_age) - int(fun_age)
            month = int(diff * 12)
            day = int((diff * 12 - month) * 30)
            fun_age = str(year) + " years " + str(month) + " months " + str(day) + " days"
            cursor.close()
            cursor = connection.cursor()
            sql = "SELECT T.NAME, C.START_DATE, C.START_YEAR FROM TEAM T JOIN COACH C ON(T.TEAM_ID=C.TEAM_ID) WHERE COACH_ID='" + id + "' "
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()

            teamcoached = []

            for r in result:
                teamid = r[0]
                s_date = r[1]
                s_year = r[2]
                format = "%B %d, %Y"  # The format
                dob2 = datetime.datetime.strptime(str(s_date)[:-9], '%Y-%m-%d').strftime(format)
                row = {'teamid': teamid, 's_date': dob2, 's_year': s_year}
                teamcoached.append(row)
                print(s_year)

            return render(request, 'coachsingle/index.html',
                          {'name': name, 'details': dict_result[0], 'teamcoached': teamcoached[0], 'age': fun_age})
        else:
            return redirect('coachall')
