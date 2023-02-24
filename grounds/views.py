from django.shortcuts import render
import random, cx_Oracle

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)


# Create your views here.


def grounds(request):
    cursor = connection.cursor()
    sql = "SELECT * FROM GROUND"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    dict_result = []

    for r in result:
        id = r[0]
        name = r[1]
        city = r[2]
        st_no = r[3]
        zip_code = r[4]
        image_link = r[5]
        row = {'id': id, 'name': name, 'city': city, 'street_no': st_no, 'zip_code': zip_code, 'image_link': image_link}
        dict_result.append(row)

    return render(request, 'grounds/index.html', {'results': dict_result})