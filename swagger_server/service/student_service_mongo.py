import os
import tempfile
from functools import reduce

import pymongo
from pymongo import MongoClient

# client = MongoClient('mongodb://mongo:27017')
client = MongoClient('mongo-release')
db = client['students']


def add(student=None):
    res = db.students.find_one({"first_name": student.first_name, "last_name": student.last_name})
    if res:
        return 'already exists', 409

    res = db.insert_one(student.to_dict())
    student.student_id = res.inserted_id
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = db.students.find_one({"student_id": student_id})
    if not student:
        return 'not found', 404

    del student['_id']
    return student


def delete(student_id=None):
    student = db.students.find_one({"student_id": student_id})
    if not student:
        return 'not found', 404

    db.student.delete_one({"student_id": student_id})
    return student_id