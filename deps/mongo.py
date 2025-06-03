# deps/mongo.py
from fastapi import Depends
from db.collections import get_collection
from fastapi import Depends, HTTPException, Path
from bson import ObjectId, errors as bson_errors

def get_users_collection():
    return get_collection("users")

def get_patients_collection():
    return get_collection("patients")

def get_detections_collection():
    return get_collection("detections")

def get_tokens_collection():
    return get_collection("tokens")

def get_logger_collection():
    return get_collection("logger")

def get_profiler_collection():
    return get_collection("profiler")