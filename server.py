student_name = "Kon Yuen Lam"
student_id = "12669130"

# Write code below
import json
from flask import Flask, jsonify, request
app = Flask(__name__)
import os.path
import socket, hashlib
import threading

HOST = "time-b-b.nist.gov"
PORT = 13
lock = threading.Lock()

#Server execution ID function
def exe_id(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            data = s.recv(1024)
            exe_id = hashlib.sha256(data).hexdigest()
            s.close()       
            return exe_id


#declare a file name
fname = "product.txt"

#Credit card and amount
creditcardNum = [
    {"creditCardid":"1111111111111111"}
]
amount = 10000

#if file not exist, create a new file 
if os.path.isfile(fname):
    print("welcome to shopping application")
else:
    f=open(fname,"w")
    product = [{                    #product list
            "id" : 1,
            "desc" : "apple",
            "UnitPrice" : 10,
            "QuantityInStock" : 20
        }, {
            "id" : 2,
            "desc" : "orange",
            "UnitPrice" : 12,
            "QuantityInStock" : 32
        }, {
            "id" : 3,
            "desc" : "water",
            "UnitPrice" : 5,
            "QuantityInStock" : 40
        }, {
            "id" : 4,
            "desc" : "wine",
            "UnitPrice" : 230,
            "QuantityInStock" : 46
        }, {
            "id" : 5,
            "desc" : "gameboy",
            "UnitPrice" : 540,
            "QuantityInStock" : 60
        }, {
            "id" : 6,
            "desc" : "ps5",
            "UnitPrice" : 3980,
            "QuantityInStock" : 10
        }, {
            "id" : 7,
            "desc" : "ps5 controller",
            "UnitPrice" : 590,
            "QuantityInStock" : 59
        }, {
            "id" : 8,
            "desc" : "banana",
            "UnitPrice" : 13,
            "QuantityInStock" : 12
        }, {
            "id" : 9,
            "desc" : "iphone 5s",
            "UnitPrice" : 3500,
            "QuantityInStock" : 33
        }, {
            "id" : 10,
            "desc" : "suger",
            "UnitPrice" : 5,
            "QuantityInStock" : 200
        }                          
    ]
    for i in range(len(product)):
        productwrite = json.dumps(product[i])
        f.write(productwrite +"\n")  #write the product list to the file      
    f.close()

#open the file product.txt and read the file.
f= open(fname,"r")
product = f.readlines()

#empty list for storing the product list by the JSON format
currentcontent=[] 
for i in range(len(product)):
    content= json.loads(product[i])
    currentcontent.append(content)
f.close()

#function for display all product's variable
@app.route("/showAll", methods=["GET"])
def showAll():

    #genarate an execution ID for each response
    exeid = exe_id(HOST,PORT) 

    #get the list of product
    global currentcontent
    item = json.dumps(currentcontent)   
    return jsonify({"exeid":exeid},"The all product on the online store:",item ) 

#function for query by the input id
@app.route("/QueryProduct", methods=["POST"])
def QueryProduct():

    # request the data
    data = json.loads(request.data) 
    id = data.get("id")

    #genarate an execution ID for each response
    exeid = exe_id(HOST,PORT) 
    global currentcontent

    #condition for checking id
    try:
        int(id)
    except:
        return jsonify({"exeid": exeid},{"error": "missing product id"}), 400 

    #if the id is equal to the input id by the user, it will corresponding display the required id. 
    # Otherwise, the error 404 will be shown
    for i in range(len(currentcontent)):      
        if int(id) == int(currentcontent[i]["id"]): 
            item = { "status": "success", "id":  currentcontent[i]["id"], "desc": currentcontent[i]["desc"],
                        "UnitPrice" : currentcontent[i]["UnitPrice"],
                         "Quanitiy" : currentcontent[i]["QuantityInStock"]}
            return jsonify({"exeid": exeid},item)   
    else:
            return jsonify({"exeid": exeid},{"error": "missing product id"}), 404
        

#function for buying the product by user's operation                 
@app.route("/BuyProduct", methods=["PUT"])
def BuyProduct():

    # request the data
    data = json.loads(request.data) 
    id = data.get("id")
    quanitiy = data.get("QuantityInStock")
    creditcard = data.get("creditCardid")
    global creditcardNum
    global amount

    #genarate an execution ID for each response
    exeid = exe_id(HOST,PORT)
    #lock this session for deadlock avoidance, other thread will stop to access this resources 
    lock.acquire()

    #condition for checking id and credit card number is correct or not
    try:
        int(id)
    except:
        return jsonify({"exeid": exeid},{"error": "missing product id"}), 400

    for i in creditcardNum:
        if creditcard != i["creditCardid"]:
            return jsonify({"exeid": exeid},{"error": "invaild credit card number"}), 404 

    #if the id is equal to the input id by the user, the operation will calculate the quantity and return it to the product list. 
    # open the file and finally rewrite again to the product.txt 
    with open(fname,"r+") as f:
        for i in range(len(currentcontent)):            
            if int(id) == int(currentcontent[i]["id"]):                                 
                    res = int(currentcontent[i]["QuantityInStock"]) - int(quanitiy)
                    reduce = res
                    currentcontent[i]["QuantityInStock"] = int(reduce) 
                    reduceAmount = int(amount) - (int(currentcontent[i]["UnitPrice"]) * int(quanitiy))
                    resAmount = reduceAmount              
                    item = { "status": "success","id":  currentcontent[i]["id"], "desc": currentcontent[i]["desc"],
                        "UnitPrice" : currentcontent[i]["UnitPrice"],
                        "Quanitiy" : currentcontent[i]["QuantityInStock"]}
            productwrite = json.dumps(currentcontent[i])
            f.write(productwrite +"\n")
        f.close()
        #release the lock
        lock.release()     
    return jsonify({"exeid": exeid},item, "your credit card amount left: " , str(resAmount))

#function for replenishing the product  
@app.route("/replenishFunction", methods=["PUT"])
def replenishFunction():
    
    #genarate an execution ID for each response
    exeid = exe_id(HOST,PORT) 
    data = json.loads(request.data) 
    id = data.get("id")
    quantity = data.get("QuantityInStock")

    #condition for checking id and credit card number is correct or not
    try:
        int(id)
    except:
        return jsonify({"exeid": exeid},{"error": "missing product id"}), 400

    #if the id is equal to the input id by the user, the quantity will be correspondingly updated by user input.
    # open the file and finally rewrite again to the product.txt
    with open(fname,"r+") as f: 
        for i in range(len(currentcontent)):      
            if int(id) == int(currentcontent[i]["id"]):                   
                    res = int(currentcontent[i]["QuantityInStock"]) + int(quantity)
                    reduce = res
                    currentcontent[i]["QuantityInStock"] = int(reduce)           
                    item = { "status": "success","id":  currentcontent[i]["id"], 
                    "Quanitiy" : currentcontent[i]["QuantityInStock"]}                     
            productwrite = json.dumps(currentcontent[i])
            f.write(productwrite +"\n")
        f.close()     

        print("program end")        
    return jsonify({"exeid": exeid},{"status":"The Quanitiy has been updated: "} , item ,{"status": "program end"})
       
if __name__ == "__main__":
    #showAll()
    #QueryProduct()
    #replenishFunction()
    #BuyProduct()
    print(exe_id)
    app.run()