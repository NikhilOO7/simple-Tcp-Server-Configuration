from socket import *



serverName = gethostbyname('localhost')

serverPort = 8000



clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))



print("Connected to ", serverName, " at " + gethostbyname(serverName))





def main():

    authentication() #User Authentication



    print("\n","Quick Menu!")

    print("********************")

    print("1. Get organisation's name and Internet Protocol (IP)")

    print("2. Get Statistics(Mean, Median, Minimum, Maximum)")

    print("3. Sort Organisations List by Name or Minutes")

    print("4. Add new Organisation")

    print("5. Remove Organisation")

    print("6. Quit program","\n")



    while True :

        try:

            option = int(input("Enter your selected option (a number between 1 and 6): "))

            if option >=1 and option <=6:

                break

        except ValueError:

            print("") 



    option = str(option)

    clientSocket.send(option.encode("utf-8"))



    choice = option

    

    if choice == '1':

        searchSer = str(input("Enter Organisation's name: "))

        clientSocket.send(searchSer.encode("utf-8"))

        msgReceived = clientSocket.recv(1024)

        m = msgReceived.decode("utf-8")

        print(m)

        

    elif choice == '2':

        msgReceived = clientSocket.recv(1024)

        stats = msgReceived.decode("utf-8")

        print(stats)


    elif choice == '3':

        serverSort = input("How do you want to Sort the Organisations Data(Press name for Name / minutes for Minutes): ")

        clientSocket.send(serverSort.encode("utf-8"))

        msgReceived = clientSocket.recv(1024)

        m = msgReceived.decode("utf-8")

        print(m)



    elif choice == '4':

        serveradd = input("Enter Organisation name '-' domain name '-'"\

                            "IP Address '-' number of minutes"\

                            "(Ex: abcd-www.abcd.com-122.20.193.254-400): ")

        clientSocket.send(serveradd.encode("utf-8"))



        msgReceived = clientSocket.recv(1024)

        m = msgReceived.decode("utf-8")

        print(m)



        if m== "already exists":

            print("\n")

            print("Organisation already exists!")

            serveradd = input("Enter Organisation name '-' domain name '-'"\

                                "IP Address '-' number of minutes"\

                                "(Ex: psc-www.psc.com-192.168.10.2-500): ")            

            clientSocket.send(serveradd.encode("utf-8"))



            msgReceived = clientSocket.recv(1024)

            m = msgReceived.decode("utf-8")

            print(m)



            if m== "already exists":

                print("\n")

                print("Organisation already exists!")

                serveradd = input("Enter Organisation name '-' domain name '-'"\

                                    "IP Address '-' number of minutes"\

                                    "(Ex: psc-www.psc.com-192.168.10.2-500): ")

                clientSocket.send(serveradd.encode("utf-8"))



                msgReceived = clientSocket.recv(1024)

                m = msgReceived.decode("utf-8")

                print(m)



                if m== "already exists":

                    print("Organisation already exists!")

                    print("Closing connection.")

                    clientSocket.close()



        clientSocket.close()

            

    elif choice == '5':

        search = input("Enter an organisation name to remove: ")

        clientSocket.send(search.encode("utf-8"))



        msgReceived = clientSocket.recv(1024)

        m = msgReceived.decode("utf-8")

        print(m)



        if m== "not found":

            print("\n")

            print("Organisation not found!")

            search = input("Enter an organisation name to remove: ")

            clientSocket.send(search.encode("utf-8"))



            msgReceived = clientSocket.recv(1024)

            m = msgReceived.decode("utf-8")



            if m== "not found":

                print("\n")

                print("Organisation not found!")

                search = input("Enter an organisation name to remove: ")

                clientSocket.send(search.encode("utf-8"))



                msgReceived = clientSocket.recv(1024)

                m = msgReceived.decode("utf-8")



                if m== "not found":

                    print("\n")

                    print("Organisation not found! Closing Connection")

                    



        clientSocket.close()

        

    elif choice == '6':

        print("Ending the program....")      



def authentication():



    msgReceived = clientSocket.recv(1024) 

    m = msgReceived.decode("utf-8")



    x=0

    while x<3:     

  

        if m== "file not found":

            print("An error occurred trying to read the file 'users.txt'. Closing connection.")

            clientSocket.close()

            break        



        messageToSend = input("Enter username and Password, separated by a space: ")

     

        clientSocket.send(messageToSend.encode("utf-8"))



        msgReceived = clientSocket.recv(1024)

        m = msgReceived.decode("utf-8")



        while m == "User already logged in.":

            print("User is already logged in. Please enter a different username.")



            messageToSend = input("Enter username and Password, separated by a space: ")

            print("\n")

            clientSocket.send(messageToSend.encode("utf-8"))



            msgReceived = clientSocket.recv(1024)

            m = msgReceived.decode("utf-8")



            

        if m == "not found":

            print("Wrong Username or Password!", "\n")

            x += 1



        elif m == "found":

            print ("User Authenticated. Welcome!")

            break



    if x==3:

        print("Wrong username/password entered 3 times. Closing connection.")

        clientSocket.close()





    



main()

