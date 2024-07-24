import requests
from typing import Dict, List, Any
from pydantic import BaseModel
from datetime import datetime, timedelta

class Timings(BaseModel):
    LectureTimings: Dict[Any, Any]
    RestTimings: List[Dict[Any, Any]]

class Course(Timings):
    available: List[Dict[Any, Any]]


def getCourse(module_code:str) -> Course:
    try:
        response = requests.get(f"https://api.nusmods.com/v2/2024-2025/modules/{module_code}.json")
        ans = response.json()
    except Exception as e:
        print(e)
    
    ans = ans['semesterData'][0]['timetable']
    restTimings = list(filter(lambda x: x['lessonType'] != 'Lecture', ans))
    lectureTimings = getLecture(list(filter(lambda x: x['lessonType'] == 'Lecture', ans)))
    return Course(available=[], RestTimings=restTimings, LectureTimings=lectureTimings)


def getLecture(array: List[Dict[Any, Any]]) -> Dict[Any, Any]:

    finalList = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}

    for slot in array:
        day = slot['day']
        finalList[day].append([float(slot['startTime']), float(slot['endTime'])])

    print(finalList)
    return finalList



def merge(intervals):

    if not intervals:
        return []

    intervals.sort()
    
    output = []
    start = 0
    end = 0
    flag = False
    for index in range(len(intervals)):
        i = intervals[index]
        if not flag:
            start = i[0]
            end = i[1]
            flag = True

        else:
            if i[0] <= end:
                end = max(end,i[1])
            else:
                output.append([start, end])
                start = i[0]
                end = i[1]

        if index == len(intervals) - 1:
            output.append([start, end])


    return output


def getAllLectureTimings(courses: List[Course]) -> Dict[Any, List[Any]]:

    finalTimings = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}

    for course in courses:
        lectures = course.LectureTimings
        for day in finalTimings:
            finalTimings[day].extend(lectures[day])
            finalTimings[day] = merge(finalTimings[day])

    return finalTimings

    


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


CS3230_class_list = getCourse('CS3230')
NGT2001K_class_list = getCourse('NGT2001K')
CS2100_class_list = getCourse('CS2100')
print(getAllLectureTimings([CS3230_class_list, CS2100_class_list, NGT2001K_class_list]))

# some reason not counting ngt?