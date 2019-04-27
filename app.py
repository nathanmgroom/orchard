# -*- coding: utf-8 -*-
from flask import Flask, flash, request, redirect, url_for, Response, render_template, send_file
import pandas as pd
import csv
import sqlite3
from matplotlib import pyplot as plt
import numpy as np
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from flask_jsonpify import jsonpify


# 1. run anaconda command prompt
# 2. navigate to flask_project folder on desktop
# 3. type flask run
# 4. it will give you URL, copy and paste this into URL

app = Flask(__name__)
@app.route('/')
def etl_thing():
    #create the database in local memory
    con = sqlite3.connect(":memory:")
    con.text_factory = str
    cur = con.cursor()
    # Reading data file into Python from Github

    fil = 'https://github.com/nathanmgroom/orchard/raw/master/DOHMH_New_York_City_Restaurant_Inspection_Results2.zip'
    df = pd.read_csv(fil, compression='zip')
    df.to_sql('food_table', con, if_exists='replace', index=True)
    # grouping for number of top Thai restaurants in each Borough
# there's a 16-way tie for 2nd place according to the 'Score' category (a lower score is better). One restaurant received
# a score of 0, and 16 received a score of 2.0.
# So even though the prompt asks for the top 10, I included the top 17
    cur.execute("""select distinct DBA, CUISINEDESCRIPTION,BORO,GRADE, 
            SCORE FROM food_table where CUISINEDESCRIPTION = 'Thai' AND GRADE IN ('A','B') AND SCORE <= 2.0
            ORDER BY SCORE """)
    x=cur.fetchall()
 
    cur.execute("""SELECT BORO, count(distinct DBA) as DBA FROM (select distinct DBA, CUISINEDESCRIPTION,BORO,GRADE, 
            SCORE FROM food_table where CUISINEDESCRIPTION = 'Thai' AND GRADE IN ('A','B') AND SCORE <= 2.0
            ORDER BY SCORE) inner1 GROUP BY BORO""")
    y=cur.fetchall()
    cur.execute("""SELECT Grade, count(distinct DBA) as DBA FROM(select distinct DBA, CUISINEDESCRIPTION,BORO,GRADE, 
            SCORE FROM food_table where CUISINEDESCRIPTION = 'Thai'
            ORDER BY SCORE) inner1 GROUP BY Grade""")
    z=cur.fetchall()
    new_df2 = pd.DataFrame(z)

    new_df2.columns = ['Grade','Count Thai Restaurants By Grade']
    new_df2.index +=1
    top_thai1 = pd.DataFrame(x)
    new_df = pd.DataFrame(y)
    top_thai1.columns = ['Restaurant Name','Category','Boro','Grade','Score']
    new_df.columns = ['Borough','Count of Top Thai Restaurants']
    top_thai1.index +=1
    new_df.index += 1
    #top_thai1.index +=1
    x = np.arange(4)
    fig, ax = plt.subplots()
    count = new_df['Count of Top Thai Restaurants']
    plt.bar(x, count)
    plt.xticks(x, ('Brooklyn', 'Manhattan', 'Queens', 'Staten Island'))
    plt.title('Top Thai Restaurants by NYC Borough')
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return render_template("template.html",top_thaihtml = top_thai1.to_html(),new_df_html=new_df.to_html(),new_df2_html = new_df2.to_html())
     
@app.route('/plot1/')
def plot1():
    #create the database in local memory
    con = sqlite3.connect(":memory:")
    con.text_factory = str
    cur = con.cursor()
    # Reading data file into Python from Github

    fil = 'https://github.com/nathanmgroom/orchard/raw/master/DOHMH_New_York_City_Restaurant_Inspection_Results2.zip'
    df = pd.read_csv(fil, compression='zip')
    df.to_sql('food_table', con, if_exists='replace', index=True)
    cur.execute("""SELECT Grade, count(distinct DBA) as DBA FROM(select distinct DBA, CUISINEDESCRIPTION,BORO,GRADE, 
            SCORE FROM food_table where CUISINEDESCRIPTION = 'Thai'
            ORDER BY SCORE) inner1 GROUP BY Grade""")
    z=cur.fetchall()
    new_df2 = pd.DataFrame(z)
    
    
    new_df.columns = ['Borough','Count of Top Thai Restaurants']
    new_df.index += 1
    x = np.arange(4)
    fig, ax = plt.subplots()
    count = new_df['Count of Top Thai Restaurants']
    plt.bar(x, count)
    plt.xticks(x, ('Brooklyn', 'Manhattan', 'Queens', 'Staten Island'))
    plt.title('Top Thai Restaurants by NYC Borough')
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/plot2/')
def plot2():
    #create the database in local memory
    con = sqlite3.connect(":memory:")
    con.text_factory = str
    cur = con.cursor()
    # Reading data file into Python from Github

    fil = 'https://github.com/nathanmgroom/orchard/raw/master/DOHMH_New_York_City_Restaurant_Inspection_Results2.zip'
    df = pd.read_csv(fil, compression='zip')
    df.to_sql('food_table', con, if_exists='replace', index=True)
    # look at count of restaurants by grade
    cur.execute("""SELECT Grade, count(distinct DBA) as DBA FROM(select distinct DBA, CUISINEDESCRIPTION,BORO,GRADE, 
            SCORE FROM food_table where CUISINEDESCRIPTION = 'Thai'
            ORDER BY SCORE) inner1 GROUP BY Grade""")
    z=cur.fetchall()
    new_df2 = pd.DataFrame(z)
    new_df2.columns = ['Grade','Count Thai Restaurants By Grade']
    x2 = np.arange(7)
    fig, ax = plt.subplots()
    count2 = new_df2['Count Thai Restaurants By Grade']
    plt.bar(x2, count2)
    plt.xticks(x2, ('None', 'A', 'B', 'C','Pending','P','Z'))
    plt.title('NYC Thai Restaurants By Grade')
    canvas = FigureCanvas(fig)
    img2 = BytesIO()
    fig.savefig(img2)
    img2.seek(0)
    return send_file(img2, mimetype='image/png')

if '__name__' == '__main__':
    app.run(debug = True)
