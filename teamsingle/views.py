import datetime

from django.shortcuts import render
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)


# Create your views here.

def teamsingle(request):
    name = request.GET.get('name')
    cursor = connection.cursor()
    sql = "SELECT TEAM_ID, IMAGE FROM TEAM WHERE NAME = '" + name + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    team = []

    for r in result:
        team_id = r[0]
        image=r[1]
        row = {'team_id': team_id, 'image':image}
        team.append(row)
    team_id=team[0]['team_id']
    image_id = team[0]['image']
    print(image_id)
    cursor = connection.cursor()
    sql="SELECT * FROM PERSON, COACH WHERE PERSON_ID=ANY(SELECT COACH_ID FROM COACH WHERE TEAM_ID= '" + team_id + "') AND COACH_ID=PERSON_ID"
    #sql = "SELECT * FROM PERSON WHERE PERSON_ID=ANY(SELECT COACH_ID FROM COACH WHERE TEAM_ID= '" + team_id + "')"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    coach = []

    for r in result:
        first_name = r[1]
        last_name = r[2]
        start_date=r[10]
        format = "%B %d, %Y"  # The format
        dob2 = datetime.datetime.strptime(str(start_date)[:-9], '%Y-%m-%d').strftime(format)
        fullname=first_name + " " + last_name
        row = {'fullname': fullname, 'start_date':dob2}
        coach.append(row)

    cursor = connection.cursor()
    sql = "SELECT TEAM1_ID, TEAM2_ID, MATCH_ID FROM MATCH WHERE WINNER= '" + name + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    details = []

    for r in result:

        team1_name=""
        team2_name=""
        team1_id=r[0]
        cursor = connection.cursor()
        sql = "SELECT NAME FROM TEAM WHERE TEAM_ID= '" + team1_id + "'"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()
        for k in result2:
            team1_name=k[0]
        team2_id = r[1]
        cursor = connection.cursor()
        sql = "SELECT NAME FROM TEAM WHERE TEAM_ID= '" + team2_id + "'"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()
        for k in result2:
            team2_name=k[0]
        match_id=r[2]
        cursor = connection.cursor()
        cursor.execute("SELECT MATCH_DATE FROM TEAM_MATCH WHERE MATCH_ID=:MID", MID=match_id)
        matchdate = cursor.fetchall()[0][0]
        cursor.close()
        format = "%B %d, %Y"  # The format
        matchdate2 = datetime.datetime.strptime(str(matchdate)[:-9], '%Y-%m-%d').strftime(format)
        row = {'team1_id': team1_id, 'team2_id': team2_id, 'match_id':match_id, 'team1_name':team1_name, 'team2_name':team2_name, 'match_date':matchdate2}
        details.append(row)

    cursor = connection.cursor()
    sql = "SELECT TOTAL_WIN, TOTAL_LOSE, NOT_PLAYED, STAT_ID FROM TEAM_STAT WHERE TEAM_ID = '" + team_id + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    team_stat = []

    stat_id=""
    for r in result:
        total_win = r[0]
        total_lose=r[1]
        not_played=r[2]
        stat_id=r[3]
        row = {'total_win': total_win, 'total_lose': total_lose, 'not_played': not_played}
        team_stat.append(row)

    cursor = connection.cursor()
    sql = "SELECT RATING FROM STAT WHERE STAT_ID = '" + stat_id + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    rating = []
    rate=""
    for r in result:
        rate = r[0]
        row = {'rate': rate}
        rating.append(row)
    tStat = None
    if len(team_stat) != 0:
        tStat = team_stat[0]

    cursor = connection.cursor()
    sql = "SELECT * FROM (SELECT * FROM PERSON P1, PLAYER P2  WHERE P1.PERSON_ID=P2.PLAYER_ID) P LEFT OUTER JOIN PLAYER_STAT PS ON (P.PLAYER_ID=PS.PLAYER_ID) LEFT OUTER JOIN STAT S ON (PS.STAT_ID=S.STAT_ID) JOIN TEAM_PLAYER TP ON (TP.PLAYER_ID=P.PLAYER_ID) WHERE P.ROLE='Batsman' AND TP.TEAM_ID=(SELECT TEAM_ID FROM TEAM WHERE NAME='"+name+"') ORDER BY S.RATING DESC NULLS LAST, TOTAL_RUN DESC NULLS LAST"
    # sql = "SELECT * FROM TEAM T JOIN TEAM_PLAYER TP ON(T.TEAM_ID=TP.TEAM_ID) JOIN PERSON P ON(P.PERSON_ID=TP.PLAYER_ID) WHERE T.NAME='"+team_name+"'"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    best=[]


    if(bool(result)):
        id = result[0][0]
        first_name = result[0][1]
        last_name = result[0][2]
        full_name = first_name + " " + last_name
        row = {'fullname':full_name}
        best.append(row)
    else:
        row = {'fullname': None}
        best.append(row)
    cursor = connection.cursor()
    sql = "SELECT * FROM (SELECT * FROM PERSON P1, PLAYER P2  WHERE P1.PERSON_ID=P2.PLAYER_ID) P LEFT OUTER JOIN PLAYER_STAT PS ON (P.PLAYER_ID=PS.PLAYER_ID) LEFT OUTER JOIN STAT S ON (PS.STAT_ID=S.STAT_ID) JOIN TEAM_PLAYER TP ON (TP.PLAYER_ID=P.PLAYER_ID) WHERE P.ROLE='Bowler' AND TP.TEAM_ID=(SELECT TEAM_ID FROM TEAM WHERE NAME='" + name + "') ORDER BY S.RATING DESC NULLS LAST, TOTAL_RUN DESC NULLS LAST"
    # sql = "SELECT * FROM TEAM T JOIN TEAM_PLAYER TP ON(T.TEAM_ID=TP.TEAM_ID) JOIN PERSON P ON(P.PERSON_ID=TP.PLAYER_ID) WHERE T.NAME='"+team_name+"'"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    best2 = []

    if (bool(result)):
        id = result[0][0]
        first_name = result[0][1]
        last_name = result[0][2]
        full_name = first_name + " " + last_name
        row = {'fullname': full_name}
        best2.append(row)
    else:
        row = {'fullname': None}
        best2.append(row)
    cursor = connection.cursor()
    sql = "SELECT * FROM (SELECT * FROM PERSON P1, PLAYER P2  WHERE P1.PERSON_ID=P2.PLAYER_ID) P LEFT OUTER JOIN PLAYER_STAT PS ON (P.PLAYER_ID=PS.PLAYER_ID) LEFT OUTER JOIN STAT S ON (PS.STAT_ID=S.STAT_ID) JOIN TEAM_PLAYER TP ON (TP.PLAYER_ID=P.PLAYER_ID) WHERE P.ROLE='Allrounder' AND TP.TEAM_ID=(SELECT TEAM_ID FROM TEAM WHERE NAME='" + name + "') ORDER BY S.RATING DESC NULLS LAST, TOTAL_RUN DESC NULLS LAST"
    # sql = "SELECT * FROM TEAM T JOIN TEAM_PLAYER TP ON(T.TEAM_ID=TP.TEAM_ID) JOIN PERSON P ON(P.PERSON_ID=TP.PLAYER_ID) WHERE T.NAME='"+team_name+"'"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    best3 = []
    if (bool(result)):
        id = result[0][0]
        first_name = result[0][1]
        last_name = result[0][2]
        full_name = first_name + " " + last_name
        row = {'fullname': full_name}
        best3.append(row)
    else:
        row = {'fullname': None}
        best3.append(row)

    print(best)
    return render(request, 'teamsingle/index.html', {'name': name, 'details': details, 'coach': coach, 'team_stat': tStat, 'rate': rate, 'image_id':image_id, 'best':best[0], 'best2':best2[0], 'best3':best3[0]})
