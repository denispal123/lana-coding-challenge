# Import socket module 
import socket 
  
  
def Main(): 
    # local host IP '127.0.0.1' 
    host = '127.0.0.1'
  
    port = 12344
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
    s.connect((host,port)) 
  
    while True:  
  
        # messaga received from server 
        data = s.recv(1024) 
    
        print(str(data.decode('utf-8'))) 

        #taking input from user
        inp = int(input("Enter Option Number:"))
        while inp < 1 or inp > 4:
            inp = int(input("Enter a VALID Option Number:")) 

        #sending option number to the server
        s.send(str(inp).encode('ascii'))  
    
        if inp == 1:
            message = str(s.recv(1024).decode('utf-8'))
            print(message)
        
        else:
            message = str(s.recv(1024).decode('utf-8'))
            print(message)  

            #taking input from user
            if message != "You don't have a basket!\n": 
                basketNum =  input()
                while not basketNum.isdigit or basketNum not in message:
                    basketNum =  input("Enter a VALID Basket number:")
                
                s.send(str(basketNum).encode('ascii'))
                
                message = str(s.recv(1024).decode('utf-8'))
                print(message) 
                    
                if inp == 2:
                    prodNum = int(input("Enter Product Number(1-3):"))
                    while prodNum < 1 or prodNum > 3:
                        prodNum = int(input("Enter a VALID Product Number:"))            

                    s.send(str(prodNum).encode('ascii'))

                    message = str(s.recv(1024).decode('utf-8'))
                    print(message)            

        # ask the client whether he wants to continue 
        ans = input('\nDo you want to continue(y/n) :') 
        if ans == 'y': 
            s.send(str(ans).encode('utf-8'))
            continue
        else:
            s.send(str(ans).encode('utf-8')) 
            break
    # close the connection 
    s.close() 
  
if __name__ == '__main__': 
    Main() 