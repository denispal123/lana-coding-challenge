# import socket programming library 
import socket 
  
# import thread module 
from _thread import *
import threading 
  
print_lock = threading.Lock() 
  
products = {"PEN": 5.00,
            "TSHIRT": 20.00,
            "MUG": 7.5}
baskets = {}


# thread function 
def threaded(c): 
    basketNum = 0
    total = 0

    while True: 
  
        dataString = (
                    "\nSelect an option(1-4):\n"
                    "1. Create a new checkout basket\n"
                    "2. Add a product to a basket\n"
                    "3. Get the total amount in a basket\n"
                    "4. Remove the basket\n")
        # send back reversed string to client 
        c.send(dataString.encode('utf-8')) 

        option = int(c.recv(1024).decode('ascii'))

        if option == 1:
            basketNum = createBasket(basketNum)
            c.send(("Your basket has been created! Basket Number is " + str(basketNum) + "\n").encode('utf-8'))
        
        elif option == 2:
            if len(baskets.keys()) != 0:
                c.send(("In which basket do you want to add your product?" + str(list(baskets.keys())) + "\n").encode('utf-8'))
                chosenBasket = int(c.recv(1024).decode('ascii'))
                
                baskets[chosenBasket] = addProduct(c, baskets[chosenBasket])
                c.send((baskets[chosenBasket][-1] + " has been added to your basket!\n").encode('utf-8'))
            else:
                c.send("You don't have a basket!\n".encode('utf-8'))
        
        elif option == 3:
            if len(baskets.keys()) != 0:
                c.send(("Which basket's total do you want to calculate?" + str(list(baskets.keys())) + "\n").encode('utf-8'))
                chosenBasket = int(c.recv(1024).decode('ascii'))                
                
                total = totalCost(c, baskets[chosenBasket])
                
                c.send(("items: " + ",".join(baskets[chosenBasket]) + "\n" + str(total) + "€ is your total bill!\n").encode('utf-8'))
            else:
                c.send("You don't have a basket!\n".encode('utf-8'))     

        elif option == 4:
            if len(baskets.keys()) != 0:
                c.send(("Which basket do you want to remove?" + str(list(baskets.keys())) + "\n").encode('utf-8'))
                chosenBasket = int(c.recv(1024).decode('ascii'))                
                
                removeBasket(chosenBasket)
                
                c.send(("Your basket with ID " + str(chosenBasket) +" has been removed!\n").encode('utf-8'))
            else:
                c.send("You don't have a basket!\n".encode('utf-8')) 


        ans = str(c.recv(1024).decode('utf-8'))
        if ans != "y": 
            print('Bye') 
              
            # lock released on exit 
            print_lock.release() 
            break
        
    # connection closed 
    c.close() 
  
def createBasket(num):
    num += 1
    baskets[num] = []
    return num 

def removeBasket(chosenBasket):
    del baskets[chosenBasket]
    

def addProduct(c, basket):

    options = (
            "\nCode      	  | Name              |  Price\n"
            "-----------------------------------------------\n"
            "1. PEN            | Lana Pen          |   5.00€\n"
            "2. TSHIRT         | Lana T-Shirt      |  20.00€\n"
            "3. MUG            | Lana Coffee Mug   |   7.50€\n\n\n"
            "Select the product number you wish to add(1-3):\n"
            )

    #sending options to the client 
    c.send(options.encode('utf-8'))

    option = int(c.recv(1024).decode('ascii'))
    print("option: ", option)

    basket.append(list(products.keys())[option - 1])
    return basket

def totalCost(c, basket):
    tshirt = 0
    pens = 0
    mugs = 0
    if basket.count("TSHIRT") >= 3:
        tshirt = products["TSHIRT"] * 0.75 * basket.count("TSHIRT")
    else: 
        tshirt = products["TSHIRT"] * basket.count("TSHIRT")

    pens = products["PEN"] * basket.count("PEN") - (products["PEN"] * (basket.count("PEN")//3))  

    mugs = products["MUG"] * basket.count("MUG")

    print(pens, tshirt, mugs)

    return tshirt + pens + mugs


def Main(): 
    host = "" 
    port = 12344
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("socket binded to port", port) 
  
    # put the socket into listening mode 
    s.listen(5) 
    print("socket is listening") 
  
    # a forever loop until client wants to exit 
    while True: 
  
        # establish connection with client 
        c, addr = s.accept() 
  
        # lock acquired by client 
        print_lock.acquire() 
        print('Connected to :', addr[0], ':', addr[1]) 
  
        # Start a new thread and return its identifier 
        start_new_thread(threaded, (c,)) 
    s.close() 
  
if __name__ == '__main__': 
    Main()
