#-------------------------------------------------
#--------Grade Distribution Analyzer V1.1---------
#-------------------------------------------------
#-----------------By Aaron Porter-----------------
#--------------------11/02/16---------------------
#-------------------------------------------------

#---------
#-Imports-
#---------

import csv
import os
import webbrowser
import time

#------------------------
#-------Class List-------
#------------------------

#prints out the list of text files in current directory
directory = os.listdir()
print("Here are the text files you can load.")
print("-"*40)

for item in directory:
        if ".txt" in item:
                print(item)
                print("-"*40)

#tries to open the text file if unsuccessful it tells the user to retry
while True:
        try:
        
            classfile = open(input("Which file of slides would you like to use? ")+".txt","r")
            classes = classfile.readlines()
            classfile.close()
            break
        except:
            print("That file does not appear to be there, try again!")
            print("You do not need to add .txt to you file name.")



#creates a count
classcounter=0
prelink = "http://gradedistribution.registrar.indiana.edu/exportToSpreadsheet.php?&dept={0}&subject={1}&crse={2}&c=desc&r=gradedist%20target="

#takes class department and number
for item in classes:
    try:
        item = item.strip()
        item = item.split()
        print(item)
        dept = item[0].split("-")
        link = prelink.format(dept[0],dept[1],item[1])

    except:
            
        pass

    try:

        #opens the link that downloads it and adds one to number of files downloaded
        webbrowser.open_new_tab(link)
        classcounter +=1

    except:

        #if theres an issue with any class just skip it
        pass

    
#gets current directory
cwd = os.getcwd()
#Moves up a directory
parts = cwd.split("\\")
parts.remove(parts[-1])
csvDir = '\\'.join(parts)
#changes current working directory to Downloads
os.chdir(csvDir)

#---------------
#----Loading----
#---------------

#Compiles a list of the files to use
fileLst = []

# Using a while loop to allow time to download
while True:
    #for file in downloads
    for file in os.listdir(os.getcwd()):
        #if file has the name the downloaded would have
         if "reportID_gradedist" in file:
             #if that file is not already in the list
             if file not in fileLst:
                 #add to the list
                 fileLst.append(file)
    #if we have downloaded all the files it allows code to continues
    if len(fileLst) == classcounter:
        break
    #if it doesnt print loading and try again in 5 seconds
    else:
        load = "Loading"
        for i in range(5):
            print(load)
            time.sleep(1)
            load+="."
        
#Tells user loading is compelete
print("Loading Complete\n\n")

#----------------------
#-Calculate GPA Totals-
#----------------------

gradedist = {}
#for every file in fileLst
for csvFile in fileLst:
    #open the file
    file = open(csvFile,"r")
    #read all the rows
    contents = list(csv.reader(file))
    file.close()
    #set the class and student gpas back to zero
    classGPAtotal = 0.0
    studentGPAtotal = 0.0
    #remove the header line
    contents.remove(contents[0])
    #to compute the total classes added
    counter = 0
    
    #Going through each row of a certain file
    for i in range(len(contents)):
        #if the row is not empty
        if contents[i]:

            #if its the first row
            if i == 0:

                #create the class name
                className = ((contents[i][5].strip())+' '+contents[i][6])

            
            try:

                #Add the student and class gpas to the running total
                classGPAtotal += float(contents[i][12])
                studentGPAtotal += float(contents[i][13])
                #add one to the counter
                counter+=1

                #Add class name to dictionary if its not already
                if className not in gradedist:
                    gradedist[className] = 0
            #any errors skip the line
            except:
                pass
        #if its the last row
        if i == (len(contents)-1):

            #Calculate the difference of the Average Class GPA and Average Student GPA
            try:
                gradedist[className] = ((classGPAtotal/counter)-(studentGPAtotal/counter))
            #If it cannot calculate let the user know
            except:
                print(className, "info could not be calculated!")
                print()


#------------
#--Printing--
#------------
    
#Makes a list of tuples of the class name and difference
finishedLst = []
for item in gradedist.items():
    if item[0]:
        finishedLst.append((item[1],item[0]))

#sorts it so highest comes first
finishedLst.sort(reverse = True)

#makes it print pretty
print("These classes are your best bet:")
print("Rank\tClass\t\tBenefit")
print("-"*32)

#prints top 10 
for i in range(10):
    print( str(i+1) +"\t" + finishedLst[i][1] + "\t" + str(finishedLst[i][0])[0:6])

#removes the files we used
for item in fileLst:
    os.remove(item)

#lets window stay open
print()
input("Press Enter to Exit")
