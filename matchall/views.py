from django.shortcuts import render
import cx_Oracle
import io
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.


def matchall(request):
    cursor = connection.cursor()
    sql = "SELECT * FROM MATCH"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []

    for r in result:
        match_id = r[0]
        ground = r[1]
        series_id=r[2]
        type = r[3]
        motm = r[4]
        weather=r[5]

        if(r[6]):
            winner = r[6]
        else:
            winner="No Result"
        team1=r[7]
        team2=r[8]
        video=r[9]
        cur = connection.cursor()
        sql = "SELECT * from TEAM WHERE TEAM_ID='"+team1+"'"
        cur.execute(sql)
        re = cur.fetchall()
        cur.close()
        for d in re:
            team1 = d[1]
        cur = connection.cursor()
        sql = "SELECT * from TEAM WHERE TEAM_ID='"+team2+"'"
        cur.execute(sql)
        re = cur.fetchall()
        cur.close()
        for d in re:
            team2 = d[1]
        cur = connection.cursor()
        sql = "SELECT * from GROUND WHERE GROUND_ID='"+ground+"'"
        cur.execute(sql)
        re = cur.fetchall()
        cur.close()
        for d in re:
            ground = d[1]
        cur = connection.cursor()
        sql = "SELECT * from SERIES WHERE SERIES_ID='"+series_id+"'"
        cur.execute(sql)
        re = cur.fetchall()
        cur.close()
        series_name=""
        for d in re:
            series_name = d[1]
        cur = connection.cursor()
        if(motm):
            newcur = connection.cursor()
            lOutput = cursor.var(cx_Oracle.STRING)
            args = [motm, lOutput]
            newcur.callproc('GET_FULLNAME_FROM_PERSON', args)
            newcur.close()
            name=str(args[1])[29:-2].strip("'")

        image_link = "default.jpg"
        match_name=""+ team1 + " vs " + team2
        row = {'match_id': match_id, 'match_name':match_name, 'ground': ground, 'series_name': series_name, 'type':type, 'motm': name, 'weather':weather, 'winner': winner,
               'team1':team1, 'team2':team2, 'video_link': video}
        dict_result.append(row)
    return render(request, 'matchall/index.html', {'results': dict_result})