import socket
import os.path
import time

def main():

    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = ''
    port = 32500
    count = 0

    FileExtensions = []
    
    ServerSocket.bind((host,port))
    ServerSocket.listen(3)

    # server acception
        
    c, addr = ServerSocket.accept()

    print("Connection from: " + str(addr))
    print("=============================")
    
    while True:
        
        # receive file from client

        ReceivedFileName = c.recv(32768).decode()
        ReceivedFileExtension = ''.join(os.path.splitext(ReceivedFileName)[1:])

        ReceivedFileChunkNumbers = c.recv(32768)
        ReceivedFileChunkNumbers = int(ReceivedFileChunkNumbers)
        

        ReceivedFile = c.recv(32768)

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
                print("Client_Received_File", ReceivedFileExtension)
                print('=============================')
                print(count)

                if count == ReceivedFileChunkNumbers :
                    break
                
                ReceivedFile = c.recv(32768)
                
            print("Finished")
            count = 0
            ReFile.close()

        FileExtensions.append(ReceivedFileExtension)
            
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
        
        # send file to client

        SendFilePath = input('-> ')
        
        if SendFilePath == 'q':
            print("Finish Connection")
            break

        SendFile = open(SendFilePath, 'rb')
        SendFileExtension = str.encode(''.join(os.path.splitext(SendFilePath)))
        
        SendFileSize = os.path.getsize(SendFilePath)
        SendFileChunkNumbers = str.encode(str(int(SendFileSize / 32768) + 1))

        c.send(SendFileExtension)
        c.send(SendFileChunkNumbers)

        time.sleep(0.8)
        
        SendLoad = SendFile.read(32768)
        c.send(SendLoad)

        while(SendLoad) :
            print("Sent : ", SendFileExtension.decode())
            print("=============================")
            SendLoad = SendFile.read(32768)

            c.send(SendLoad)

        print("Sent Finished")
        SendFile.close()
            
    c.close()

if __name__ == '__main__':
    main()
