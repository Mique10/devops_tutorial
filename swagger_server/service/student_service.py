import os
import tempfile
from functools import reduce

import pymongo
from pymongo import MongoClient

uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017')


client = MongoClient(uri)
# client = MongoClient('mongo-release')
db = client['test_db']
student_db = db['students']


def add(student=None):
    res = student_db.find_one({"first_name": student.first_name, "last_name": student.last_name})
    if res:
        return 'already exists', 409

    res = student_db.insert_one(student.to_dict())
    inserted_id = res.inserted_id

    res = student_db.find_one({"_id": inserted_id})

    student.student_id = res['student_id']
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = student_db.find_one({"student_id": student_id})
    if not student:
        return 'not found', 404

    del student['_id']
    return student


def delete(student_id=None):
    student = student_db.find_one({"student_id": student_id})
    if not student:
        return 'not found', 404

    student_db.delete_one({"student_id": student_id})
    return student_id