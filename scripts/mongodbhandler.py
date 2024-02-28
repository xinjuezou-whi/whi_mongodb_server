from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]


    def insert_data(self, collection_name, data):
        result = self.db[collection_name].insert_one(data)
        return str(result.inserted_id)

    def find_data(self, collection_name, query):
        results = self.db[collection_name].find(query)
        return [str(result) for result in results]

    def update_data(self, collection_name, query, new_values):
        result = self.db[collection_name].update_one(query, {'$set': new_values})
        return str(result.modified_count)

    def delete_data(self, collection_name, query):
        result = self.db[collection_name].delete_one(query)
        return str(result.deleted_count)
    

    def collection_exists(self, collection_name):
        """
        检查指定的集合是否存在于数据库中。
        :param collection_name: 要检查的集合的名称。
        :return: 如果集合存在则返回 True，否则返回 False。
        """
        return collection_name in self.db.list_collection_names()
    
    def delete_collection(self, collection_name):
        """
        删除指定的集合。
        :param collection_name: 要删除的集合的名称。
        :return: 删除成功返回 True，如果集合不存在则返回 False。
        """
        if self.collection_exists(collection_name):
            self.db[collection_name].drop()
            return True
        else:
            return False
        
    def create_collection(self, collection_name, options=None):
        """
        创建一个新的集合。
        :param collection_name: 要创建的集合的名称。
        :param options: 创建集合时的可选参数。
        :return: 创建成功返回 True，如果集合已存在则返回 False。
        """
       

        if not self.collection_exists(collection_name):

            self.db.create_collection(collection_name, **(options or {}))
            return True
        else:
            return False
