import datetime

from django.shortcuts import render
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)

# Create your views here.


def records(request):
    cursor = connection.cursor()

    # HIGHEST SCORED RUNS BY A PLAYER IN A MATCH
    sql = "SELECT * FROM PLAYER_SCORE WHERE SCORED_RUNS= ANY(SELECT SCORED_RUNS FROM PLAYER_SCORE WHERE SCORED_RUNS=(SELECT MAX(SCORED_RUNS) FROM PLAYER_SCORE))"
    cursor.execute(sql)
    result = cursor.fetchall()
    highestRunByAplayerMatch = []
    for r in result:
        mid = r[0]
        pid = r[1]
        run = r[2]
        balls = r[3]
        fours = r[4]
        sixes = r[5]

        cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM PERSON WHERE PERSON_ID=:PID", PID=pid)
        re = cursor.fetchall()[0]
        name = re[0]+" "+re[1]
        # print('name: '+ name)


        cursor.execute("SELECT TEAM1_ID,TEAM2_ID FROM MATCH WHERE MATCH_ID=:MID", MID=mid)
        matchteams = cursor.fetchall()[0]
        team1 = matchteams[0]
        team2 = matchteams[1]

        cursor.execute("SELECT MATCH_DATE FROM TEAM_MATCH WHERE MATCH_ID=:MID", MID=mid)
        matchdate = cursor.fetchall()[0][0]
        format = "%B %d, %Y"  # The format
        dob2 = datetime.datetime.strptime(str(matchdate)[:-9], '%Y-%m-%d').strftime(format)

        row = {'run': run, 'balls': balls, 'fours': fours, 'sixes': sixes, 'name': name, 'team1': team1, 'team2': team2,
               'date': dob2}
        highestRunByAplayerMatch.append(row)
    # print(result)

    # highest wickets taken by a player in match
    sql="SELECT * FROM PLAYER_SCORE WHERE NUM_OF_WICKETS=ANY(SELECT NUM_OF_WICKETS FROM PLAYER_SCORE WHERE NUM_OF_WICKETS=(SELECT MAX(NUM_OF_WICKETS) FROM PLAYER_SCORE))"
    cursor.execute(sql)
    result = cursor.fetchall()
    highestwicketsByAplayerMatch = []
    # print(result)
    for r in result:
        mid = r[0]
        pid = r[1]
        overs = r[7]
        givenrun = r[8]
        wickets = r[9]

        cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM PERSON WHERE PERSON_ID=:PID", PID=pid)
        re = cursor.fetchall()[0]
        name = re[0] + " " + re[1]

        cursor.execute("SELECT TEAM1_ID,TEAM2_ID FROM MATCH WHERE MATCH_ID=:MID", MID=mid)
        matchteams = cursor.fetchall()[0]
        team1 = matchteams[0]
        team2 = matchteams[1]

        cursor.execute("SELECT MATCH_DATE FROM TEAM_MATCH WHERE MATCH_ID=:MID", MID=mid)
        matchdate = cursor.fetchall()[0][0]
        format = "%B %d, %Y"  # The format
        dob3 = datetime.datetime.strptime(str(matchdate)[:-9], '%Y-%m-%d').strftime(format)

        row = {'mid': mid, 'pid': pid, 'overs': overs, 'givenrun': givenrun, 'wickets': wickets, 'name': name, 'team1': team1, 'team2': team2,
               'date': dob3}
        highestwicketsByAplayerMatch.append(row)



    #highest run by a player in career
    sql="SELECT * FROM PLAYER_STAT WHERE PLAYER_ID=ANY(SELECT PLAYER_ID FROM PLAYER_STAT WHERE SCORED_RUN=(SELECT MAX(SCORED_RUN)FROM PLAYER_STAT))"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    highestRunByAplayerCareer = []

    for r in result:
        stid = r[0]
        pid = r[1]
        run = r[2]
        avg = r[8]
        strate = r[9]

        cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM PERSON WHERE PERSON_ID=:PID", PID=pid)
        re = cursor.fetchall()[0]
        name = re[0] + " " + re[1]

        row = {'stid': stid, 'pid': pid, 'run': run, 'avg': avg, 'strate': strate, 'name': name}
        highestRunByAplayerCareer.append(row)


    #HIGHEST WICKETS BY PLAYER IN A CAREER
    sql="SELECT * FROM PLAYER_STAT WHERE PLAYER_ID=ANY(SELECT PLAYER_ID FROM PLAYER_STAT WHERE NUM_OF_WICKETS=(SELECT MAX(NUM_OF_WICKETS) FROM PLAYER_STAT))"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)

    highestwicketsByAplayerCareer =[]

    for r in result:
        stid = r[0]
        pid = r[1]
        wickets = r[10]
        overs = r[12]
        bowlavg = r[14]

        cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM PERSON WHERE PERSON_ID=:PID", PID=pid)
        re = cursor.fetchall()[0]
        name = re[0] + " " + re[1]

        row = {'stid':stid, 'pid': pid, 'wickets': wickets, 'overs': overs, 'bowlavg': bowlavg, 'name': name}
        highestwicketsByAplayerCareer.append(row)


    #HIGHEST SCORED RUNS IN A MATCH
    sql="SELECT * FROM MATCH WHERE MATCH_ID=(SELECT MATCH_ID FROM PLAYER_SCORE GROUP BY MATCH_ID HAVING SUM(SCORED_RUNS)=(SELECT MAX(SUM(SCORED_RUNS)) FROM PLAYER_SCORE GROUP BY MATCH_ID))"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    highestScoredMatch = []

    for r in result:
        mid = r[0]
        gid = r[1]
        sid = r[2]
        type = r[3]
        winner = r[6]
        team1id = r[7]
        team2id = r[8]

        cursor.execute("SELECT MATCH_DATE FROM TEAM_MATCH WHERE MATCH_ID=:MID", MID=mid)
        matchdate = cursor.fetchall()[0][0]
        format = "%B %d, %Y"  # The format
        dob4 = datetime.datetime.strptime(str(matchdate)[:-9], '%Y-%m-%d').strftime(format)

        row = {'mid': mid, 'gid': gid, 'sid': sid, 'type': type, 'winner': winner, 'team1': team1id, 'team2': team2id, 'date':dob4}
        highestScoredMatch.append(row)


    #MAX WIN BY A TEAM
    sql="SELECT * FROM TEAM_STAT WHERE TEAM_ID=ANY(SELECT TEAM_ID FROM TEAM_STAT WHERE TOTAL_WIN=ANY(SELECT MAX(TOTAL_WIN) FROM TEAM_STAT))"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    MaxWinTeams =[]

    for r in result:
        stid = r[0]
        tid = r[1]
        totalwin = r[2]
        totalLose = r[3]

        cursor.execute("SELECT NAME FROM TEAM WHERE TEAM_ID=:TID", TID=tid)
        re = cursor.fetchall()[0]
        name = re[0]

        row = {'stid': stid, 'tid': tid, 'win': totalwin, 'lose': totalLose, 'name': name}
        MaxWinTeams.append(row)

    #max lose by a team
    sql="SELECT * FROM TEAM_STAT WHERE TEAM_ID=ANY(SELECT TEAM_ID FROM TEAM_STAT WHERE TOTAL_LOSE=ANY(SELECT MAX(TOTAL_LOSE) FROM TEAM_STAT))"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    MaxLoseTeams = []

    for r in result:
        stid = r[0]
        tid = r[1]
        totalwin = r[2]
        totalLose = r[3]

        cursor.execute("SELECT NAME FROM TEAM WHERE TEAM_ID=:TID", TID=tid)
        re = cursor.fetchall()[0]
        name = re[0]

        row = {'stid': stid, 'tid': tid, 'win': totalwin, 'lose': totalLose, 'name': name}
        MaxLoseTeams.append(row)

    return render(request, 'records/records.html', {'highestRunByAplayerMatch': highestRunByAplayerMatch, 'highestwicketsByAplayerMatch': highestwicketsByAplayerMatch,
                                                    'highestRunByAplayerCareer': highestRunByAplayerCareer, 'highestwicketsByAplayerCareer': highestwicketsByAplayerCareer,
                                                    'highestScoredMatch': highestScoredMatch,
                                                    'MaxWinTeams': MaxWinTeams, 'MaxLoseTeams': MaxLoseTeams})