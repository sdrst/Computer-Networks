#Sam Durst
#10/4/19
import socket
import select
import sys


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create tcp client socket
    port = 12000
    ip = socket.gethostbyname('www.goatgoose.com')

    client.connect((ip, port))  # form the connection

    message = "HELLO \n"
    client.send(message.encode('utf-8'))  # Hardcoded handshake

    client.recv(1024)

    username = input("Enter username: ")
    psswd = input("Enter password: ")
    message2 = "AUTH:"+username+":"+psswd+"\n"  # Authentication
    client.send(message2.encode('utf-8'))
    resp = (client.recv(1024))

    while resp != b'AUTHYES\n':
        if resp == b'UNIQNO\n':
            print("User not unique, try again")
        else:
            print("Incorrect username and/or password.")  # Unlimited log in attempts
        username = input("Enter username: ")
        psswd = input("Enter password: ")
        message2 = "AUTH:" + username + ":" + psswd + "\n"
        client.send(message2.encode('utf-8'))
        resp = (client.recv(1024))

    s = [client]  # for the select method
    client.recv(1024)
    print("You are now authenticated")

    while True:
        print("Choose an option:\n1. List online users\n2. Send someone a message\n3. Sign off")
        x = True
        while x:
            ready = select.select([sys.stdin], [], [], .5)[0]  # Check every half a second for keyboard input
            if ready:   # if we are in this section incoming notifications will be queued
                sys.stdin.flush()  # housekeeping
                choice = input()

                if choice == '1':
                    message = "LIST\n"
                    client.send(message.encode('utf-8'))  # gets list of users online
                    print(client.recv(1024).decode('utf-8'))
                elif choice == '2':
                    to_user = input("User you would like to send a message to: ")
                    msg = input("Message: ")
                    message3 = "To:" + to_user + ":" + msg + '\n'  # Sending message
                    client.send(message3.encode('utf-8'))
                    print("Message sent.")
                else:
                    message = "BYE\n"
                    client.send(message.encode('utf-8'))  # Quits program when signout occurs
                    print("Signing out...")
                    client.close()
                    exit(0)
                x = False

            else:
                rd, wd, ed = select.select(s, [], [], .5)  # Probes socket every half a second for incoming data
                if len(rd) != 0:
                    rspnse = client.recv(1024).decode('utf-8')
                    if rspnse == "" or rspnse == "\n":  # cases determine type of notification, strip newline character
                        pass
                    elif rspnse[0:4] == "From":
                        print("Message from " + rspnse.split(":")[1] + ": " + rspnse.split(":")[2])
                    elif rspnse[0:6] == "SIGNIN":
                        print(rspnse.split(":")[1].rstrip() + " signed in.")
                    elif rspnse[0:7] == "SIGNOFF":
                        print(rspnse.split(":")[1].rstrip() + " signed out.")
                    else:
                        print(rspnse)


main()

