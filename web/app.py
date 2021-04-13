from flask import Flask, request, render_template
import json
from flask_pymongo import PyMongo, pymongo
from pymongo import MongoClient
import datetime

app = Flask(__name__)
#db connection 
mongo = pymongo.MongoClient("mongodb+srv://iimt:iimt@cluster0.xsglo.mongodb.net/iimtnewsdb?retryWrites=true&w=majority") #connect mongodb
db = mongo.iimtnewsdb #iimtnewsdb is my database
col = db.cluster
graphs = {"image_2021-01-05all.png", "image_2021-02-01month.png", "image_2021-03-01month.png"}
    
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

def returnAll():
    nc = col.find_one({"cluster_type": "all" }) 
    img = getImage("2021-01-05", "all")
    return render_template('index.html', nc=nc, img=img)

def handleError():
    nc = col.find_one({"cluster_type": "all"}) #if search error occur, the web will show current week's cluster
    return render_template('index.html', nc=nc, no_error=False)

def getImage(date, cluster_type):
    img = "image_" + date + cluster_type + ".png"
    return "static/" + img if img in graphs else None


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        try: 
            typeresult = request.values["ctype"] 
            if typeresult == "all":
                return returnAll()
            dateresult = request.values["inputdate"]
            if dateresult is "":
                return handleError()
            if typeresult == "week":
                dateresult = updateDateByWeek(dateresult)
            if typeresult == "month":
                dateresult = updateDateByMonth(dateresult)
            nc = col.find_one({"cluster_type": typeresult , "date": dateresult }) 
            img = getImage(dateresult, typeresult)
            return render_template('index.html', nc=nc, img=img)

        except: 
            return handleError()
        
    else:
        return returnAll()

@app.route('/about', methods=['GET'])
def about():
        return render_template('about.html')

@app.route('/uci', methods=['GET', 'POST'])
def uci():
    col = db.uci
    if request.method == 'POST':
        try: 
            typeresult = request.values["ctype"] 
            if typeresult == "all":
                nc = col.find_one({"cluster_type": typeresult }) 
                return render_template('index_uci.html', nc=nc, today=today)
            dateresult = request.values["inputdate"]
            if dateresult is "":
                return handleError()
            if typeresult == "week":
                dateresult = updateDateByWeek(dateresult)
            if typeresult == "month":
                dateresult = updateDateByMonth(dateresult)
            nc = col.find_one({"cluster_type": typeresult , "date": dateresult }) 
            return render_template('index_uci.html', nc=nc, today=today)

        except: 
            return handleError()
        
    else:
        nc = col.find_one({"cluster_type": "day" , "date": "2014-03-11" }) 
        return render_template('index_uci.html', nc=nc)

if __name__ == "__main__":
    app.run(debug=True)



