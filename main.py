from copy import deepcopy
import csv
from flask import Flask, render_template, request,flash
import pypyodbc
import random
import numpy as np
# import scipy
import math

from time import time
# import itertools
# from sklearn.cluster import KMeans



app = Flask(__name__)
app.secret_key = "Secret"

connection = pypyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=(Specify Server Name);Database=(specify database name);Uid=(specify userid);Pwd=(specify password);")
cursor = connection.cursor()

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/search', methods = ['POST', 'GET'])
def search():

    k = request.args.get("k")
    min = request.args.get("min")
    max = request.args.get("max")

    start_time = time()
    for i in range(0, int(k)):
        mag = random.uniform(float(min), float(max))
        cursor.execute("select  top 1 locationSource from earthquakes where mag>='"+str(mag)+"'")
        result=cursor.fetchall()

    end_time = time()
    time_taken = (end_time - start_time) / int(k)
    flash('The Average Time taken to execute the random queries is : ' + "%.4f" % time_taken + " seconds")
    return render_template('output.html',t=time_taken,r=result)


@app.route('/case',methods = ['POST', 'GET'])
def case():
    cursor = connection.cursor()
    k = request.args.get("k")
    i = int(k)
    query = "SELECT case \
    while i < 5:\
              when mag between " + str(i) + " and " + str(i + 0.01) + " then '" + str(i) + " and " + str(
            i + 0.01) + "' \
        i = i + 0.01\
            else 'OTHERS' end as 'mag', count(*) as 'count' from edata group by mag"
    print(query)
    cursor.execute(query)
    print(query)
    rows = cursor.fetchall()
    print(rows)
    connection.close()
    return render_template('case.html', r=rows)

@app.route('/count',methods = ['POST', 'GET'])
def count():

    mag = request.args.get("mag")
    cursor.execute("Select count(*) from edata where mag>='"+mag+"'")
    rows=cursor.fetchall()

    return render_template('count.html', a=rows)


@app.route('/list',methods = ['POST', 'GET'])
def list():

    min = request.args.get("min")
    max = request.args.get("max")
    # loc = request.args.get("loc")
    cursor.execute("select  latitude, longitude, place from edata where mag Between '"+min+"' and '"+max+"' ")
    rows=cursor.fetchall()
    print(rows)
 
    return render_template('list.html', ci=rows)



if __name__ == '__main__':
   app.run(debug = True)
