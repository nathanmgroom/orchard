# ETL Project
# Nathan Groom
The schema consists of 1 table, called 'food_table' which is on a SQLite database in the machine's local memory.
The table is the .CSV of NYC Dept. of Health restaurant reviews provided in the assignement prompt

The data was slightly cleaned in Excel to make it easier to import into Python -- for example replacing spaces in column names with periods, and the cleaned file is currently on Github at the following link:
https://github.com/nathanmgroom/orchard/raw/master/DOHMH_New_York_City_Restaurant_Inspection_Results2.zip


The main code is in the 'thai_restaurants.py' file. All the data was uploaded to a SQLite database using SQLite3 in Python and most insights were found with SQL queries. 
The main question asked in this prompt was 'What are the top 10 Thai restaurants with either an A or B rating?', so I had to determine criteria as to what makes a top Thai restaurant. I used the 'score' column which assigns each restaurant a cleanliness score. It seems that lower scores are better (as 'A' grade restaurants have lower scores than 'B' grade restaurants), so I queried a list of the Thai restaurants with a score of A or B, with the lowest scores. There was one restaurant with a score of 0.0 and 16 restaurants with a score of 2.0. I decided to include all of these in the list of 'best restaurants' even though the prompt only asked for 10, as I didn't think there was a way to decide what the 'top' (e.g. 9 out of 16) restaurants that scored a 2.0 were. Including the restaurant with a score of 0.0, the list has a total of 17 restaurants.

I included the list in the code. As for visualizations, I looked for some insights to plot. I eventually ploted the count of top Thai restaurants by borough as well as an overall count of the distribution of grades given to all restaurants throughout New York.

The 'app.py' and 'template.html' are for a Flask app. It takes the same code present in thai_restaurants.py and wraps it in a web app. It then outputs the Python code in 'app.py' into a html template, which is written in 'template.html'. So far, the Flask app only works on a localhost URL. The resulting web page displays several tables of data and two bar graphs. 

Column names and data types for food_table are as follows:  
0, 'index', 'INTEGER',  
1, 'CAMIS', 'INTEGER',  
2, 'DBA', 'TEXT', 0,  
3, 'BORO', 'TEXT', 0,  
4, 'BUILDING', 'TEXT',  
5, 'STREET', 'TEXT',  
6, 'ZIPCODE', 'REAL',  
7, 'PHONE', 'TEXT',  
8, 'CUISINEDESCRIPTION', 'TEXT',  
9, 'INSPECTION.DATE', 'TEXT',  
10, 'ACTION', 'TEXT',  
11, 'VIOLATION.CODE', 'TEXT',  
12, 'CRITICAL.FLAG', 'TEXT',  
13, 'SCORE', 'REAL',  
14, 'GRADE', 'TEXT',  
15, 'GRADE.DATE', 'TEXT',  
16, 'RECORD.DATE', 'TEXT',  
17, 'INSPECTION TYPE', 'TEXT'  
