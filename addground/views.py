from django.shortcuts import render, redirect
import cx_Oracle

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
connection = cx_Oracle.connect(user='cricinfo', password='cricinfo', dsn=dsn_tns)


# Create your views here.


def addground(request):
    if request.method == 'GET':
        if request.session['loginstatus']:
            return render(request, 'addground/index.html')
        else:
            return redirect('login')
    else:
        name = request.POST['name']
        country = request.POST['country']
        Address = request.POST['address']
        street_no = request.POST['street_no']
        zip_code = request.POST['pincode']
        city = request.POST['city']
        file = request.FILES['image']
        # print(file.name)
        splits = file.name.split(".")
        # print(splits[-1])
        fname = city + "_" + country + "_" + zip_code + "." + splits[-1]
        gid = country+"_"+city
        print(name, country, Address, street_no, zip_code, city)
        handle_uploaded_file(request.FILES['image'], fname)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO GROUND VALUES(:GID,:GNAME,:GCITY,:GSTRNO,:GZIP,:GIMAGE)", GID=gid, GNAME=name, GCITY=city, GSTRNO=street_no, GZIP=zip_code, GIMAGE=fname)
        connection.commit()
        cursor.close()
        # return HttpResponse("File uploaded successfuly")
        return render(request, 'adminpage/index.html')


def handle_uploaded_file(f, name):
    with open('static/grounds/images/' + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
