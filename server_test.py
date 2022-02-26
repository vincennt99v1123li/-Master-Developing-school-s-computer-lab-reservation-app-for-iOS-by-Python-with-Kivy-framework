import socket
import pymysql

connection = pymysql.connect(user='root',
                             password='',
                             db='comp5327test',
                             cursorclass=pymysql.cursors.DictCursor)


class booking_system_serverside():
    def __init__(self):
        s = socket.socket()
        print ("Socket created")
        port = 9000

        s.bind(('', port))
        print ("socket binded: %s" %(port))


        s.listen(5)
        print ("socket listening")

        while True:
            c, addr = s.accept()
            print ('Got connection from', addr )

            option = (c.recv(1024).decode("utf-8"))
            print(option)

            if option == "test":

                test_value = []
                self.database_test(test_value)
                reply = str(addr) + 'Thank you for connecting' + str(test_value[0])
                c.send(reply.encode('utf-8'))
                c.close()

            elif option == "login":

                reply = 'OK'
                c.send(reply.encode('utf-8'))

                input_username = (c.recv(1024).decode("utf-8"))
                reply2 = 'input_username received'
                c.send(reply2.encode('utf-8'))
                input_pw = (c.recv(1024).decode("utf-8"))

                #print(input_username)
                #print(input_pw)

                login_reply = ""
                reply3 = str(self.login_check(input_username,input_pw,login_reply))

                #print(reply3)
                c.send(reply3.encode('utf-8'))

                c.close()

            else:
                c.close()

    def database_test(self,test_value):
        try:
            with connection.cursor() as cursor:
                found = False
                cursor.execute('''SELECT * FROM User WHERE 1 ''')
                for e in cursor.fetchall():
                    test_value.append(e)
                    #print(e)
                return test_value
        except NameError as error:
            pass

    def login_check(self,input_username,input_pw,login_reply):
        try:
            with connection.cursor() as cursor:
                #print(login_reply)
                sql = '''SELECT Password FROM User WHERE Username = "'''+str(input_username)+'''"'''
                cursor.execute(sql)

                for e in cursor.fetchall():
                    #print(e)
                    str_e = str(e)

                length_e = len(str_e)
                #print(length_e)
                #print(str_e[14:length_e-2])
                valid_pw = (str_e[14:length_e-2])

                if valid_pw == str(input_pw):
                    #print("test")
                    login_reply = "True"
                else:
                    login_reply = "False"
                #print(login_reply)
                return login_reply
        except NameError as error:
            pass

if __name__ == "__main__":
    booking_system_serverside()



