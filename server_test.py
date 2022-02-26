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

            test_value = []
            self.database_test(test_value)

            reply = str(addr) + 'Thank you for connecting' + str(test_value[0])
            c.send(reply.encode())
            c.close()

    def database_test(self,test_value):
        try:
            with connection.cursor() as cursor:
                found = False
                cursor.execute('''SELECT * FROM User WHERE 1 ''')
                for e in cursor.fetchall():
                    test_value.append(e)
                    print(e)
                return test_value
        except NameError as error:
            pass

if __name__ == "__main__":
    booking_system_serverside()



