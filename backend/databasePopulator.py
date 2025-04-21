import psycopg2
import csv
import glob
from collections import defaultdict
import os
from psycopg2.extras import execute_batch


conn = psycopg2.connect(
    host="localhost",
    database="gradient",
    user="postgres",
   # password="accountSqL01"
)
cur = conn.cursor()

hashMapProf = defaultdict(dict)
hashMapProfCourse = defaultdict(dict)
hashMapCourse = defaultdict(dict)

def commaNameToName(name: str) -> str:
    name = name.split(",")
    fullName = name[0]
    if len(name) == 2:
        fullName = (name[1] + " " + fullName)[1:]
    return fullName


# LOAD SUMMARY
for file_path in glob.glob(f'backend/rmp-scraper/summarized/*.csv'):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        # next(reader) # there is no header here

        for row in reader:
            name = row[0]
            summary = row[1]
            hashMapProf[name].update({'summary': summary})
    
print(f"Loaded {len(hashMapProf)} professors with summaries; sample:\n",
      list(hashMapProf.items())[:5])


# LOAD SENTIMENT
for file_path in glob.glob(f'backend/sentiment_analysis/Updated Ratings Data/*.csv'):
    print("HEHEHEHEHEHEHEHEHEEHEHEHEHEE")
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader) # skip header

        for row in reader:
            name = row[0]
            rating = row[1]
            hashMapProf[name].update({'rating': float(rating)})

# LOAD SQI
courses = ['Chemistry', 'Physics', 'Math', 'Computer Science', 'Engineering']
for course in courses:
    for file_path in glob.glob(f'backend/Grade-ient_SQI/courses/{course}/*.csv'):
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)

            if '_professor_SQI.csv' in file_path:
                for row in reader:
                    name = row[0]
                    name = commaNameToName(name)
                    sqi = row[1]
                    hashMapProf[name].update({'SQI': float(sqi)})

            elif 'course_SQI.csv' in file_path:     
                #print('in here')
                for row in reader:
                    courseCode = row[0]
                    courseName = row[1]
                    sqi = row[2]
                    hashMapCourse[courseCode].update({'SQI': float(sqi), 'course_name': courseName})
print(hashMapCourse)
print(f"len of courses: {len(hashMapCourse)}")
print(hashMapProf)
print(f"len of profs: {len(hashMapProf)}")

# print(hashMapProf.items())

try:
    with conn.cursor() as cur:
        batch_values = []
        for name, data in hashMapProf.items():
            rating = data.get('rating')
            sqi_raw = data.get('SQI')
            
            combined_sqi = sqi_raw if rating is None else round((sqi_raw + rating) / 2,2)

            batch_values.append((
                name,
                data.get('summary'),
                combined_sqi
            ))
        print("Will insert", len(batch_values), "professors")
        execute_batch(
            cur,
            """
            INSERT INTO Professor (prof_name, summary, SQI)
            VALUES (%s, %s, %s)
            ON CONFLICT (prof_name) DO NOTHING
            """,
            batch_values
        )
    conn.commit()
except Exception as e:
    print(f"Error inserting into Professor table: {e}")
    
with conn.cursor() as cur:
    execute_batch(cur, """INSERT INTO Class (course_code, course_name, SQI) VALUES (%s, %s, %s) ON CONFLICT (course_code) DO NOTHING""",
                [(course_code,data.get('course_name'),data.get('SQI')) for course_code,data in hashMapCourse.items()])
    
conn.commit()


for course in courses:
    for file_path in glob.glob(f'backend/Grade-ient_SQI/courses/{course}/*.csv'):
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                # try:
                    if 'course-professor_SQI.csv' in file_path:
                        #print(row)
                        profName = row[2]
                        profName = commaNameToName(profName)
                        courseCode = row[0]
                        courseName = row[1]
                        sqi = row[3]
                        with conn.cursor() as cur:
                            execute_batch(cur, """INSERT INTO Teaches (prof_id,class_id, SQI) VALUES (
                                        
                                        (SELECT id FROM Professor WHERE prof_name = %s),
                                        (SELECT id FROM Class WHERE course_code = %s),
                                          %s
                                        
                                        ) ON CONFLICT (prof_id,class_id) DO NOTHING """,[(profName,courseCode,sqi)])
                # except Exception as e:
                #     print("encountered something that doesn't exist")
                #     continue

# for file_path in glob.glob(f'backend/class_and_pre-rec_scraper/data/course_prereqs/*.csv'):
#     with open(file_path, 'r', encoding='utf-8') as csv_file:
#         reader = csv.reader(csv_file)
#         next(reader)

#         for row in reader:
#            # print(row)
#             with conn.cursor() as cur:

#                 cur.execute("SELECT id FROM Class WHERE course_code ILIKE %s", (f'%:{row[0]}',))
#                 class_id = cur.fetchone()

#                 cur.execute("SELECT id FROM Class WHERE course_code ILIKE %s", (f'%:{row[2]}',))
#                 pre_req_id = cur.fetchone()

#                 if class_id and pre_req_id:
#                     cur.execute("INSERT INTO Pre_Reqs (class_id, pre_req_group, pre_req_id) VALUES (%s, %s, %s) ON CONFLICT (class_id, pre_req_id) DO NOTHING",
#                                (class_id[0], row[1], pre_req_id[0]))
#                 else:
#                     print(f"Class or pre-requisite not found for {row[0]} or {row[2]}")

print("Connected to PostgreSQL!")
conn.commit()
cur.close()
conn.close()