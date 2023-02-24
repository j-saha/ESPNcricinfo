import datetime
import time

from django.shortcuts import render, redirect
import cx_Oracle, json

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.

players_fullname = []


def umpiresall(request):
    if request.method == "GET":
        players_fullname.clear()
        cursor = connection.cursor()
        sql="SELECT P.PERSON_ID, P.FIRST_NAME, P.LAST_NAME, P.NATIONALITY, P.DATE_OF_BIRTH, P.IMAGE, COUNT(*) AS NUM_OF_MATCH FROM PERSON P JOIN UMPIRE U ON(P.PERSON_ID=U.UMPIRE_ID) LEFT OUTER JOIN UMPIRE_MATCH UM ON (P.PERSON_ID=UM.UMPIRE_ID) GROUP BY U.UMPIRE_ID,P.PERSON_ID, P.FIRST_NAME, P.LAST_NAME, P.NATIONALITY, P.DATE_OF_BIRTH, P.IMAGE ORDER BY NUM_OF_MATCH DESC NULLS LAST"
        #sql = "SELECT * FROM PERSON P JOIN UMPIRE U ON(P.PERSON_ID=U.UMPIRE_ID) JOIN UMPIRE_MATCH UM ON (P.PERSON_ID=UM.UMPIRE_ID)"
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
            no_of_match=r[6]
            cursor = connection.cursor()
            sql="SELECT * FROM UMPIRE_MATCH WHERE UMPIRE_ID='"+id+"'"
            cursor.execute(sql)
            result = cursor.fetchall()
            if(bool(result)==False):
                no_of_match=0
            cursor.close()
            if image_link is None:
                image_link = "default.jpg"
            row = {'id': id, 'first_name': first_name, 'last_name': last_name, 'full_name': full_name,
                   'nationality': nationality, 'date_of_birth': dob2, 'image_link': image_link, 'no_of_match':no_of_match}
            dict_result.append(row)

        json_names = json.dumps(players_fullname)
        json_fname = json.dumps(first_name_list)
        json_lname = json.dumps(last_name_list)
        return render(request, 'umpiresall/index.html',
                      {'persons': dict_result, 'names': json_names, 'fname': json_fname, 'lname': json_lname})

    else:
        name = request.POST['search2']
        # print(players_fullname)
        if str(name) in players_fullname:
            part = name.split(" ")
            first_name = part[0]
            last_name = part[1]
            cursor = connection.cursor()
            sql = "SELECT * FROM PERSON P JOIN UMPIRE U ON(P.PERSON_ID=U.UMPIRE_ID) WHERE FIRST_NAME='" + first_name + "' AND LAST_NAME='" + last_name + "'"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()

            dict_result = []
            id = ""

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

            #return render(request, 'umpiresingle/index.html', {'name': name, 'details': dict_result[0]})
            cursor = connection.cursor()
            fun_age = cursor.callfunc('CALCULATE_AGE', float, [id])
            year = int(fun_age)
            diff = float(fun_age) - int(fun_age)
            month = int(diff * 12)
            day = int((diff * 12 - month) * 30)
            fun_age = str(year) + " years " + str(month) + " months " + str(day) + " days"
            print(year, month, day)
            cursor.close()

            cursor = connection.cursor()
            sql = "SELECT M.MATCH_ID, M.TEAM1_ID, M.TEAM2_ID FROM MATCH M JOIN UMPIRE_MATCH UM ON(M.MATCH_ID=UM.MATCH_ID) WHERE UM.UMPIRE_ID='" + id + "'"
            cursor.execute(sql)
            result = cursor.fetchall()

            NumOfMatches = 0
            if id != "":
                NumOfMatches = cursor.callfunc('GET_NO_OF_MATCH', int, [id])

            cursor.close()

            history = []

            for r in result:
                team1_name = ""
                team2_name = ""
                team1_id = r[1]
                team2_id = r[2]
                cursor = connection.cursor()
                sql = "SELECT NAME FROM TEAM WHERE TEAM_ID= '" + team1_id + "'"
                cursor.execute(sql)
                result2 = cursor.fetchall()
                cursor.close()
                for k in result2:
                    team1_name = k[0]

                cursor = connection.cursor()
                sql = "SELECT NAME FROM TEAM WHERE TEAM_ID= '" + team2_id + "'"
                cursor.execute(sql)
                result2 = cursor.fetchall()
                cursor.close()
                for k in result2:
                    team2_name = k[0]
                match_id = r[0]
                cursor = connection.cursor()
                sql = "SELECT MATCH_DATE FROM TEAM_MATCH WHERE MATCH_ID='" + match_id + "'"
                cursor.execute(sql)
                matchdate = cursor.fetchall()[0][0]
                format = "%B %d, %Y"  # The format
                matchdate2 = datetime.datetime.strptime(str(matchdate)[:-9], '%Y-%m-%d').strftime(format)
                cursor.close()
                row = {'team1_id': team1_id, 'team2_id': team2_id, 'match_id': match_id, 'team1_name': team1_name,
                       'team2_name': team2_name, 'match_date': matchdate2}
                history.append(row)

            return render(request, 'umpiresingle/index.html',
                          {'name': name, 'details': dict_result[0], 'history': history, 'age': fun_age,
                           'number': NumOfMatches})
        else:
            return redirect('umpiresall')

