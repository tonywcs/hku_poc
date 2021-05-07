from flask import Flask, request, render_template
import json
from flask_pymongo import PyMongo, pymongo
from pymongo import MongoClient
import datetime
import matplotlib.pyplot as plt
import networkx as nx

pp = Flask(__name__)
#db connection 
mongo = pymongo.MongoClient("mongodb+srv://iimt:iimt@cluster0.xsglo.mongodb.net/iimtnewsdb?retryWrites=true&w=majority") #connect mongodb
db = mongo.iimtnewsdb #iimtnewsdb is my database
col = db.cluster #Here cluster is my collection

nc = col.find_one({"cluster_type": "all"})
#nc = col.find_one({"cluster_type":"month","date":"2021-03-01"})
#nc = col.find_one({"cluster_type":"month","date":"2021-02-01"})
#nc = col.find_one({"cluster_type":"day","date":"2014-03-11"})
G = nx.Graph()
number_of_cluster = nc["total_number_of_clusters"]
color_map =[]
size_map = []

#add node
for i in range(number_of_cluster):
    if nc["clusters"][i]["total_number_of_articles"] > 20:     #not show cluster with little articles
        G.add_node("Cluster"+str(i+1))
        color_map.append('red') 
        size_map.append(nc["clusters"][i]["total_number_of_articles"]*5)   

for i in range(number_of_cluster):
    if nc["clusters"][i]["total_number_of_articles"] > 20: 
        for j in nc["clusters"][i]["nerKeywords"]:
            if j[0] not in G:
                G.add_node(j[0])
                color_map.append('grey')
                size_map.append(30)

#add edges 
for i in range(number_of_cluster):
    if nc["clusters"][i]["total_number_of_articles"] > 20: 
        if nc["clusters"][i]["nerKeywords"] != []:
            for j in nc["clusters"][i]["nerKeywords"]: 
                G.add_edge("Cluster"+str(i+1),j[0]) 
#print diagram

pos = nx.spring_layout(G,k=0.2)
nx.draw(G,pos,with_labels=True,node_size=size_map,node_color=color_map)

# Convert plot to PNG image
plt.savefig("image_"+str(nc["date"])+str(nc["cluster_type"])+".png")
plt.show()
print ("finish")