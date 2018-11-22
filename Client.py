import socket
import os.path
import time

def main():
    
    host = '120.142.106.94' # External ip address
    port = 32500
    count = 0

    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ClientSocket.connect((host, port))

    FileExtensions = []

    SendFilePath = input("-> ")
    print("=============================")
    
    while SendFilePath != 'q':

        # send file to server

        SendFile = open(SendFilePath, 'rb')
        SendFileExtension = str.encode(''.join(os.path.splitext(SendFilePath)))
        
        SendFileSize = os.path.getsize(SendFilePath)
        
        SendFileChunkNumbers = str.encode(str(int(SendFileSize / 32768) + 1))

        ClientSocket.send(SendFileExtension)
        ClientSocket.send(SendFileChunkNumbers)

        time.sleep(0.8)
        
        SendLoad = SendFile.read(32768)
        ClientSocket.send(SendLoad)

        while(SendLoad) :
            print("Sent : ", SendFileExtension.decode())
            print("=============================")
            SendLoad = SendFile.read(32768)

            ClientSocket.send(SendLoad)

        print("Sent Finished")
        SendFile.close()
        
        # receive file from server

        ReceivedFileName = ClientSocket.recv(32768).decode()
        ReceivedFileExtension = ''.join(os.path.splitext(ReceivedFileName)[1:])

        ReceivedFileChunkNumbers = int(ClientSocket.recv(32768).decode())

        ReceivedFile = ClientSocket.recv(32768)

        # Finish Connection
        
        if not ReceivedFile :
            print("Finish Connection")
            break

        with open('Client_Received_File', 'wb') as ReFile :
            print("Get file from Client \n")
            
            print("File : ", ReceivedFileName)
            print("=============================")
            
            while True :
                count += 1
                
                print('receiving data...')
                ReFile.write(ReceivedFile)
                ReFile.truncate()
                
                print("Saving Finished")
                print('=============================')

                if count == ReceivedFileChunkNumbers :
                    break
                
                ReceivedFile = ClientSocket.recv(32768)
                
            print("Finished")
            count = 0
            ReFile.close()

        FileExtensions.append(ReceivedFileExtension)
        print(FileExtensions)
            
        if len(FileExtensions) > 2 :
            FileExtensions.remove(FileExtensions[0])
                
            os.remove("Client_Received_File" + FileExtensions[0])
            os.rename('Client_Received_File', 'Client_Received_File' + FileExtensions[1])

        elif len(FileExtensions) == 2 :
            os.remove("Client_Received_File" + FileExtensions[0])
            os.rename('Client_Received_File', 'Client_Received_File' + FileExtensions[1])

        else :
            if os.path.isfile("Client_Received_File" + ReceivedFileExtension) :
                os.remove("Client_Received_File" + ReceivedFileExtension)
                    
            os.rename('Client_Received_File', 'Client_Received_File' + FileExtensions[0])
                
        print("Convert Form Finished")
        print("=============================")
            
        SendFIlePath = input("-> ")

    print("Finsh Connection")
    print("=============================")
    ClientSocket.close()

if __name__ == '__main__':
    main()
