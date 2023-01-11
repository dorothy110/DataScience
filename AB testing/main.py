


import pandas as pd
import numpy as np
import re
from flask import Flask, request, jsonify, Response
from scipy import stats
import time
import io
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt # matplotlib.use('agg')必须在本句执行前运行

num_subscribed = 0
CountA = 0
CountB= 0
visitCount = 0

app = Flask(__name__)


@app.route('/')
def home():
    global visitCount
    global CountA
    global CountB
    
    with open("index.html") as f:
        html = f.read()
    

    
    visitCount += 1   
    CurrentCount = visitCount

    
    if visitCount <11:

    # Homepage(index.html) donation button will direct customers go to the donate.html
    # We set customer will go to homepage 10 times
    # and divided:  odd times is going to A page, even times is going to B page, so is 50% to go to A and B 
        #seperate groups 0 1 0 1 0 1... 0 is A , 1 is B
        if CurrentCount%2 != 0:
            html = html.replace("replace", "blue")
            html = html.replace("x", "donate.html?from=A")
               
        else:
            html = html.replace("replace", "red")
            html = html.replace("x", "donate.html?from=B")


    else:
        if CountA >= CountB:
            html = html.replace("replace", "blue")
            html = html.replace("x", "donate.html?from=A")
        else:
            html = html.replace("replace", "red")
            html = html.replace("x", "donate.html?from=B")

    return html

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.


# panda dataframe part
covid_data = pd.read_csv("main.csv")
# covid_data=covid_data[["continent","location","date","total_cases","new_cases","total_deaths","new_deaths","human_development_index","population"]]
# covid_data = covid_data.dropna()
# grouped = covid_data.groupby("location")
# covid_data = grouped.get_group("United States")
# covid_data= covid_data.reset_index(drop =True)
@app.route("/dashboard_1.svg")
def plot1():
    bar_type =  str(request.args.get("type"))
    #generate the image
    fig, ax = plt.subplots(figsize = (30,5))
    if bar_type == "bar":
        pd.Series(dict(zip(covid_data.iso_code, covid_data.covid_cases))).plot.bar(ax = ax)
    else:
        pd.Series(dict(zip(covid_data.iso_code, covid_data.covid_cases))).plot.hist(ax = ax, color = "red")
    ax.set_xlabel("location")
    ax.set_ylabel("covid_cases")
    plt.tight_layout()  
    #send image back
    f = io.StringIO() # fake text "file" object
    fig.savefig(f,format = "svg")
    plt.close()#closes most recent fig
    return Response(f.getvalue(), headers= {"Content-Type":"image/svg+xml"})

# def plot2():
#     #generate the image
#     fig, ax = plt.subplots(figsize = (30,5))
#     pd.Series(dict(zip(covid_data.iso_code, covid_data.covid_cases))).plot.hist(ax = ax,bins =100,color = "red")
#     ax.set_xlabel("location")
#     ax.set_ylabel("deaths")
#     plt.tight_layout()
    
#     #send image back
#     f = io.StringIO() # fake text "file" object
#     fig.savefig(f,format = "svg")
#     plt.close()#closes most recent fig
#     return Response(f.getvalue(), headers= {"Content-Type":"image/svg+xml"})

@app.route("/dashboard_2.svg")
def plot3():
    #generate the image
    fig, ax = plt.subplots(figsize = (30,5))
    # pd.Series(covid_data).plot.line(ax = ax)
    pd.Series(dict(zip(covid_data.iso_code, covid_data.population_density))).plot.line(ax = ax)
    ax.set_xlabel("location")
    ax.set_ylabel("population_density")
    plt.tight_layout()
       
    #send image back
    f = io.StringIO() # fake text "file" object
    fig.savefig(f,format = "svg")
    plt.close()#closes most recent fig
    return Response(f.getvalue(), headers= {"Content-Type":"image/svg+xml"})

# transfer dataframe to table in html
@app.route('/browse.html')
def browse():
    with open("browse.html") as f:
        html = f.read()
    html = html.format(covid_data.to_html())
    return html

# dic1 = {Flask.request.remote_addr,last_visit_time}
dic1={}

@app.route('/browse.json',methods = ["GET"])
def slow():
    global dic1
    print("visitor", request.remote_addr)
    #identify if it is new user ip: if it is new，then add it into dic1
    if request.remote_addr in dic1:
        # print "IP exists"
            #time.time() : module.function(return 一个float)
        if time.time() -  dic1[request.remote_addr] >60:
            dic1[request.remote_addr] = time.time() 
            return jsonify(covid_data.to_dict()) 
             #displays the same information as browse.html, but in JSON format     
        else:
            return Response("<b>TOO MANY REQUESTS, Please retry again after 1 minute<b>",
                                 status = 429,
                                 headers = {"Retry-After": "60"})
    else:
        # print "IP does not exist"
        dic1[request.remote_addr] = time.time()
        return   jsonify(covid_data.to_dict())   
        #displays the same information as browse.html, but in JSON format

@app.route('/visitors.json',methods = ["GET"])
# 2. 我要在visitor.json里放字典dic1 里的IP
def visitor():
 
    return jsonify(list(dic1.keys()))

        
#1. 多个ip用同一个variable不行， 
#2.每个用户都有一个last vist{}
#3.如果用户是第一次来这个网站，他不需要被判断60s

    

#subscriber using email address, if success, the record will goes into emails.txt, if fail, it will showing invalid email address. if forgot to set up global variable, will showing "POST failed".  
@app.route('/email', methods=["POST"])
def email():
    global num_subscribed
    email = str(request.data, "utf-8")
    
    if len(re.findall(r"^[\w]+@[\w]+\.[a-zA-Z]{3}$", email)) > 0: # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + '\n') # 2
        num_subscribed += 1
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    else:
        return jsonify("invalid email address") # 3
    

@app.route('/donate.html')
def donate():
    global CountA
    global CountB

    

    # Once customer click the button, if it is in A page, then we countA +=1
    # Once customer click the button, if it is in B page, then we countB +=1
    # finally, which one is bigger, then we choose which one to show, after clicking homepage's donation button    
  
    # we get variable "from", we could actually determined variable name by ourselves
    GetVariable = str(request.args.get("from"))
    if visitCount <11:
        if GetVariable == 'A':
             CountA += 1
        elif GetVariable == 'B':
             CountB += 1

    with open("donate.html") as f:
        html = f.read()

    return html



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.