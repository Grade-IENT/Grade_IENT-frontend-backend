import psycopg2
import csv
import glob
from collections import defaultdict
import os
from psycopg2.extras import execute_batch


conn = psycopg2.connect(
    host="localhost",
    database="gradientdb",
    user="postgres",
    password="accountSqL01"
)
cur = conn.cursor()

hashMapProf = defaultdict(dict)
hashMapProfCourse = defaultdict(dict)
hashMapCourse = defaultdict(dict)



for file_path in glob.glob('*backend/rmp-scraper/Summarized_Reviews/*.csv'):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:  
            hashMapProf[row[0]].update({'summary': row[1]})



for file_path in glob.glob('*backend/sentiment_analysis/Ratings Data/*.csv'):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
    
        for row in reader:
            hashMapProf[row[0]].update({'rating': float(row[1])})

courses = ['Chemistry', 'Physics', 'Math', 'Computer Science', 'Engineering']

for course in courses:
    for file_path in glob.glob(f'backend\Grade-ient_SQI\courses\{course}\*.csv'):
        #print(file_path)

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            #next(reader)
            
            if 'professor_SQI.csv' in file_path and 'course-professor_SQI.csv' not in file_path:
                    
                for row in reader:
                    hashMapProf[row[0]].update({'SQI': float(row[1])})

            elif 'course_SQI.csv' in file_path:     
                #print('in here')
                for row in reader:
                    hashMapCourse[row[0]].update({'SQI': float(row[2]), 'course_name': row[1]})
#print(hashMapCourse)

#print(hashMapProf)

#print(hashMapProf)
try:
    with conn.cursor() as cur:
        execute_batch(cur, """
            INSERT INTO Professor (prof_name, netid, summary, metrics, SQI)
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT (prof_name) DO NOTHING""", 
            [(name, '', data.get('summary'), data.get('rating'), data.get('SQI')) for name, data in hashMapProf.items()])
except Exception as e:
    print(f"Error inserting into Professor table: {e}")
    
with conn.cursor() as cur:
    execute_batch(cur, """INSERT INTO Class (course_code, course_name, SQI) VALUES (%s, %s, %s) ON CONFLICT (course_code) DO NOTHING""",
                [(course_code,data.get('course_name'),data.get('SQI')) for course_code,data in hashMapCourse.items()])
    
conn.commit()


for course in courses:
    for file_path in glob.glob(f'backend\Grade-ient_SQI\courses\{course}\*.csv'):

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)

            for row in reader:

                #try:

                
                    if 'course-professor_SQI.csv' in file_path:
                        #print(row)

                        with conn.cursor() as cur:
                            execute_batch(cur, """INSERT INTO Teaches (prof_id,class_id, SQI) VALUES (
                                        
                                        (SELECT id FROM Professor WHERE prof_name = %s),
                                        (SELECT id FROM Class WHERE course_code = %s),
                                          %s
                                        
                                        ) ON CONFLICT (prof_id,class_id) DO NOTHING """,[(row[2],row[0],row[3])])
                #except Exception as e:
                #   print("encountered something that doesn't exist")
                 #   continue

        

print("Connected to PostgreSQL!")
conn.commit()
cur.close()
conn.close()