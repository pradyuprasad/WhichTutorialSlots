import requests
from typing import Dict, List, Any
from pydantic import BaseModel

class Timings(BaseModel):
    LectureTimings: List[Dict[Any, Any]]
    RestTimings: List[Dict[Any, Any]]

class Course(BaseModel):
    timings: Timings


def getAllTimings(module_code:str) -> Timings:
    try:
        response = requests.get(f"https://api.nusmods.com/v2/2024-2025/modules/{module_code}.json")
        ans = response.json()
    except Exception as e:
        print(e)
    
    return Timings(RestTimings=(list(filter(lambda x: x['lessonType'] != 'Lecture', ans['semesterData'][0]['timetable']))), LectureTimings=list(filter(lambda x: x['lessonType'] == 'Lecture', ans['semesterData'][0]['timetable'])))


'''
Function that
1. takes in a list of modules and returns a list of tutorial slots possible based on your constraints
2. make all possible tutorial combinations 
example: 
input:
ST2334 9am-10am, 11am-12am, 17:00-18:00
NGN: 10-12, 2-4, 6-8

it gives me -

version1
9-10 st
10-12 ngn
5-6 st
2-4 ngn
6-8 st

version2

you should bid for
1. st 9-10, 3-4, 5-6

constraints
1. do not conflict with lecture times of all mods
2. allow them to block out times (other times) (everyday and pattern)
3. time between classes 
4. classes in same building keep together


'''


ST_class_list = getAllTimings('ST2334')
CS2109s_class_list = getAllTimings('CS2109S')

