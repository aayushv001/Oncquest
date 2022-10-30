from typing_extensions import runtime
from django.core.checks import messages
from django.http import request
from django.shortcuts import redirect, render,HttpResponse
from .models import data,pdata,regdata
import psycopg2 as p
import xlwt as x
from django.contrib.auth.models import auth
from django.contrib import messages
import datetime
import json
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import logout

# Create your views here.
def validateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False
def home(request):
    logout(request)
    return render(request,"home.html")
def add(request):
    conn=p.connect(host="localhost",database="Base1",user="postgres",password="1234")
    cur=conn.cursor()
    cur.execute("SELECT runstat FROM public.one_pdata where id = (select Max(id) from public.one_pdata)")
    runstat=cur.fetchone()
    if runstat==None:
        runstat=['ED',]
    cur.execute("SELECT runid FROM public.one_pdata where id = (select Max(id) from public.one_pdata)")
    runno=cur.fetchone()
    if runno==None:
        runno=[1,]
    val1= request.POST['num1']
    #request.session['username']=val1
    val2 = request.POST['num2']
    #request.session['sampleCount']=0
    #sampleCount=request.session.get('sampleCount')
    #cur.execute("SELECT Count(*) FROM public.one_pdata where runstat='R' and rem != 'NC' ")
    #samplefromdb=cur.fetchone()
    #sampleCount=samplefromdb[0]+sampleCount
    #request.session['sampleCount']=sampleCount
    user=auth.authenticate(username=val1,password=val2)
    if user is not None:
        auth.login(request,user)
        dbrole=request.user.role
        #request.session['role']=dbrole
        dt=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if dbrole=="SR":
            cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat='R';")
        elif dbrole=="REPORTING":
            cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat='ER' and res='';")
        elif dbrole=="RECEIVING":
            cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat!='ED' and accid=''")
        sqlraw=cur.fetchall()
        dblen=len(sqlraw)
        sql=json.dumps(sqlraw)
        cur.execute("SELECT srfid, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email FROM public.one_regdata;")
        regdataraw=cur.fetchall()
        reglen=len(regdataraw)
        regdata=json.dumps(regdataraw)
        cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata;")
        chkdataraw=cur.fetchall()
        chkdatalen=len(chkdataraw)
        chkdata=json.dumps(chkdataraw)
        cur.close()
        conn.close()
        if dbrole=='ADMIN':
            return render(request,"adminpage.html",{'result':val1,'role':dbrole,'date':dt,'runstat':runstat[0],'runno':runno[0]})
        else:
            return render(request,"result.html",{'result':val1,'role':dbrole,'sql':sqlraw,'runstat':runstat[0],'runno':runno[0],'dblen':dblen,'sqljson':sql,'regdata':regdata,'reglen':reglen,'chkdata':chkdata,'chklen':chkdatalen,})
    else:
        return redirect("home")
def register(request):
    name=request.user.username
    role=request.user.role
    return render(request,"register.html",{'name':name,'role':role})

def adduser(request):
    if request.method == 'POST':
        name=request.POST['nname']
        username=request.POST['nuser']
        password=request.POST['npass']
        role=request.POST['nrole']
        if data.objects.filter(username=username).exists():
            messages.error(request,'Username Taken')
            return redirect("register")
        elif role!="ADMIN" and role!="SR" and role!="RECEIVING" and role!="REPORTING":
            messages.error(request,'Please Enter Valid Role')
            return redirect("register")
        else:
            if(role=='ADMIN'):
                user=data.objects.create_superuser(name=name,username=username,password=password,role=role)
            else:
                user=data.objects.create_user(name=name,username=username,password=password,role=role)
        return redirect("startop")
def pregister(request):
    srfid=request.POST['SRFID']
    bcode=request.POST['bcode']
    pname=request.POST['pname']
    mobno=request.POST['mobno']
    age=request.POST['age']
    gender=request.POST['gender']
    address=request.POST['address']
    ccode=request.POST['ccode']
    dname=request.POST['dname']
    rem=request.POST['rem']
    cexe=request.POST['cexe']
    email=request.POST['email']
    loc=request.POST['loc']
    runid=request.POST['runid']
    runclk=request.POST['runtime']
    icmrup=request.POST['icmrup']
    accid=request.POST['accid']
    res=request.POST['res']
    ctval=request.POST['ctval']
    runstat=request.POST['runstat']
    patient=pdata(srfid=srfid,bcode=bcode,pname=pname,mobno=mobno,age=age,gender=gender,address=address,ccode=ccode,dname=dname,rem=rem,cexe=cexe,email=email,loc=loc,runid=runid,runtime=runclk,icmrup=icmrup,accid=accid,res=res,ctval=ctval,runstat=runstat)
    patient.save() 
    if runstat=='ER':
        endrun()
        #request.session['sampleCount']=0
    return HttpResponse()
def endrun():
    conn=p.connect(host="localhost",database="Base1",user="postgres",password="1234")
    cur=conn.cursor()
    cur.execute("UPDATE public.one_pdata SET runstat='ER' WHERE runstat='R';")
    conn.commit()   
    cur.close()
    conn.close()

def endday(request):
    conn=p.connect(host="localhost",database="Base1",user="postgres",password="1234")
    cur=conn.cursor()
    cur.execute("UPDATE public.one_pdata SET runstat='ED' WHERE id<=(select Max(id) from public.one_pdata);")
    conn.commit()   
    cur.close()
    conn.close()
    return HttpResponse()
def loaddb(request):
    name=request.user.username
    role=request.user.role
    srfid=request.POST['SRFID']
    bcode=request.POST['bcode']
    pname=request.POST['pname']
    mobno=request.POST['mobno']
    age=request.POST['age']
    gender=request.POST['gender']
    address=request.POST['address']
    ccode=request.POST['ccode']
    dname=request.POST['dname']
    rem=request.POST['rem']
    cexe=request.POST['cexe']
    email=request.POST['email']
    loc=request.POST['loc']
    runid=request.POST['runid']
    runclk=request.POST['runtime']
    icmrup=request.POST['icmrup']
    accid=request.POST['accid']
    res=request.POST['res']
    ctval=request.POST['ctval']
    conn=p.connect(host="localhost",database="Base1",user="postgres",password="1234")
    cur=conn.cursor()
    cur.execute("SELECT runid FROM public.one_pdata where id = (select Max(id) from public.one_pdata);")
    runid=cur.fetchone()
    cur.execute("SELECT runstat FROM public.one_pdata where id = (select Max(id) from public.one_pdata);")
    runstat=cur.fetchone()
    if request.is_ajax():
        print("ajax")
    else:
        if len(srfid)==13 and str(srfid).isnumeric():
            print("srfidpass")
            if len(mobno)==0 or (len(mobno)==10 and str(mobno).isnumeric()):
                print("mobnopass")
                if len(email)==0 or validateEmail(email):
                    print("emailpass")
                    if len(age)==0 or str(age).isnumeric():
                        print("agepass")
                        if len(runclk)==0 or str(runclk).isnumeric():
                            print("runtimepass")
                            if len(accid)==0 or str(accid).isnumeric():
                                print("accidpass")
                                if len(ctval)==0 or str(ctval).isnumeric():
                                    print("ctpass")
                                    if len(gender)==0 or gender=="Male" or gender=="Female" or gender=="Other":
                                        print("genpass")
                                        if len(icmrup)==0 or icmrup=="Yes" or icmrup=="No":
                                            print("icmrpass")
                                            if len(res)==0 or res=="Positive" or res=="Negative":
                                                print("respass")
                                                if len(bcode)>0:
                                                    print("bcodepass")
                                                    if len(pname)>0:
                                                        print("pnamepass")
                                                        if bool(pdata.objects.filter(srfid=srfid).exists()):
                                                            print("up")
                                                            upd="UPDATE public.one_pdata SET srfid=%s, bcode=%s, pname=%s, mobno=%s, age=%s, gender=%s, address=%s, ccode=%s, dname=%s, rem=%s, cexe=%s, email=%s, loc=%s, runtime=%s, icmrup=%s, accid=%s, res=%s, ctval=%s WHERE srfid=%s;"
                                                            cur.execute(upd,(srfid,bcode,pname,mobno,age,gender,address,ccode,dname,rem,cexe,email,loc,runclk,icmrup,accid,res,ctval,srfid))
                                                            conn.commit()
                                                        else:
                                                            print("ins")
                                                            #temp=request.session.get('sampleCount')
                                                            #request.session['sampleCount']=temp+1  
                                                            newdata=pdata(srfid=srfid,bcode=bcode,pname=pname,mobno=mobno,age=age,gender=gender,address=address,ccode=ccode,dname=dname,rem=rem,cexe=cexe,email=email,loc=loc,runid=runid[0],runtime=runclk,icmrup=icmrup,accid=accid,res=res,ctval=ctval,runstat=runstat[0])
                                                            newdata.save()
    if role=="SR":
        cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat='R';")
    elif role=="REPORTING":
        cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat='ER' and res='';")
    elif role=="RECEIVING":
        cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat!='ED' and accid=''")
    elif role=="ADMIN" :
        cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat!='ED'")
    sqlraw=cur.fetchall()
    dblen=len(sqlraw)
    sql=json.dumps(sqlraw)
    cur.execute("SELECT srfid, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email FROM public.one_regdata;")
    regdataraw=cur.fetchall()
    reglen=len(regdataraw)
    regdata=json.dumps(regdataraw)
    cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata;")
    chkdataraw=cur.fetchall()
    chkdatalen=len(chkdataraw)
    chkdata=json.dumps(chkdataraw)
    cur.close()
    conn.close()
    print("result")
    #sampleCount=request.session.get('sampleCount')
    return render(request,"result.html",{'result':name,'role':role,'sql':sqlraw,'dblen':dblen,'sqljson':sql,'regdata':regdata,'reglen':reglen,'runno':runid[0],'runstat':runstat[0],'chkdata':chkdata,'chklen':chkdatalen,})
def editrec(request):
    name=request.user.username
    role=request.user.role
    conn=p.connect(host="localhost",database="Base1",user="postgres",password="1234")
    cur=conn.cursor()
    cur.execute("SELECT runstat FROM public.one_pdata where id = (select Max(id) from public.one_pdata)")
    runstat=cur.fetchone()
    if runstat==None:
        runstat=['ED',]
    cur.execute("SELECT runid FROM public.one_pdata where id = (select Max(id) from public.one_pdata)")
    runno=cur.fetchone()
    if runno==None:
        runno=[1,]
    if role=="SR":
            cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat='R';")
    elif role=="REPORTING":
            cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat='ER' and res='';")
    elif role=="RECEIVING":
        cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat!='ED' and accid=''")
    elif role=="ADMIN" :
        cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat!='ED'")
    sqlraw=cur.fetchall()
    dblen=len(sqlraw)
    sql=json.dumps(sqlraw)
    cur.execute("SELECT srfid, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email FROM public.one_regdata;")
    regdataraw=cur.fetchall()
    reglen=len(regdataraw)
    regdata=json.dumps(regdataraw)
    cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata;")
    chkdataraw=cur.fetchall()
    chkdatalen=len(chkdataraw)
    chkdata=json.dumps(chkdataraw)
    cur.close()
    conn.close()
    #sampleCount=request.session.get('sampleCount')
    return render(request,"result.html",{'result':name,'role':role,'sql':sqlraw,'dblen':dblen,'sqljson':sql,'regdata':regdata,'reglen':reglen,'runno':runno[0],'runstat':runstat[0],'chkdata':chkdata,'chklen':chkdatalen,})
def startop(request):
    val1=request.user.username
    dbrole=request.user.role
    conn=p.connect(host="localhost",database="Base1",user="postgres",password="1234")
    cur=conn.cursor()
    cur.execute("SELECT runstat FROM public.one_pdata where id = (select Max(id) from public.one_pdata)")
    runstat=cur.fetchone()
    if runstat==None:
        runstat=['ED',]
    cur.execute("SELECT runid FROM public.one_pdata where id = (select Max(id) from public.one_pdata)")
    runno=cur.fetchone()
    if runno==None:
        runno=[1,]
    cur.close()
    conn.close()
    return render(request,"adminpage.html",{'result':val1,'role':dbrole,'runstat':runstat[0],'runno':runno[0]})
def dash(request):
    name=request.user.username
    role=request.user.role
    conn=p.connect(host="localhost",database="Base1",user="postgres",password="1234")
    cur=conn.cursor()
    cur.execute("SELECT runstat FROM public.one_pdata where id = (select Max(id) from public.one_pdata)")
    runstat=cur.fetchone()
    if runstat==None:
        runstat=['ED',]
    if runstat[0]=='R':
       runstat=['Running',] 
    elif runstat[0]=='ER':
       runstat=['Ended Run',]
    elif runstat[0]=='ED':
       runstat=['Ended Day',]
    cur.execute("SELECT runid FROM public.one_pdata where id = (select Max(id) from public.one_pdata)")
    runno=cur.fetchone()
    if runno==None:
        runno=[1,]
    cur.execute("SELECT count(*) FROM public.one_pdata where runstat='R' and rem!='NC';")
    SamplesInRun=cur.fetchone()
    cur.execute("SELECT count(*) FROM public.one_pdata where rem!='NC' and rem!='PC';")
    TotalSamplesTillDate=cur.fetchone()
    cur.execute("SELECT count(*) FROM public.one_pdata where res!='' and rem!='NC' and rem!='PC';")
    TotalSamplesReportedOn=cur.fetchone()
    cur.execute("SELECT count(*) FROM public.one_pdata where res='' and rem!='NC' and rem!='PC';")
    TotalSamplesPendingReport=cur.fetchone()
    cur.execute("SELECT count(*) FROM public.one_pdata where accid!='' and rem!='NC' and rem!='PC';")
    TotalSamplesAcc=cur.fetchone()
    cur.execute("SELECT count(*) FROM public.one_pdata where accid='' and rem!='NC' and rem!='PC';")
    TotalSamplesPendingAcc=cur.fetchone()
    cur.close()
    conn.close()
    return render(request,"dash.html",{'name':name,'role':role,'runstat':runstat[0],'runno':runno[0],'SiR':SamplesInRun[0],'TSTD':TotalSamplesTillDate[0],'TSRO':TotalSamplesReportedOn[0],'TSPR':TotalSamplesPendingReport[0],'TSA':TotalSamplesAcc[0],'TSPA':TotalSamplesPendingAcc[0]})
def exportdata(request):
    name=request.user.username
    role=request.user.role
    conn=p.connect(host="localhost",database="Base1",user="postgres",password="1234")
    cur=conn.cursor()
    cur.execute("SELECT srfid, bcode, pname, mobno, age, gender, address, ccode, dname, rem, cexe, email, loc, runid, runtime, icmrup, accid, res, ctval FROM public.one_pdata where runstat!='ED'")
    sqlraw=cur.fetchall()
    dblen=len(sqlraw)
    sql=json.dumps(sqlraw)
    cur.close()
    conn.close()
    return render(request,"exportdata.html",{'name':name,'role':role,'sql':sqlraw,'dblen':dblen,'sqljson':sql})
def  downloadexcel(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename="DbData.xls"'
    wb=x.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Covid Data')
    row_num=0
    font_style=x.XFStyle()
    font_style.font.bold=True
    
    columns=['SRFID','Barcode','Patient Name','Mobile Number','Age','Gender','Address','Client Code','Doctor Name','Remarks','Collection Executive','Email','Location','Run Number','Runtime','ICMR Update','AccessionID','Result','CTValue',]
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style=x.XFStyle()
    rows=pdata.objects.exclude(rem = "NC").exclude(rem = "PC").values_list('srfid','bcode','pname','mobno','age','gender','address','ccode','dname','rem','cexe','email','loc','runid','runtime','icmrup','accid','res','ctval')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,row[col_num],font_style)
    wb.save(response)
    return response
