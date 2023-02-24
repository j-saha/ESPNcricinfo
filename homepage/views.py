from django.contrib.auth import logout
from django.shortcuts import render, redirect
import random, cx_Oracle, json

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)


# Create your views here.
def home(request):
    request.session['loginstatus'] = False
    logout(request)
    cursor = connection.cursor()
    sql = "SELECT * FROM TEAM T LEFT OUTER JOIN TEAM_STAT TS ON (T.TEAM_ID=TS.TEAM_ID) LEFT OUTER JOIN STAT S ON (TS.STAT_ID=S.STAT_ID) ORDER BY S.RATING DESC NULLS LAST"
    # sql = "SELECT * FROM TEAM"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    teams = []
    rank = 0
    for r in result:
        rank = rank + 1
        id = r[0]
        name = r[1]
        image_link = r[2]
        row = {'id': id, 'name': name, 'image_link': image_link, 'rank': rank}
        teams.append(row)

    curs = connection.cursor()
    sql = "SELECT * FROM SERIES"
    curs.execute(sql)
    result = curs.fetchall()
    curs.close()
    series = []

    for r in result:
        id = r[0]
        name = r[1]
        host = r[2]
        motm = r[3]
        cur = connection.cursor()
        sql = "SELECT * from PERSON WHERE PERSON_ID='" + motm + "'"
        cur.execute(sql)
        re = cur.fetchall()
        cur.close()
        for d in re:
            fn = d[1]
            ln = d[2]
            fullname = fn + " " + ln
        winner = r[4]
        image_link = r[5]
        if image_link is None:
            image_link = "default.jpg"
        row = {'id': id, 'name': name, 'host': host, 'motm': fullname, 'winner': winner, 'image_link': image_link}
        series.append(row)

    return render(request, 'homepage/index.html', {'teams': teams, 'series': series})


def series_details(request):
    series_name = request.GET.get('name')
    cursor = connection.cursor()
    sql = "SELECT * FROM SERIES WHERE NAME='" + series_name + "'"
    cursor.execute(sql)
    result = cursor.fetchall()

    dict_result = []
    sid = ""

    for r in result:
        sid = r[0]
        id = r[0]
        name = r[1]
        host = r[2]
        motm = r[3]
        cur = connection.cursor()
        sql = "SELECT * from PERSON WHERE PERSON_ID='" + motm + "'"
        cur.execute(sql)
        re = cur.fetchall()
        cur.close()
        for d in re:
            fn = d[1]
            ln = d[2]
            fullname = fn + " " + ln
        winner = r[4]
        image_link = r[5]
        if image_link is None:
            image_link = "default.jpg"
        row = {'id': id, 'name': name, 'host': host, 'motm': fullname, 'winner': winner, 'image_link': image_link}
        dict_result.append(row)

    cursor.execute("SELECT * FROM SERIES S, MATCH M WHERE S.SERIES_ID=M.SERIES_ID AND S.SERIES_ID=:SID", SID=sid)
    result = cursor.fetchall()

    Matches = []
    matchno = 1
    for r in result:
        mid = r[6]
        gid = r[7]
        type = r[9]
        motm = r[10]
        motmFullName = ""
        print(motm)
        if motm is not None:
            cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM PERSON WHERE PERSON_ID=:PID", PID=motm)
            result2 = cursor.fetchall()[0]
            motmFullName = result2[0] + " " + result2[1]
        weather = r[11]
        winner = r[12]
        toss_win = r[13]
        # video = r[15]

        row = {'no': matchno, 'mid': mid, 'gid': gid, 'type': type, 'motm': motmFullName, 'weather': weather,
               'winner': winner, 'toss': toss_win}
        matchno = matchno + 1
        Matches.append(row)

    newcur = connection.cursor()
    lOutput = cursor.var(cx_Oracle.NUMBER)
    args = [sid, lOutput]
    newcur.callproc('PROC_FOURS_IN_SERIES', args)
    newcur.close()
    fours = str(lOutput)[29:-3]
    print(fours)
    if fours == "No":
        fours = 0

    sixes = cursor.callfunc('SIXES_IN_SERIES', int, [sid])
    if sixes == None:
        sixes = 0

    return render(request, 'homepage/speaker-details.html',
                  {'name': series_name, 'series': dict_result[0], 'matches': Matches, 'fours': fours, 'sixes': sixes})


def teams(request):
    all_team = []
    if request.method == "GET":
        cursor = connection.cursor()
        sql = "SELECT * FROM TEAM T LEFT OUTER JOIN TEAM_STAT TS ON (T.TEAM_ID=TS.TEAM_ID) LEFT OUTER JOIN STAT S ON (TS.STAT_ID=S.STAT_ID) ORDER BY S.RATING DESC NULLS LAST"
        # sql = "SELECT * FROM TEAM"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        dict_result = []
        all_team.clear()
        rank = 0
        for r in result:
            rank = rank + 1
            id = r[0]
            name = r[1]
            all_team.append(name)
            image_link = r[2]
            row = {'id': id, 'name': name, 'image_link': image_link, 'rank': rank}
            dict_result.append(row)

        json_teams = json.dumps(all_team)

        return render(request, 'homepage/teams.html', {'results': dict_result, 'allteam': json_teams})
    else:
        name = request.POST['search2']
        return redirect('teams')
