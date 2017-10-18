from socket import *

from threading import Thread





################# Authentication ######################



usersList = []      #users List created from txt file

usersList2 = []     #users List created for users that have signed in





def authentication():   



    connectionSocket.send("file found".encode("utf-8"))     # to allow the client program to continue if the txt file has been found 

    

    try: 

        usersfile = open("users.txt", 'r')



        noOfUsers = 0



        for user in usersfile:          # to create a list of users from "users.txt" file

            user=user.rstrip('\n')

            user=user.split()

            usersList.append(user)

            noOfUsers = noOfUsers + 1

              

        usersfile.close()

            

        NoOfTimesWrongUserNameEntered=0                     #to ensure that client is not allowed to

        while NoOfTimesWrongUserNameEntered <3 :            #enter the wrong username more than 3 times



            msgReceived = connectionSocket.recv(1024)

            decodedMessage = msgReceived.decode("utf-8")

            

            usernameAndPassword = decodedMessage

            usernameAndPassword = usernameAndPassword.split()

            username = usernameAndPassword [0]



            for user in usersList2:                         #to ensure that a client is not allowed to sign in with 

                while user == username:                     #a username that is already signed in

                    print("This user is already logged in.")

                    connectionSocket.send("User already logged in.".encode("utf-8"))



                    msgReceived = connectionSocket.recv(1024)

                    decodedMessage = msgReceived.decode("utf-8")

                    

                    usernameAndPassword = decodedMessage

                    usernameAndPassword = usernameAndPassword.split()

                    username = usernameAndPassword [0]

                              

            password = usernameAndPassword [1]                       



            userNo=0

            wrongUsername=0

            x=0

            while userNo < len(usersList):          #to allow the correct combination of usrname and password to be authenticated           

                if username == usersList[userNo][0] and password == usersList[userNo][1]:

                    print("User Authenticated.")

                    usersList2.append(username)                

                    connectionSocket.send("found".encode("utf-8"))

                    x=1

                    break                        

                else:

                    wrongUsername = wrongUsername +1                                           

                userNo += 1                              



            if len(usersList) == wrongUsername:

                print("Wrong username or password!")

                NoOfTimesWrongUserNameEntered += 1

                connectionSocket.send("not found".encode("utf-8"))

                

            if x==1:

                break



        if NoOfTimesWrongUserNameEntered == 3:

            print("Wrong entry 3 times. Closing connection.")                                 



    except IOError:                     #an exception will be raised if an error is encountered in opening the txt file                               

        print("An error occurred trying to read the file 'users.txt'")

        connectionSocket.send("file not found".encode("utf-8"))

        connectionSocket.close()                            





################### Menu ###########################



def menu():

   

    print("\n","Quick Menu!")

    print("********************")

    print("1. Get organisation's name and Internet Protocol (IP)")

    print("2. Get Statistics(Mean, Median, Minimum, Maximum)")

    print("3. Sort Organisations List by Name or Minutes")

    print("4. Add new Organisation")

    print("5. Remove Organisation")

    print("6. Quit program","\n")

    option = int((input("Enter your Selection(1-6): ",)))

    print("\n")

    return option



################### Menu 1 #########################



def serverConnection(search, serverL):

    try:

           

        for subL in serverL:

            if subL[0] == search:

                info= "Server name: " + str(subL[1]) + "   ,   IP address: " + str(subL[2])

                return info

        if subL[0] != search:

            return "Unknown organziation."

                    

    except TypeError:

        print("Type Error")

    except ValueError:

        print("Value Error")





################## Menu 2 #########################

                

def statSer(num, serverL):

    #To get mean of the Organisation

    total = 0

    for subL in serverL:

        total = total + int(subL[3])

    mean = total / num

    

    #To get median of the Organisation

    subL1 = []

    for subL in serverL:

        subL1.append(int(subL[3]))

    subL1.sort()

    

    if len(subL1)% 2 == 0:

        x1=len(subL1)//2

        x2=(len(subL1)+2)//2

        median = (subL1[x1-1] + subL1[x2-1])//2

        

    else:

        x=(len(subL1)+1)//2

        median = subL1[x-1]

        

    #To get maximum minutes of the Organisation

    maxi = int(serverL[0][3])

    #orgMaximum = '0'

    for subL in serverL:

        if int(int(subL[3]))> maxi:

            maxi = int(subL[3])

            #orgMaximum = str(subL[0])

            

    #To get minimum minutes of the Organisation

    mini = int(maxi)

    #orgMinimum = 0

    

    for subL in serverL:

        if int(int(subL[3]))< mini:

            mini = int(subL[3])

            #orgMinimum = subL[0]  

    

    return mean, median, mini, maxi



################## Menu 3 #########################

                

def dataSorting(serverL):

    #To get sorted file in ascending order according to organisation name

    msgReceived = connectionSocket.recv(1024)

    serverSort = msgReceived.decode("utf-8")

    newList = []

    subL0 = []

    subL1 = []


    if serverSort == "name":

        for subL in serverL:

            print ("subL is: ",subL)

            subL0.append(subL[0])

            subL0.sort()

        # print("sorted subL0: ",subL0)

        for item in subL0:

            print(item)

            for subL in serverL:

                if item == subL[0]:

                    print ("selected subL is: ",subL)

                    newList.append(subL)

        print ("sorted subL is: ", newList)

        outFile = open("organisations.txt", 'w')

        for lst in newList:
            lst = '\t'.join(lst)
            outFile.write(lst + "\n")

        outFile.close()

        print("Organisations.txt file has been sorted in ascending order according to names")

        # serverSocket.close()

        

    #To get sorted file in descending order according to the minutes

    if serverSort == "minutes":

        for subL in serverL:

            print ("subL is: ",subL)

            subL1.append(subL[3])

            subL1.sort(reverse=True)

        # print("sorted subL0: ",subL0)

        for item in subL1:

            print(item)

            for subL in serverL:

                if item == subL[3]:

                    print ("selected subL is: ",subL)

                    newList.append(subL)

        print ("sorted subL is: ", newList)

        outFile = open("organisations.txt", 'w')

        for lst in newList:
            lst = '\t'.join(lst)
            outFile.write(lst + "\n")

        outFile.close()

        print("Organisations.txt file has been sorted in descending order according to minutes")

        # serverSocket.close()

    return "File has been sorted!"


####################### Menu 4 ##########################



def serverAddition(serverL):



    tryAgain = 0

    attempts =3

    while tryAgain < 3:



        msgReceived = connectionSocket.recv(1024)

        serveradd = msgReceived.decode("utf-8")

        #serveradd = input("Enter Organisation name '-' domain name '-'\

                            #IP Address '-' number of minutes\

                            #(Ex: abcd-www.abcd.com-122.20.193.254-400): ")

        x = 0

        count = 0

        newList = serveradd.split('-')



        

        for subL in serverL:

            if subL[0] == newList[0]:



                print("Organisation already exists")



                connectionSocket.send("already exists".encode("utf-8"))

                tryAgain += 1



                print("Attempts left: ", attempts)

                attempts -= 1

                

            else:

                count+=1



        if count == len(serverL):

            serverL.append(newList)

            print("Orgainsation has been added.")

            connectionSocket.send("Added".encode("utf-8"))

            break



   # serverSocket.close()

    

    outFile = open("organisations.txt", 'a')

    newList= '\t'.join(newList)

    outFile.write("\n" + newList)

    outFile.close()



############################## Menu 5 ############################   

    

def serverRemove(serverL):



    tryAgain = 0

    reverse = 2



    while tryAgain<3:



        msgReceived = connectionSocket.recv(1024)

        search = msgReceived.decode("utf-8")



        x=0

        count=0

        

        for subL in serverL:

            if subL[0] == search:

                               

                del serverL[count]

                print("Organisation "+ search + " removed from the list.")

                connectionSocket.send("found".encode("utf-8"))

                x=1

                break

                           

            else:

                count += 1

                

        if count == len(serverL):

        

            print("Organisation not found")

            connectionSocket.send("not found".encode("utf-8"))

            tryAgain += 1

            print(reverse, "attempts left.")

            reverse -= 1

            

        if x==1:

            break



    listToFile(serverL, "organisations.txt")

      



def listToString(subL):

    string = ''



    for sub in subL:

        string += sub + ' '



    return string.rstrip()

        

def listToFile(serverL, filename):

    outfile = open("organisations.txt", 'w') 



    for subL in serverL:

        outfile.write(listToString(subL) + '\n')

        

    outfile.close()





########################### Client Handler ##################





class ClientHandler (Thread):



    def __init__(self, client):

        Thread.__init__(self)

        self.__client = client

        



    def run(self):

        

        print("usersList2 = ", usersList2)

            

        authentication() #User Authentication



              

            

        try:

            print("usersList2 = ", usersList2)



            

            infile = open("organisations.txt", 'r')

        

            serverList = []

            numOrg = 0

            for line in infile:

                linelist = (line.rstrip()).split()

                serverList.append(linelist)

                numOrg += 1

            infile.close()



            msgReceived = connectionSocket.recv(1024)

            choice = msgReceived.decode("utf-8") 



            if choice == '1':

                msgReceived = connectionSocket.recv(1024)

                searchSer = msgReceived.decode("utf-8") 

                info  = serverConnection(searchSer, serverList)

                info=str(info)

                print("info:", info)

                connectionSocket.send(info.encode("utf-8"))

                

            elif choice == '2':



                mean, median, minimum, maximum = statSer(numOrg, serverList)

                mean= str(mean)

                median = str(median)

                minimum = str(minimum)

                maximum = str(maximum)

                stats = ("The mean of number of minutes is: "+ mean \

                   + "\n" + "The median of number of minutes is: " + median \

                   + "\n" + "Organisation with minimum number of minutes is: " + minimum \

                   + "\n" + "Organisation with maximum number of minutes is: " + maximum)

                print(stats)

                connectionSocket.send(stats.encode("utf-8"))




            elif choice == '3':

             

                dataSorting(serverList)

                connectionSocket.send("Sorted!".encode("utf-8"))

                

            elif choice == '4':

             

                serverAddition(serverList)
                connectionSocket.send("Organization Added!".encode("utf-8"))



            elif choice == '5':



                serverRemove(serverList)
                connectionSocket.send("Organization Removed!".encode("utf-8"))
        

            elif choice == '6':

                print("Ending the program....")

                connectionSocket.close()



        except IOError:

            print("File Not Found.")

           

serverName = gethostbyname('localhost')

serverPort = 8000

address = (serverName, serverPort)

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(address)

serverSocket.listen(5)



while True:

    print("Waiting for connection . . . ")

    connectionSocket, address = serverSocket.accept()

    print("... connected from: ", address)

    handler = ClientHandler(connectionSocket)

    handler.start()







