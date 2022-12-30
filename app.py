import json  
import os 
import random 
from datetime import datetime, date 
import requests 
from flask import Flask, request, send_file 
from flask_cors import CORS, cross_origin 
from namebase_marketplace.marketplace import * 
from userObject import User 
 
app = Flask(__name__, static_url_path='/static') 
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type' 
users = [] 

m = input("Boot in maintenence mode [y/n]? ")

def open_html(name):
    with open(name, "r", encoding="utf-8") as html:
        html_file = html.read()
        html.close()
    
    return html_file


"""def log_user(user):
    now = datetime.now() 
    nTime = now.strftime("%H:%M:%S") 
    today = date.today() 
    nDate = today.strftime("%m/%d/%Y") 
    json_dump = {
        user.ip: [
            "domain": user.domain,
            "ip": user.ip,
            "email": user.email,
            "address": user.address,
            "time": nTime + nDate
        ]
    }"""

    
@app.before_request 
def block_method(): 
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    maintenence = open_html("static/maintenence.html")
    ban = open_html("static/ban.html")
    if m.lower() == "y":
      with open('admin-ips.txt', 'r') as read_obj:
        for line in read_obj:
          try:
              if str(ip) == str(line):
                print(ip + " was blocked due to maintenence mode")
                return maintenence
              else:
                pass
          except TypeError:
            print("excep")
            return maintenence

    with open('blocked-ips.txt', 'r') as read_obj: 
        for line in read_obj: 
            try: 
                if ip in line: 
                    print(str(ip) + " was blocked.") 
                    return ban
            except TypeError: 
                pass 
 
 
def create_app(): 
    return app 
 
 
 
@cross_origin() 
@app.route('/', methods=['GET', 'POST']) 
def form_example(): 
    if request.method == 'POST': 
        email = request.form.get('email') 
        hnsAdr = request.form.get('hns') 
        code = request.form.get('code') 
        #logr = open('log.txt' 'r+')
        try:
            logged_email = email.replace('.','') 
        except AttributeError:
            print("hnadr")
        error = open_html("static/error.html")
        muse = open_html("static/muse.html")
        hnfail = open_html("static/hnfail.html")
 
        log = open('log.txt', 'a+') 
        fl = open('names.txt', 'r+') 
        flt = open('namesTemp.txt', 'w+') 
        addresses_log = open('addresses.txt', 'r+') 
        ip_log = open('ips.txt', 'r+') 
        blocked_ip_list = open('blocked-ips.txt', 'r+') 
 
        names = fl.readlines() 
        now = datetime.now() 
        nTime = now.strftime("%H:%M:%S") 
        today = date.today() 
        nDate = today.strftime("%m/%d/%Y") 
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 
 
        log.write(50 * "-" + "\n") 
        log.write(nTime + " " + nDate + "\n") 
        log.write(ip + "\n") 
         
        print(50 * "-") 
        print(names) 
        print(nTime + " " + nDate) 
        print(ip) 
 
        try:
            print(logged_email)
        except:
            print("null email")
        
        for raw_line in addresses_log: 
            line = raw_line.replace('.','') 
            try: 
                if hnsAdr in line: 
                    return muse.format("HNS Address")
            except TypeError: 
                pass 
            try:
                if logged_email in line: 
                    return muse.format("Email")
            except:
                pass
        # Check if IP has already been used. 
        for line in ip_log:
            try:
                if ip in line:
                    return muse.format("IP")
            except TypeError:
                pass
                
        a = 0
        for x in names:
            a = a + 1
        print(a)

        nameDe = random.randint(0, a) - 1
        print(nameDe)

        try:
            name = names.pop(nameDe)
            current_user = User(name, ip, email, hnsAdr)
            print("User email: " + str(current_user.email))
        except IndexError:
            
            current_user = User(None, ip, email, hnsAdr)
            #log_user(current_user);
            return '''
            <h1>Sorry, no more names are left! Please try again later.</h1>'''
        
        print(name.strip("\n"))

        for x in names:
            flt.write(x)

        if email == None:
            # marketplace = Marketplace()
            # marketplace.transfer_domain_on_chain(name, hnsAdr)
            # fl.close()
            # flt.close()

            # os.remove('names.txt')
            # os.rename('namesTemp.txt', 'names.txt')
            # log.write(hnsAdr)
            # print(hnsAdr)
            # log.close

            return hnfail
        elif hnsAdr == None:

            fl.close()
            flt.close()

            if "mrvpt" in email:
                addresses_log.write("\n" + email)
                print(email)
                blocked_ip_list.write("\n" + ip)
                print(ip)
            else:
                log.write("\n" + str(email))
                print(email)
                log.close

                os.remove('names.txt')
                os.rename('namesTemp.txt', 'names.txt')
                headers = {"Accept": "application/json", "Content-Type": "application/json"}
                cookies = {
                    "namebase-main": "s%3Anononoyoudont.sometextidecidedtoputhere"}

                params = {"recipientEmail": email, "senderName": "IoniFaucet",
                          "note": "Thank you for using IoniFaucet!"}
                r = requests.post("https://www.namebase.io/api/gift/" + name.strip("\n"), headers=headers,
                                  data=json.dumps(params), cookies=cookies)

                success = r.json()
                try:
                    if success['success'] == True:
                        pass
                    else:
                        print(r.json())
                        return error.format(r.json())
                except:
                    print(r.json())
                    return error.format(r.json())

                print(r.json())

                log.write("{},{},{}".format(name, email, request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))

                print(logged_email)

                if email != 'no@maybe.fine' or email != 'yes@maybe.no':
                    addresses_log.write(f"\n{logged_email}")
                    ip_log.write(f"\n{ip}")
                else:
                    addresses_log.write(f"\n{logged_email}TEST")
                    ip_log.write(f"\n{ip}TEST")

                return '''
                <h1>Success!</h1>
                <h2>Successfully sent {} to {}!</h2>
                <h2>Check your email and claim it!<h2>'''.format(name, email)
        else:
            # Error Handling (Backend -f)
            return '''Please input an eMail or HN$ Address!'''

    if request.method == 'GET':
        fl = open('names.txt', 'r+')
        log = open('log.txt', 'a+')

        names = fl.readlines()
        print(50 * "-")
        log.write(50 * "-" + "\n")
        now = datetime.now()
        nTime = now.strftime("%H:%M:%S")
        today = date.today()
        nDate = today.strftime("%m/%d/%Y")
        print(nTime + " " + nDate) 
        log.write(nTime + " " + nDate + "\n")
        print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
        log.write(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) + "\n")

        a = 0
        for x in names:
            a = a + 1
        fl.close

        log.close()
        vl = open('addresses.txt', 'r+')

        views = vl.readlines()
        b = 0
        for x in views:
            b = b + 1
        vl.close

        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if ip == "07.157.66.4":
            test = User("none", ip, "none", "none")
            print(test)
            return '<h1>{}</h1>'.format(test)
        
        html = open_html("static/index.html")
        return html.format(a, b)


@app.route('/static/styles.css')
def send_js():
    return send_file('static/styles.css')


@app.route('/static/logo.png')
def logo_send():
    return send_file('static/logo.png', mimetype="image/png")


@app.route('/static/bg.svg')
def send_bg():
    return send_file('static/bg.svg')


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=443)
