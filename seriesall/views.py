from django.shortcuts import render
import cx_Oracle
dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)
# Create your views here.


def seriesall(request):
    cursor = connection.cursor()
    sql = "SELECT * FROM SERIES"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []

    for r in result:
        id = r[0]
        name = r[1]
        host = r[2]
        motm = r[3]
        cur = connection.cursor()
        sql = "SELECT * from PERSON WHERE PERSON_ID='"+motm+"'"
        cur.execute(sql)
        re = cur.fetchall()
        cur.close()
        for d in re:
            fn = d[1]
            ln = d[2]
            fullname = fn+" "+ln
        winner = r[4]
        image_link = r[5]
        if image_link is None:
            image_link = "default.jpg"
        row = {'id': id, 'name': name, 'host': host, 'motm': fullname, 'winner': winner, 'image_link': image_link}
        dict_result.append(row)
    return render(request, 'seriesall/index.html', {'results': dict_result})