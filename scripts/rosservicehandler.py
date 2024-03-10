
import rospy
from whi_mongodb_server.srv import MongoQuery, MongoQueryResponse
import json
from mongodbhandler import MongoDBHandler
from datetime import datetime
import subprocess

class ROSServiceHandler:
    def __init__(self):
        # 初始化节点
        rospy.init_node('whi_mongodb_server')

        # 读取参数
        uri = rospy.get_param('~uri')
        db_name = rospy.get_param('~db_name')
        conf = rospy.get_param('~conf')

        # 启动 mongodb
        self.start_mongodb(conf)

        # 创建MongoDB处理器
        self.mongo_handler = MongoDBHandler(uri, db_name)

        # 设置ROS服务
        self.service = rospy.Service('process_db_action', MongoQuery, self.process_db_action)

        rospy.loginfo("Initialization completed.")

    def start_mongodb(self, conf):        
        cmd = [
            'mongod',
            '-f', conf
        ]

        subprocess.Popen(cmd)

    def close_video_writer(self):
        if self.video_writer:
            self.video_writer.release()


    def process_db_action(self, req):
        query_str = req.data
        try:
            query_dict = json.loads(query_str)
        except json.JSONDecodeError:
            return MongoQueryResponse("Invalid JSON format")
       
        try:
            # 获取指令
            action = req.action
            # 获取集合名称
            collection_name = req.collection_name
            if collection_name is None:
                result = "Unknown collection_name"
                return MongoQueryResponse(False, "Error: " + str(result))

            if action == 'insert':

                # 获取当前时间  # 添加微秒
                current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")
                query_dict["_id"] = current_time
                
                result = self.mongo_handler.insert_data(collection_name, query_dict)
            elif action == 'find':
                result = self.mongo_handler.find_data(collection_name, query_dict)
            elif action == 'update':
                query_criteria = query_dict.get('query', {})
                new_values = query_dict.get('new_values', {})
                result = self.mongo_handler.update_data(collection_name, query_criteria, new_values)
            elif action == 'delete':
                result = self.mongo_handler.delete_data(collection_name, query_dict)
            elif action == 'create_collection':
                # 调用创建集合的方法
                if self.mongo_handler.create_collection(collection_name):
                    result = "Collection created successfully"
                else:
                    result = "Collection already exists"
                    return MongoQueryResponse(False, "Error: " + str(result))
            elif action == 'delete_collection':
                # 调用删除集合的方法
                if self.mongo_handler.delete_collection(collection_name):
                    result = "Collection deleted successfully"
                else:
                    result = "Collection does not exist"
                    return MongoQueryResponse(False, "Error: " + str(result))
            else:
                result = "Unknown action"
                return MongoQueryResponse(False, "Error: " + str(result))

            return MongoQueryResponse(True, str(result))
        except Exception as e:
            # 如果发生错误，可以返回错误信息
            return MongoQueryResponse(False, "Error: Failed to execute command")

    def spin(self):
        rospy.spin()
