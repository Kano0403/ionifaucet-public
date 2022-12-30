import json  
import os 
import random 
from datetime import datetime, date 
import requests 
from flask import Flask, request, send_file 
from flask_cors import CORS, cross_origin 
from namebase_marketplace.marketplace import * 
from userObject import User 

email = "iprefernot@doestexist.com"
headers = {"Accept": "application/json", "Content-Type": "application/json"}
cookies = {
    "namebase-main": "s%nononoyoudont.somerandomstuffthatidecidedtoputhere"}
params = {"recipientEmail": email, "senderName": "IoniFaucet",
          "note": "Thank you for using IoniFaucet!"}
r = requests.post("https://www.namebase.io/api/gift/" + "xn--8k8haaaa13cbbbb594ncaccc", headers=headers,
                  data=json.dumps(params), cookies=cookies)
print(r.json)
if "success" in str(r.json()):
    pass
else:
    print(r.json())
