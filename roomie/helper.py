def iscollege(filename):
	try:
		file=open("./colleges/"+filename,"r")
		file.close()
		return True
	except:
		return False

def isuser(username,filename):
	i=0
	file=open("./colleges/"+filename,"r")
	for line in file:
		if(i!=0):
			line=line.rstrip("\n")
			user=line[:line.find("^")]
			if(username==user):
				return True
		i+=1
	return False

def isemail(email,filename):
	i=0
	file=open("./colleges/"+filename,"r")
	for line in file:
		if(i!=0):
			line=line.rstrip("\n")
			commaindex=line.find("^")
			commaindex=line.find("^",commaindex+1)
			commaindex=line.find("^",commaindex+1)
			commaindex=line.find("^",commaindex+1)
			mail=line[commaindex+1:line.find("^",commaindex+1)]
			if(email==mail):
				return True
		i+=1
	return False

def sorting(list1):
    list2=[]
    count1=[]
    
    for i in range(len(list1)-1):
        for t in range(i+1,len(list1),1):
            count=0
            for j in range(len(list1[0])):
                           if(list1[i][j]==list1[t][j]):
                               count=count+1
            count1.append([list1[i][0],list1[t][0],count])
    count1=sorted(count1,key=lambda l:l[2],reverse=True)
    paired_list=[]
    for i in range(len(count1)):
        if (count1[i][0] not in paired_list) and (count1[i][1] not in paired_list):
            paired_list.append(count1[i][0])
            paired_list.append(count1[i][1])
    return paired_list

def findname(file,email):
	file=open(file,"r")
	i=0
	for line in file:
		if(i!=0):
			line=line.rstrip("\n")
			commaindex=line.find("^")
			name=line[:commaindex]
			commaindex=line.find("^",commaindex+1)
			commaindex=line.find("^",commaindex+1)
			commaindex=line.find("^",commaindex+1)
			emailadd=line[commaindex+1:line.find("^",commaindex+1)]
			if(emailadd==email):
				return name
		i+=1



