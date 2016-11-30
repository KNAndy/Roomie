from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import helper
from hashlib import md5
import string
import os
from django.views.static import serve

"""
register college
register student
open college profile in student dash - messy
"""

activecollegecode=None
activeuseremail=None
clgname=None
clgadd=None
clgphone=None
clgdir=None
clgyear=None
nos=None
nor=None
reg=None
userid=None
usergender=None
userroll=None
userphone=None
useradd=None
studentkey="is-active"
collegekey=""
clgdasherror=""
filepath=None
roomie="--"
collegename=None

def download(request):
	global filepath
	return serve(request,os.path.basename(filepath),os.path.dirname(filepath))

def passauth(request):
	global clgname,clgadd,clgphone,clgdir,clgyear,nos,nor,reg,clgdasherror
	if request.method=="POST":
		passauth=request.POST.get("passauth")
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			line=line.rstrip("\n")
			break
		commaindex=line.find("^")
		line=line[commaindex+1:line.find("^",commaindex+1)]
		file.close()
		if(line==md5(passauth.encode()).hexdigest()):
			return HttpResponseRedirect("/college_dashboard/pairings/")
		return render(request,"roomie/collegedashboard.html",{"clgname":clgname,"clgcode":activecollegecode,"clgadd":clgadd,"clgphone":clgphone,"clgdir":clgdir,"clgyear":clgyear,"nos":nos,"nor":nor,"studname":"--","studgender":"--","studemail":"--","studphone":"--","studadd":"--","roomie":"--","mode1":"","mode2":"is-active","mode3":"","altmode1":"","altmode2":"is-active","submode1":"is-active","submode2":"","registrations":reg,"errorcode":clgdasherror})

def showquestionnaire(request):
	return render(request,"roomie/questions.html",{})

def pair(request):
	file=open("./colleges/"+str(activecollegecode)+"responses","r")
	maleresponselist=[]
	femaleresponselist=[]
	for line in file:
		line=line.rstrip("\n")
		line=line.split("^")
		if(line[0]=="male"):
			maleresponselist.append(line[1:])
		else:
			femaleresponselist.append(line[1:])
	file.close()
	file=open("./colleges/"+str(activecollegecode)+"status","w")
	file.write("paired")
	file.close()
	try:
		os.remove("./colleges/"+str(activecollegecode)+"pairedlist")
	except:
		pass
	try:
		os.remove("./colleges/"+str(activecollegecode)+"pairedemails")
	except:
		pass
	file=open("./colleges/"+str(activecollegecode)+"pairedlist","a")
	malepairedlist=helper.sorting(maleresponselist)
	femalepairedlist=helper.sorting(femaleresponselist)
	for i in range(0,len(malepairedlist)-1,2):
		file.write(helper.findname("./colleges/"+str(activecollegecode),malepairedlist[i])+" - "+helper.findname("./colleges/"+str(activecollegecode),malepairedlist[i+1])+"\n")
	for i in range(0,len(femalepairedlist)-1,2):
		file.write(helper.findname("./colleges/"+str(activecollegecode),femalepairedlist[i])+" - "+helper.findname("./colleges/"+str(activecollegecode),femalepairedlist[i+1])+"\n")
	file.close()
	file=open("./colleges/"+str(activecollegecode)+"pairedemails","a")
	for i in range(0,len(malepairedlist)-1,2):
		file.write(malepairedlist[i]+" "+malepairedlist[i+1]+"\n")
	for i in range(0,len(femalepairedlist)-1,2):
		file.write(femalepairedlist[i]+" "+femalepairedlist[i+1]+"\n")
	file.close()
	return HttpResponseRedirect("../")
	
def questionnaire(request):
	global activecollegecode,activeuseremail,usergender
	if request.method=="POST":
		opt1=request.POST.get("options-1","")
		opt2=request.POST.get("options-2","")
		opt3=request.POST.get("options-3","")
		opt4=request.POST.get("options-4","")
		opt5=request.POST.get("options-5","")
		opt6=request.POST.get("options-6","")
		opt7=request.POST.get("options-7","")
		opt8=request.POST.get("options-8","")
		opt9=request.POST.get("options-9","")
		opt10=request.POST.get("options-10","")
		file=open("./colleges/"+str(activecollegecode)+"responses","a")
		file.write(usergender+"^"+activeuseremail+"^"+opt1+"^"+opt2+"^"+opt3+"^"+opt4+"^"+opt5+"^"+opt6+"^"+opt7+"^"+opt8+"^"+opt9+"^"+opt10+"\n")
		file.close()
		return HttpResponseRedirect("../../student_dashboard/")

def main(request):
	global activecollegecode,studentkey,collegekey,clgdasherror
	clgdasherror=""
	studentkey="is-active"
	collegekey=""
	activecollegecode=None
	return render(request,'roomie/main.html',{})
def aboutus(request):
	global studentkey,collegekey,clgdasherror
	clgdasherror=""
	studentkey="is-active"
	collegekey=""
	return render(request,'roomie/aboutus.html',{})
def commonlogin(request):
	global studentkey,collegekey,clgdasherror
	clgdasherror=""
	return render(request,'roomie/commonlogin.html',{"studentkey":studentkey,"collegekey":collegekey})
def studentregister(request):
	if request.method=="POST":
		global activecollegecode,collegename
		activecollegecode=request.POST.get("collegecode","")
		if  helper.iscollege(activecollegecode):
			file=open("./colleges/"+str(activecollegecode),"r")
			for line in file:
				line=line.rstrip("\n")
				break
			line=line[:line.find("^")]
			collegename=line
			file.close()
			return render(request,'roomie/studentregister.html',{"clgname":collegename})
		else:
			return HttpResponseRedirect('../../')  									#invalid college code
				
def collegeregister(request):
	return render(request,'roomie/collegeregister.html',{})

def new_student(request):
	global activecollegecode,activeuseremail,userid,usergender,userroll,userphone,useradd,clgname,clgadd,clgdir,clgphone,clgyear,studentkey,collegekey,roomie,collegename
	if request.method=="POST":
		username=request.POST.get('username','')
		sex=request.POST.get('sex','')
		if(sex=="1"):
			sex="male"
		else:
			sex="female"		
		identity=request.POST.get('id','')		
		password=request.POST.get('password','')
		repass=request.POST.get('repass','')
		email=request.POST.get('email','')		
		if(helper.isuser(username,activecollegecode) or helper.isemail(email,activecollegecode)):
			return render(request,'roomie/studentregister.html',{"clgname":collegename})
		address=request.POST.get('address','')		
		phone=request.POST.get('phone','')		
		if(password!=repass or username=="" or password=="" or sex=="" or identity=="" or email=="" or address==""):
			return render(request,'roomie/studentregister.html',{"clgname":collegename})	
		userid=username	
		usergender=sex	
		userroll=identity
		activeuseremail=email	
		useradd=address		
		userphone=phone			
		file=open("./colleges/"+str(activecollegecode),"a")
		file.write(username+"^"+sex+"^"+identity+"^"+md5(password.encode()).hexdigest()+"^"+email+"^"+address+"^"+phone+"\n")
		file.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			line=line.rstrip("\n")
			break
		college=line
		commaindex=college.find("^")
		clgname=college[:commaindex]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgadd=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgphone=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgdir=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgyear=college[commaindex+1:]
		file.close()
		studentkey="is-active"
		collegekey=""

		try:
			file=open("./colleges/"+str(activecollegecode)+"pairedemails","r")
			mailid=None
			for line in file:
				line=line.rstrip("\n")
				line=line.split(" ")
				if(activeuseremail in line):
					if(activeuseremail==line[0]):
						mailid=line[1]
						break
					elif activeuseremail==line[1]:
						mailid=line[0]
						break
			if mailid==None:
				roomie="Not allocated"
			else:
				roomie=helper.findname("./colleges/"+str(activecollegecode),mailid)
			file.close()
		except:
			roomie="--"

		return HttpResponseRedirect("/studentregister/questionnaire")

def new_college(request):
	global activecollegecode,clgname,clgadd,clgphone,clgdir,clgyear,nos,nor,reg,studentkey,collegekey,clgdasherror
	if request.method=="POST":
		clgdasherror=""
		file=open("collegesequence.txt","r")
		for line in file:
			line=line.rstrip("\n")
			collegecode=int(line)+1
		file.close()
		name=request.POST.get('name','')
		password=request.POST.get('password','')
		repass=request.POST.get('repass','')
		email=request.POST.get('email','')
		address=request.POST.get('address','')
		phone=request.POST.get('phone','')
		nos=request.POST.get('nos','')
		nor=request.POST.get('nor','')
		file=open("./colleges/"+str(collegecode)+"status","w")
		file.write("notpaired")
		file.close()
		if(password!=repass or name=="" or password=="" or email=="" or address=="" or nos=="" or nor=="" or int(nos)>(2*int(nor))):
			return HttpResponseRedirect("../")
		file=open("./colleges/"+str(collegecode)+"pairedlist","w")
		file.write("Students have not been paired. Pair them and download again")
		file.close()
		file=open("./colleges/"+str(collegecode),"a")
		file.write(name+"^"+md5(password.encode()).hexdigest()+"^"+email+"^"+address+"^"+phone+"^"+nos+"^"+nor+"^--^--\n")
		file.close()
		file=open("collegesequence.txt","w")
		file.write(str(collegecode))
		file.close()
		activecollegecode=collegecode
		file3=open("./colleges/"+str(activecollegecode),"r")
		reg=0
		clgname=name
		clgadd=address
		clgphone=phone
		clgdir="--"
		clgyear="--"
		collegekey="is-active"
		studentkey=""
		return HttpResponseRedirect("/college_dashboard")

def stddash(request):
	
	global activeuseremail,activecollegecode,studentkey,collegekey,studentkey,collegekey,roomie
	if(request.method=="POST"):
		activecollegecode=None
		useremail=request.POST.get("email","")
		password=request.POST.get("password1","")
		collegecode=request.POST.get("collegecode1","")
		if(not helper.iscollege(collegecode)):
			return HttpResponseRedirect("../commonlogin")
		file=open("./colleges/"+str(collegecode),"r")
		i=0
		flag=0
		for line in file:
			line=line.rstrip("\n")
			if(i!=0):
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				hashpass=line[commaindex+1:line.find("^",commaindex+1)]
				commaindex=line.find("^",commaindex+1)
				email=line[commaindex+1:line.find("^",commaindex+1)]
				if(useremail==email and md5(password.encode()).hexdigest()==hashpass):
					file.close()
					commaindex=line.find("^")
					user=line[:commaindex]
					gender=line[commaindex+1:line.find("^",commaindex+1)]
					commaindex=line.find("^",commaindex+1)
					roll=line[commaindex+1:line.find("^",commaindex+1)]
					commaindex=line.find("^",commaindex+1)
					commaindex=line.find("^",commaindex+1)
					commaindex=line.find("^",commaindex+1)
					address=line[commaindex+1:line.find("^",commaindex+1)]
					commaindex=line.find("^",commaindex+1)
					phone=line[commaindex+1:]
					activeuseremail=email
					activecollegecode=collegecode
					studentkey="is-active"
					collegekey=""
					try:
						file=open("./colleges/"+str(activecollegecode)+"pairedemails","r")
						mailid=None
						for line in file:
							line=line.rstrip("\n")
							line=line.split(" ")
							if(activeuseremail in line):
								if(activeuseremail==line[0]):
									mailid=line[1]
									break
								elif activeuseremail==line[1]:
									mailid=line[0]
									break
						if mailid==None:
							roomie="Not allocated"
						else:
							roomie=helper.findname("./colleges/"+str(activecollegecode),mailid)
						file.close()
					except:
						roomie="--"
					return render(request,"roomie/studentdashboard.html",{"user":user,"gender":gender,"roll":roll,"phone":phone,"address":address,"clgname":clgname,"clgadd":clgadd,"clgphone":clgphone,"clgdir":clgdir,"clgyear":clgyear,"roomie":roomie})    	
			else:
				college=line
				commaindex=college.find("^")
				clgname=college[:commaindex]
				commaindex=college.find("^",commaindex+1)
				commaindex=college.find("^",commaindex+1)
				clgadd=college[commaindex+1:college.find("^",commaindex+1)]
				commaindex=college.find("^",commaindex+1)
				clgphone=college[commaindex+1:college.find("^",commaindex+1)]
				commaindex=college.find("^",commaindex+1)
				commaindex=college.find("^",commaindex+1)
				commaindex=college.find("^",commaindex+1)
				clgdir=college[commaindex+1:college.find("^",commaindex+1)]
				commaindex=college.find("^",commaindex+1)
				clgyear=college[commaindex+1:]

			i+=1
		file.close()
		return HttpResponseRedirect("../commonlogin")								

	else:
		global user,gender,roll,phone,address,clgname,clgadd,clgdir,clgphone,clgyear,roomie
		return render(request,"roomie/studentdashboard.html",{"user":userid,"gender":usergender,"roll":userroll,"phone":userphone,"address":useradd,"clgname":clgname,"clgadd":clgadd,"clgdir":clgdir,"clgphone":clgphone,"clgyear":clgyear,"roomie":roomie})

def clgdash(request):

	global activecollegecode,studentkey,collegekey,clgdasherror,filepath
	if(request.method=="POST"):
		activecollegecode=None
		clgdasherror=""
		username=request.POST.get("id","")
		password=request.POST.get("password2","")
		if(not helper.iscollege(str(username))):
			return HttpResponseRedirect("../commonlogin")

		try:
			file3=open("./colleges/"+str(username),"r")
			reg=0
			for line in file3:
				reg+=1
			reg-=1
			file3.close()
			file=open("./colleges/"+str(username),"r")
			curline=0
			for line in file:
				line=line.rstrip("\n")
				if(curline==0):
					college=line
				commaindex=line.find("^")
				hashpass=line[commaindex+1:line.find("^",commaindex+1)]
				print(password,hashpass,md5(password.encode()).hexdigest())
				if(md5(password.encode()).hexdigest()==hashpass):
					filepath="/home/nihesh/Documents/Andy's Linux/webdev/SM mini project/master/colleges/"+str(username)+"pairedlist"
					commaindex=college.find("^")
					clgname=college[:commaindex]
					commaindex=college.find("^",commaindex+1)
					commaindex=college.find("^",commaindex+1)
					clgadd=college[commaindex+1:college.find("^",commaindex+1)]
					commaindex=college.find("^",commaindex+1)
					clgphone=college[commaindex+1:college.find("^",commaindex+1)]
					commaindex=college.find("^",commaindex+1)
					nos=college[commaindex+1:college.find("^",commaindex+1)]
					commaindex=college.find("^",commaindex+1)
					nor=college[commaindex+1:college.find("^",commaindex+1)]
					commaindex=college.find("^",commaindex+1)
					clgdir=college[commaindex+1:college.find("^",commaindex+1)]
					commaindex=college.find("^",commaindex+1)
					clgyear=college[commaindex+1:]
					activecollegecode=username
					collegekey="is-active"
					studentkey=""
					return render(request,"roomie/collegedashboard.html",{"clgname":clgname,"clgcode":activecollegecode,"clgadd":clgadd,"clgphone":clgphone,"clgdir":clgdir,"clgyear":clgyear,"nos":nos,"nor":nor,"studname":"--","studgender":"--","studemail":"--","studphone":"--","studadd":"--","roomie":"--","mode1":"is-active","mode2":"","mode3":"","altmode1":"is-active","altmode2":"","submode1":"is-active","submode2":"","registrations":reg,"errorcode":clgdasherror})    			
				curline+=1
			file.close()
			return HttpResponseRedirect("../commonlogin")				
		
		except:
			return HttpResponseRedirect("../commonlogin") 	

	else:
		global clgname,clgadd,clgphone,clgdir,clgyear,nos,nor,reg
		return render(request,"roomie/collegedashboard.html",{"clgname":clgname,"clgcode":activecollegecode,"clgadd":clgadd,"clgphone":clgphone,"clgdir":clgdir,"clgyear":clgyear,"nos":nos,"nor":nor,"studname":"--","studgender":"--","studemail":"--","studphone":"--","studadd":"--","roomie":"--","mode1":"is-active","mode2":"","mode3":"","altmode1":"is-active","altmode2":"","submode1":"is-active","submode2":"","registrations":reg,"errorcode":clgdasherror})

	
def changemail(request):

	global activecollegecode,activeuseremail
	flag=0
	if(request.method=="POST"):
		newmail=request.POST.get("newmail")
		passwd=request.POST.get("passconfirm")
		file=open("./colleges/"+str(activecollegecode),"r")
		lineno=1
		i=0
		for line in file:
			if(i!=0):
				line=line.rstrip("\n")
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				hashpass=line[commaindex+1:line.find("^",commaindex+1)]
				commaindex=line.find("^",commaindex+1)
				email=line[commaindex+1:line.find("^",commaindex+1)]
				if(email==activeuseremail and md5(passwd.encode()).hexdigest()==hashpass):
					flag=1
					break
				lineno+=1
			i+=1
		if(flag==0):
			return HttpResponseRedirect("../")
		file.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		for line in file:
			if(curline==lineno):
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex2=line.find("^",commaindex+1)
				newstring=line[:commaindex+1]+newmail+line[commaindex2:]
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))	
		return HttpResponseRedirect("../../commonlogin")

def changename(request):
	global activecollegecode,activeuseremail,userid,usergender,userroll,userphone,useradd,clgname,clgadd,clgdir,clgphone,clgyear
	flag=0
	if(request.method=="POST"):
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			college=line.rstrip("\n")
			break
		commaindex=college.find("^")
		clgname=college[:commaindex]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgadd=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgphone=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgdir=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgyear=college[commaindex+1:]
		file.close()
		newname=request.POST.get("newname")
		file=open("./colleges/"+str(activecollegecode),"r")
		lineno=1
		i=0
		for line in file:
			if(i!=0):
				line=line.rstrip("\n")
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				email=line[commaindex+1:line.find("^",commaindex+1)]
				if(email==activeuseremail):
					flag=1
					break
				lineno+=1
			i+=1
		if(flag==0):
			return HttpResponseRedirect("../")
		file.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		for line in file:
			if(curline==lineno):
				extract=line
				commaindex=line.find("^")
				newstring=newname+line[commaindex:]
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		extract=extract.rstrip("\n")
		commaindex=extract.find("^")
		userid=newname
		usergender=extract[commaindex+1:extract.find("^",commaindex+1)]
		commaindex=extract.find("^",commaindex+1)
		userroll=extract[commaindex+1:extract.find("^",commaindex+1)]
		commaindex=extract.find("^",commaindex+1)
		commaindex=extract.find("^",commaindex+1)
		commaindex=extract.find("^",commaindex+1)
		useradd=extract[commaindex+1:extract.find("^",commaindex+1)]
		commaindex=extract.find("^",commaindex+1)
		userphone=extract[commaindex+1:]
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))
		return HttpResponseRedirect("/student_dashboard")

def changephone(request):
	global activecollegecode,activeuseremail,userid,usergender,userroll,userphone,useradd,clgname,clgadd,clgdir,clgphone,clgyear
	flag=0
	if(request.method=="POST"):
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			college=line.rstrip("\n")
			break
		commaindex=college.find("^")
		clgname=college[:commaindex]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgadd=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgphone=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgdir=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgyear=college[commaindex+1:]
		file.close()
		newphone=request.POST.get("newphone")
		file=open("./colleges/"+str(activecollegecode),"r")
		lineno=1
		i=0
		for line in file:
			if(i!=0):
				line=line.rstrip("\n")
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				email=line[commaindex+1:line.find("^",commaindex+1)]
				if(email==activeuseremail):
					flag=1
					break
				lineno+=1
			i+=1
		if(flag==0):
			return HttpResponseRedirect("../")
		file.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		for line in file:
			if(curline==lineno):
				extract=line
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				newstring=line[:commaindex+1]+newphone+"\n"
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		extract=extract.rstrip("\n")
		commaindex=extract.find("^")
		userid=extract[:commaindex]
		usergender=extract[commaindex+1:extract.find("^",commaindex+1)]
		commaindex=extract.find("^",commaindex+1)
		userroll=extract[commaindex+1:extract.find("^",commaindex+1)]
		commaindex=extract.find("^",commaindex+1)
		commaindex=extract.find("^",commaindex+1)
		commaindex=extract.find("^",commaindex+1)
		useradd=extract[commaindex+1:extract.find("^",commaindex+1)]
		commaindex=extract.find("^",commaindex+1)
		userphone=newphone
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))
		return HttpResponseRedirect("/student_dashboard")

def changeadd(request):
	global activecollegecode,activeuseremail,userid,usergender,userroll,userphone,useradd,clgname,clgadd,clgdir,clgphone,clgyear
	flag=0
	if(request.method=="POST"):
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			college=line.rstrip("\n")
			break
		commaindex=college.find("^")
		clgname=college[:commaindex]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgadd=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgphone=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgdir=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgyear=college[commaindex+1:]
		file.close()
		newadd=request.POST.get("newadd")
		file=open("./colleges/"+str(activecollegecode),"r")
		lineno=1
		i=0
		for line in file:
			if(i!=0):
				line=line.rstrip("\n")
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				email=line[commaindex+1:line.find("^",commaindex+1)]
				if(email==activeuseremail):
					flag=1
					break
				lineno+=1
			i+=1
		if(flag==0):
			return HttpResponseRedirect("../")
		file.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		for line in file:
			if(curline==lineno):
				extract=line
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				newstring=line[:commaindex+1]+newadd+line[line.find("^",commaindex+1):]
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		extract=extract.rstrip("\n")
		commaindex=extract.find("^")
		userid=extract[:commaindex]
		usergender=extract[commaindex+1:extract.find("^",commaindex+1)]
		commaindex=extract.find("^",commaindex+1)
		userroll=extract[commaindex+1:extract.find("^",commaindex+1)]
		commaindex=extract.find("^",commaindex+1)
		commaindex=extract.find("^",commaindex+1)
		commaindex=extract.find("^",commaindex+1)
		useradd=newadd
		print(newadd)
		commaindex=extract.find("^",commaindex+1)
		userphone=extract[commaindex+1:]
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))
		return HttpResponseRedirect("/student_dashboard")

def changepass(request):

	global activecollegecode,activeuseremail
	flag=0
	if(request.method=="POST"):
		oldpass=request.POST.get("oldpass")
		newpass=request.POST.get("newpass")
		newpassconfirm=request.POST.get("newpassconfirm")
		if(newpass!=newpassconfirm):
			return HttpResponseRedirect("../")
		file=open("./colleges/"+str(activecollegecode),"r")
		lineno=1
		i=0
		for line in file:
			if(i!=0):
				line=line.rstrip("\n")
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				hashpass=line[commaindex+1:line.find("^",commaindex+1)]
				commaindex=line.find("^",commaindex+1)
				email=line[commaindex+1:line.find("^",commaindex+1)]
				if(email==activeuseremail and md5(oldpass.encode()).hexdigest()==hashpass):
					flag=1
					break
				lineno+=1
			i+=1
		if(flag==0):
			return HttpResponseRedirect("../")
		file.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		for line in file:
			if(curline==lineno):
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				newstring=line[:commaindex+1]+md5(newpass.encode()).hexdigest()+line[line.find("^",commaindex+1):]
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))
		return HttpResponseRedirect("../../commonlogin")

def changecollegemail(request):

	global activecollegecode,clgdasherror
	flag=0
	if(request.method=="POST"):
		clgdasherror=""
		newmail=request.POST.get("newmail")
		passwd=request.POST.get("passconfirm")
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			line=line.rstrip("\n")
			commaindex=line.find("^")
			hashpass=line[commaindex+1:line.find("^",commaindex+1)]
			if(md5(passwd.encode()).hexdigest()==hashpass):
				flag=1
			break
		if(flag==0):
			return HttpResponseRedirect("../../commonlogin/")
		file.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		lineno=0
		for line in file:
			if(curline==lineno):
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				newstring=line[:commaindex+1]+newmail+line[line.find("^",commaindex+1):]
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))		
		return HttpResponseRedirect("../../commonlogin")

def changeclgpass(request):
	global activecollegecode,clgdasherror,clgname,clgadd,clgphone,clgdir,clgyear,nos,nor,reg
	flag=0
	if(request.method=="POST"):
		clgdasherror=""
		oldpass=request.POST.get("oldpass")
		newpass=request.POST.get("newpass")
		newpassconfirm=request.POST.get("newpassconfirm")
		if(newpass!=newpassconfirm):
			return HttpResponseRedirect("../../commonlogin")
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			line=line.rstrip("\n")
			commaindex=line.find("^")
			hashpass=line[commaindex+1:line.find("^",commaindex+1)]
			if(md5(oldpass.encode()).hexdigest()==hashpass):
				flag=1
			break
		file.close()

		if(flag==0):
			clgdasherror="True"
			return render(request,"roomie/collegedashboard.html",{"clgname":clgname,"clgcode":activecollegecode,"clgadd":clgadd,"clgphone":clgphone,"clgdir":clgdir,"clgyear":clgyear,"nos":nos,"nor":nor,"studname":"--","studgender":"--","studemail":"--","studphone":"--","studadd":"--","roomie":"--","mode1":"","mode2":"","mode3":"is-active","altmode1":"is-active","altmode2":"","submode1":"","submode2":"is-active","registrations":reg,"errorcode":clgdasherror})
		
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		lineno=0
		for line in file:
			if(curline==lineno):
				commaindex=line.find("^")
				newstring=line[:commaindex+1]+md5(newpass.encode()).hexdigest()+line[line.find("^",commaindex+1):]
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))		
		return HttpResponseRedirect("../../commonlogin")

def changeclgname(request):
	global activecollegecode,clgname,clgadd,clgphone,clgdir,clgyear,nos,nor,reg,clgdasherror
	flag=0
	if(request.method=="POST"):
		clgdasherror=""
		file3=open("./colleges/"+str(activecollegecode),"r")
		reg=0
		for line in file3:
			reg+=1
		reg-=1
		file3.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			college=line.rstrip("\n")
			break
		commaindex=college.find("^")
		clgname=college[:commaindex]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgadd=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgphone=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nos=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nor=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgdir=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgyear=college[commaindex+1:]
		file.close()
		newname=request.POST.get("newname")
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		lineno=0
		for line in file:
			if(curline==lineno):
				commaindex=line.find("^")
				newstring=newname+line[commaindex:]
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))
		clgname=newname	
		return HttpResponseRedirect("/college_dashboard")

def changeclgphone(request):
	global activecollegecode,clgname,clgadd,clgphone,clgdir,clgyear,nos,nor,reg,clgdasherror
	flag=0
	if(request.method=="POST"):
		clgdasherror=""
		file3=open("./colleges/"+str(activecollegecode),"r")
		reg=0
		for line in file3:
			reg+=1
		reg-=1
		file3.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			college=line.rstrip("\n")
			break
		commaindex=college.find("^")
		clgname=college[:commaindex]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgadd=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgphone=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nos=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nor=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgdir=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgyear=college[commaindex+1:]
		file.close()
		newphone=request.POST.get("newphone")
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		lineno=0
		for line in file:
			if(curline==lineno):
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex2=line.find("^",commaindex+1)
				newstring=line[:commaindex+1]+newphone+line[commaindex2:]
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))	
		clgphone=newphone
		return HttpResponseRedirect("/college_dashboard")

def changeclgadd(request):
	global activecollegecode,clgname,clgadd,clgphone,clgdir,clgyear,nos,nor,reg,clgdasherror
	flag=0
	if(request.method=="POST"):
		clgdasherror=""
		file3=open("./colleges/"+str(activecollegecode),"r")
		reg=0
		for line in file3:
			reg+=1
		reg-=1
		file3.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			college=line.rstrip("\n")
			break
		commaindex=college.find("^")
		clgname=college[:commaindex]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgadd=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgphone=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nos=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nor=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgdir=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgyear=college[commaindex+1:]
		file.close()
		newadd=request.POST.get("newadd")
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		lineno=0
		for line in file:
			if(curline==lineno):
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex2=line.find("^",commaindex+1)
				newstring=line[:commaindex+1]+str(newadd)+line[commaindex2:]
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))	
		clgadd=newadd
		return HttpResponseRedirect("/college_dashboard")

def changeclgyear(request):
	global activecollegecode,clgname,clgadd,clgphone,clgdir,clgyear,nos,nor,reg,clgdasherror
	flag=0
	if(request.method=="POST"):
		clgdasherror=""
		file3=open("./colleges/"+str(activecollegecode),"r")
		reg=0
		for line in file3:
			reg+=1
		reg-=1
		file3.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			college=line.rstrip("\n")
			break
		commaindex=college.find("^")
		clgname=college[:commaindex]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgadd=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgphone=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nos=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nor=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgdir=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgyear=college[commaindex+1:]
		file.close()
		newyear=request.POST.get("newyear")
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		lineno=0
		for line in file:
			if(curline==lineno):
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				newstring=line[:commaindex+1]+newyear+"\n"
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))
		clgyear=newyear	
		return HttpResponseRedirect("/college_dashboard")
	
def changeclgdir(request):
	global activecollegecode,clgname,clgadd,clgphone,clgdir,clgyear,nos,nor,reg,clgdasherror
	flag=0
	if(request.method=="POST"):
		clgdasherror=""
		file3=open("./colleges/"+str(activecollegecode),"r")
		reg=0
		for line in file3:
			reg+=1
		reg-=1
		file3.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			college=line.rstrip("\n")
			break
		commaindex=college.find("^")
		clgname=college[:commaindex]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgadd=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgphone=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nos=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nor=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgdir=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgyear=college[commaindex+1:]
		file.close()
		newdir=request.POST.get("newdir")
		file=open("./colleges/"+str(activecollegecode),"r")
		file2=open("./colleges/"+"temp","w")
		curline=0
		lineno=0
		for line in file:
			if(curline==lineno):
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex=line.find("^",commaindex+1)
				commaindex2=line.find("^",commaindex+1)
				newstring=line[:commaindex+1]+newdir+line[commaindex2:]
				file2.write(newstring)
			else:
				file2.write(line)
			curline+=1
		os.remove("./colleges/"+str(activecollegecode))
		os.rename("./colleges/temp","./colleges/"+str(activecollegecode))	
		clgdir=newdir
		return HttpResponseRedirect("/college_dashboard")

def search(request):
	global activecollegecode,clgdasherror
	flag=0
	if(request.method=="POST"):
		clgdasherror=""
		roll=request.POST.get("roll")
		file=open("./colleges/"+str(activecollegecode),"r")
		curline=0
		lineno=0
		for line in file:
			if(curline!=0):
				commaindex=line.find("^")
				commaindex=line.find("^",commaindex+1)
				rollno=line[commaindex+1:line.find("^",commaindex+1)]
				if(rollno==roll):
					line=line.rstrip("\n")
					flag=1
					commandindex=line.find("^")
					name=line[:commandindex]
					gender=line[commandindex+1:line.find("^",commandindex+1)]
					commandindex=line.find("^",commandindex+1)
					commandindex=line.find("^",commandindex+1)
					commandindex=line.find("^",commandindex+1)
					email=line[commandindex+1:line.find("^",commandindex+1)]
					commandindex=line.find("^",commandindex+1)
					address=line[commandindex+1:line.find("^",commandindex+1)]
					commandindex=line.find("^",commandindex+1)
					phone=line[commandindex+1:]
					break
			else:
				pass
			curline+=1
		file.close()
		file3=open("./colleges/"+str(activecollegecode),"r")
		reg=0
		for line in file3:
			reg+=1
		reg-=1
		file3.close()
		file=open("./colleges/"+str(activecollegecode),"r")
		for line in file:
			college=line.rstrip("\n")
			break
		commaindex=college.find("^")
		clgname=college[:commaindex]
		commaindex=college.find("^",commaindex+1)
		commaindex=college.find("^",commaindex+1)
		clgadd=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgphone=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nos=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		nor=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgdir=college[commaindex+1:college.find("^",commaindex+1)]
		commaindex=college.find("^",commaindex+1)
		clgyear=college[commaindex+1:]
		file.close()
		try:
			file=open("./colleges/"+str(activecollegecode)+"pairedemails","r")
			mailid=None
			for line in file:
				line=line.rstrip("\n")
				line=line.split(" ")
				if(email in line):
					if(email==line[0]):
						mailid=line[1]
						break
					elif(email==line[1]):
						mailid=line[0]
						break
			if mailid==None:
				roomie="Not allocated"
			else:
				roomie=helper.findname("./colleges/"+str(activecollegecode),mailid)
			file.close()
		except:
			roomie="--"
		if(flag==0):
			return render(request,"roomie/collegedashboard.html",{"clgname":clgname,"clgcode":activecollegecode,"clgadd":clgadd,"clgphone":clgphone,"clgdir":clgdir,"clgyear":clgyear,"nos":nos,"nor":nor,"studname":"--","studgender":"--","studemail":"--","studphone":"--","studadd":"--","roomie":"--","mode1":"","mode2":"is-active","mode3":"","altmode1":"is-active","altmode2":"","submode1":"is-active","submode2":"","registrations":reg,"errorcode":clgdasherror,"roomie":roomie})
		return render(request,"roomie/collegedashboard.html",{"clgname":clgname,"clgcode":activecollegecode,"clgadd":clgadd,"clgphone":clgphone,"clgdir":clgdir,"clgyear":clgyear,"nos":nos,"nor":nor,"studname":name,"studgender":gender,"studemail":email,"studphone":phone,"studadd":address,"roomie":"--","mode1":"","mode2":"is-active","mode3":"","altmode1":"is-active","altmode2":"","submode1":"is-active","submode2":"","registrations":reg,"errorcode":clgdasherror,"roomie":roomie})



