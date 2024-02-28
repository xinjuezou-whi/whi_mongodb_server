#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import rospy
# from whi_mongodb_server.srv import MongoQuery, MongoQueryResponse
# from pymongo import MongoClient
# import json

# client = MongoClient('mongodb://localhost:27017/')
# db = client['whi_demo']  # 替换为你的数据库名
# collection = db['test']  # 替换为你的集合名

# # 增加数据
# def insert_data(data):
#     result = collection.insert_one(data)
#     return str(result.inserted_id)

# # 查询数据
# def find_data(query):
#     results = collection.find(query)
#     # 将查询结果转换为字符串形式的列表，以便发送
#     return [str(result) for result in results]

# # 更新数据
# def update_data(query, new_values):
#     result = collection.update_one(query, {'$set': new_values})
#     # 返回更新的文档数
#     return str(result.modified_count)

# # 删除数据
# def delete_data(query):
#     result = collection.delete_one(query)
#     # 返回删除的文档数
#     return str(result.deleted_count)

# #处理数据库操作
# def process_db_action(req):
#     query_str = req.query
#     try:
#         query_dict = json.loads(query_str)
#     except json.JSONDecodeError:
#         return MongoQueryResponse("Invalid JSON format")

#     action = query_dict.get('action')

#     if action == 'insert':
#         # 从 query_dict 移除'action'，然后插入剩余部分
#         query_dict.pop('action', None)
#         result = insert_data(query_dict)
#     elif action == 'find':
#         query_dict.pop('action', None)
#         result = find_data(query_dict)
#     elif action == 'update':
#         query_dict.pop('action', None)  # 移除'action'
#         query_criteria = query_dict.get('query', {})  # 获取并保留用于查询的部分
#         new_values = query_dict.get('new_values', {})  # 获取新值
#         result = update_data(query_criteria, new_values)
#     elif action == 'delete':
#         query_dict.pop('action', None)
#         result = delete_data(query_dict)
#     else:
#         result = "Unknown action"

#     return MongoQueryResponse(str(result))
  

# def mongo_server():
#     rospy.init_node('mongo_server')
#     s = rospy.Service('process_db_action', MongoQuery, process_db_action)
#     print("Ready to query MongoDB.")
#     rospy.spin()

# if __name__ == "__main__":
#     mongo_server()

import subprocess
import os
from rosservicehandler import ROSServiceHandler


def start_mongodb():
    # cmd = [
    #     'mongod',
    #     '--dbpath', '/home/whi/mongodb-home/data',
    #     '--logpath', '/home/whi/mongodb-home/logs/mongod.log',
    #     '--fork'
    # ]

    cmd = [
        'mongod',
        '-f', '/home/whi/whi_db/mongod.conf'
    ]


    subprocess.Popen(cmd)

def stop_mongodb():
    cmd = ['mongo', '--eval', 'db.getSiblingDB("admin").shutdownServer()']
    subprocess.Popen(cmd)

if __name__ == "__main__":
    try:
        start_mongodb()
        ros_service_handler = ROSServiceHandler()
        ros_service_handler.spin()

    except Exception as e:
        print("An error occurred: {}".format(e))
    finally:
        print("Finalizing...")
        stop_mongodb()
    