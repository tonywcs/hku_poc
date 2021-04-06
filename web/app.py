from flask import Flask, request, render_template
import json
from flask_pymongo import PyMongo, pymongo
from pymongo import MongoClient
import datetime

app = Flask(__name__)
#db connection 
mongo = pymongo.MongoClient("mongodb+srv://iimt:iimt@cluster0.xsglo.mongodb.net/iimtnewsdb?retryWrites=true&w=majority") #connect mongodb
db = mongo.iimtnewsdb #iimtnewsdb is my database
col = db.cluster #Here cluster is my collection
    
today = '2021-01-17' #datetime.date.strftime(datetime.date.today(),"%Y-%m-%d") change it to real today in real implementation
no_error = True #state whether search has error or not 

def updateDateByWeek(dateresult):
    
    year, month, day = dateresult.split("-")
    date = datetime.datetime(int(year), int(month), int(day))
    while(date.strftime("%a") != "Sun"):
        date -= datetime.timedelta(days=1)
    dateresult = date.strftime("%Y") + "-" + date.strftime("%m") + "-" + date.strftime("%d")
    return dateresult

def updateDateByMonth(dateresult):
    year, month, day = dateresult.split("-")
    date = datetime.datetime(int(year), int(month), 1)
    dateresult = date.strftime("%Y") + "-" + date.strftime("%m") + "-" + date.strftime("%d")
    return dateresult

def handleError():
    nc = col.find_one({"cluster_type": "all"}) #if search error occur, the web will show current week's cluster
    return render_template('index.html', nc=nc, no_error=False)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        try: 
            typeresult = request.values["ctype"] 
            if typeresult == "all":
                nc = col.find_one({"cluster_type": typeresult }) 
                return render_template('index.html', nc=nc, today=today)
            dateresult = request.values["inputdate"]
            if dateresult is "":
                return handleError()
            if typeresult == "week":
                dateresult = updateDateByWeek(dateresult)
            if typeresult == "month":
                dateresult = updateDateByMonth(dateresult)
            nc = col.find_one({"cluster_type": typeresult , "date": dateresult }) 
            return render_template('index.html', nc=nc, today=today)

        except: 
            return handleError()
        
    else:
        nc = col.find_one({"cluster_type": "all"}) #default / landing page will show current week's cluster
        return render_template('index.html', nc=nc)

if __name__ == "__main__":
    app.run(debug=True)



