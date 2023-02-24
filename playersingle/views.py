import datetime

from django.shortcuts import render
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)


# Create your views here.

def playersingle(request):
    name = request.GET.get('name')
    part = name.split(" ")
    first_name = part[0]
    last_name = part[1]
    cursor = connection.cursor()
    print(first_name)
    print(last_name)
    # sql = "SELECT * FROM PERSON WHERE FIRST_NAME='" + first_name + "' AND LAST_NAME='" + last_name + "'"

    cursor.execute("SELECT * FROM PERSON P, PLAYER PL WHERE P.PERSON_ID=PL.PLAYER_ID AND FIRST_NAME=:FNAME AND LAST_NAME=:LNAME", FNAME=first_name, LNAME=last_name)
    result = cursor.fetchall()

    pid = ""

    dict_result = []
    for r in result:
        pid = r[0]
        id = r[0]
        first_name = r[1]
        last_name = r[2]
        full_name = first_name + " " + last_name
        nationality = r[3]
        dob = r[4]
        format = "%B %d, %Y"  # The format
        dob2 = datetime.datetime.strptime(str(dob)[:-9], '%Y-%m-%d').strftime(format)
        image_link = r[5]
        role = r[7]
        print(role)
        bat_style = r[8]
        bowl_style = r[9]
        if image_link is None:
            image_link = "default.jpg"
        row = {'id': id, 'first_name': first_name, 'last_name': last_name, 'full_name': full_name,
               'nationality': nationality, 'date_of_birth': dob2, 'image_link': image_link,'role': role, 'batstyle':bat_style,'bowlstyle':bowl_style}
        dict_result.append(row)

    print(dict_result)
    cursor.execute("SELECT * FROM PLAYER_STAT PS, STAT S WHERE PLAYER_ID=:PID AND PS.STAT_ID=S.STAT_ID", PID=pid)
    result21 = cursor.fetchall()
    print(result21)
    playerSTAT = {}
    if len(result21) != 0:
        result2 = result21[0]
        scored_run = result2[2]
        motm = result2[3]
        hundred = result2[4]
        fifty = result2[5]
        notout = result2[7]
        avgrun = result2[8]
        strate = result2[9]
        wickets = result2[10]
        fifer = result2[11]
        overs = result2[12]
        givenrun = result2[13]
        bowl_avg = result2[14]
        bowl_strate = result2[15]
        matches = result2[17]
        rating = result2[18]

        playerSTAT ={'scored_run': scored_run, 'motm': motm,'hundred': hundred, 'fifty': fifty, 'notout': notout, 'avgrun': avgrun, 'strate':strate, 'wickets': wickets,
                'fifer': fifer, 'overs': overs, 'givenrun': givenrun, 'bowl_avg': bowl_avg, 'bowl_strate': bowl_strate, 'matches': matches, 'rating': rating}

    cursor.execute("SELECT * FROM PLAYER_SCORE WHERE PLAYER_ID=:PID", PID=pid)
    res = cursor.fetchall()


    Matches = []

    fun_age = cursor.callfunc('CALCULATE_AGE', float, [pid])
    year = int(fun_age)
    diff = float(fun_age) - int(fun_age)
    month = int(diff * 12)
    day = int((diff * 12 - month) * 30)
    fun_age = str(year) + " years " + str(month) + " months " + str(day) + " days"

    for r in res:
        mid = r[0]
        scored_run = r[2]
        balls = r[3]
        fours = r[4]
        sixes = r[5]
        notout = r[6]
        if notout == "":
            notout = "NOT BATTED"
        overs = r[7]
        givenrun = r[8]
        wickets = r[9]

        cursor.execute("SELECT TEAM1_ID,TEAM2_ID FROM MATCH WHERE MATCH_ID=:MID", MID=mid)
        matchteams = cursor.fetchall()[0]
        team1 = matchteams[0]
        team2 = matchteams[1]

        cursor.execute("SELECT MATCH_DATE FROM TEAM_MATCH WHERE MATCH_ID=:MID", MID=mid)
        matchdate = cursor.fetchall()[0][0]


        row = {'mid': mid, 'scored_run': scored_run, 'balls': balls, 'fours': fours, 'sixes': sixes, 'notout': notout,
               'overs': overs, 'givenrun': givenrun, 'wickets': wickets,
               'team1': team1, 'team2': team2, 'date': matchdate}
        Matches.append(row)

    return render(request, 'playersingle/playersingle.html', {'name': name, 'details': dict_result[0],
                                                              'playerstat': playerSTAT, 'matches': Matches, 'age': fun_age})
