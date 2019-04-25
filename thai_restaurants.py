# -*- coding: utf-8 -*-


import pandas as pd
import csv
import sqlite3
from matplotlib import pyplot as plt
import numpy as np

#create the database in local memory
con = sqlite3.connect(":memory:")
con.text_factory = str
cur = con.cursor()
# Reading data file into Python
df = pd.read_csv('C:/Users/natha/Desktop/DOHMH_New_York_City_Restaurant_Inspection_Results2.csv')
df.to_sql('food_table', con, if_exists='replace', index=True)


# grouping for number of top Thai restaurants in each Borough
# there's a 16-way tie for 2nd place according to the 'Score' category (a lower score is better). One restaurant received
# a score of 0, and 16 received a score of 2.0.
# So even though the prompt asks for the top 10, I included the top 17
cur.execute("""select distinct DBA, CUISINEDESCRIPTION,BORO,GRADE, 
            SCORE FROM food_table where CUISINEDESCRIPTION = 'Thai' AND GRADE IN ('A','B') AND SCORE <= 2.0
            ORDER BY SCORE LIMIT 100""")
x=cur.fetchall()
cur.execute("""SELECT BORO, count(distinct DBA) as DBA FROM (select distinct DBA, CUISINEDESCRIPTION,BORO,GRADE, 
            SCORE FROM food_table where CUISINEDESCRIPTION = 'Thai' AND GRADE IN ('A','B') AND SCORE <= 2.0
            ORDER BY SCORE LIMIT 100) inner1 GROUP BY BORO""")
y=cur.fetchall()

top_thai1 = pd.DataFrame(x)
new_df = pd.DataFrame(y)
top_thai1.columns = ['Restaurant_Name','Category','Boro','Grade','Score']
new_df.columns = ['Borough','Count of Top Thai Restaurants']
new_df.index += 1
top_thai1.index +=1
#the top Thai restaurants
top_thai1

#first visualization - top thai restaurants by borough
x = np.arange(4)
fig, ax = plt.subplots()
count = new_df['Count of Top Thai Restaurants']
plt.bar(x, count)
plt.xticks(x, ('Brooklyn', 'Manhattan', 'Queens', 'Staten Island'))
plt.title('Top Thai Restaurants by NYC Borough')

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