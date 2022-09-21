student_name = "Kon Yuen Lam"
student_id = "12669130"

# Write code below
import json, unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

SERVER = "localhost:5000"
JSON_CONTENT_TYPE = "application/json; charset=UTF-8"

#function for display all product's variable
def get_all_products():
    with urlopen(f"http://{SERVER}/showAll") as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result
#function for query by the input id
def query_product():
    print("product details:")
    id = input("input the product id to check detail: ")
    data = {"id" : id}
    req = Request(url = f"http://{SERVER}/QueryProduct",
            data = json.dumps(data).encode("utf-8"),
            headers = {"Content-type": "application/json; charset=UTF-8"},
           method="POST")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result

#function for buying the product by user's operation  
def buy_product():
    print("Payment operation page:")
    id = input("input the product id: ")
    quantity = input("input the quantity:")
    creditcard = input("input your credit Card number(16 digits number):")
    data = {"id" : id, "QuantityInStock" : quantity, "creditCardid" :creditcard}

    req = Request(url = f"http://{SERVER}/BuyProduct",
            data = json.dumps(data).encode("utf-8"),
            headers = {"Content-type": "application/json; charset=UTF-8"},
           method="PUT")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result

#function for replenishing the product  
def Replenish_product():
    print("Replenish the product page:")
    id = input("input your product id: ")
    quantity = input("input the quantity:")
    data = {"id" : id, "QuantityInStock" : quantity}
    req = Request(url = f"http://{SERVER}/replenishFunction",
            data = json.dumps(data).encode("utf-8"),
            headers = {"Content-type": "application/json; charset=UTF-8"},
           method="PUT")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result

#Unit test section
def ws_client(url, method=None, data=None):
    if not method:
        method = "POST" if data else "GET"
    if data:
        data = json.dumps(data).encode("utf-8")
    headers = {"Content-type": "application/json; charset=UTF-8"} \
                if data else {}
    req = Request(url=url, data=data, headers=headers, method=method)
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result

class UnitTest(unittest.TestCase):

    #A query about a product returns the correct product attributes.
    def test_query_product(self):
        id = 1
        create_resp = ws_client(f"http://{SERVER}/QueryProduct",
                "POST", {"id": 1})
        self.assertEqual(id,create_resp[1]["id"])

    #Buying a product with sufficient stock in the server succeeds and the quantity in stock is updated.
    def test_buy_product_success(self):
        create_resp = ws_client(f"http://{SERVER}/BuyProduct",
                "PUT", {"id" : 1 , "QuantityInStock" : 2 , "creditCardid" : "1111111111111111"})
        self.assertEqual("success",create_resp[1]["status"]) 

    #Buying a product with insufficient stock in the server fails and the quantity in stock remains unchanged.
    def test_buy_product_error(self):
        try:
             ws_client(f"http://{SERVER}/BuyProduct",
                "PUT", {"id" : 1 , "QuantityInStock" : "200" , "creditCardid" : "1111111111111111"})
        except HTTPError as e:
            self.assertEqual(400, e.code)  

    #Replenishing a product updates the server’s quantity in stock.
    def test_Replenish_product_success(self):
        create_resp = ws_client(f"http://{SERVER}/replenishFunction",
                "PUT", {"id" : 2 , "QuantityInStock" : 2})
        self.assertEqual("success",create_resp[2]["status"])  

    #When the product ID does not exist, the server returns the 404 status code
    def test_id_not_exist(self):
        try:
            ws_client(f"http://{SERVER}/QueryProduct",
                "POST", {"id": 111})
        except HTTPError as e:
            self.assertEqual(404, e.code)  
         
    #When some required input data are missing or invalid, the server returns the 400 status code.        
    def test_input_id_missing(self):
        try:
            ws_client(f"http://{SERVER}/QueryProduct",
                "POST", {"id": ""})
        except HTTPError as e:
            self.assertEqual(400, e.code)
        try:
            ws_client(f"http://{SERVER}/BuyProduct",
                "PUT", {"id": "", "QuantityInStock" : "", "creditCardid" : ""})
        except HTTPError as e:
            self.assertEqual(400, e.code)
        try:
            ws_client(f"http://{SERVER}/replenishFunction",
                "PUT", {"id": "", "QuantityInStock" : ""})
        except HTTPError as e:
            self.assertEqual(400, e.code)
            
if __name__ == "__main__":
    print(get_all_products())
    print(query_product())
    print(buy_product())
    print(Replenish_product())

#unit test function call, remove the annotation # 
#---------------------------------#   
    #unittest.main()
#---------------------------------#