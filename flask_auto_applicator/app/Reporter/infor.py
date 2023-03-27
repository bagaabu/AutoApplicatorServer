import urllib.parse
from .const import auth_dict
from .tools import get_time
import pymongo


class dbReporter:
    state_flag = {0: 'clean all', 1: 'keep all'}

    def __init__(self):
        username = urllib.parse.quote_plus(auth_dict['user'])
        password = urllib.parse.quote_plus(auth_dict['password'])
        self.mongo_client = pymongo.MongoClient('mongodb://{}:{}@{}'.format(username, password, auth_dict['address']),
                                                auth_dict['port'])

    def setup_db(self, dbName, collectionName, flag):
        print('setup flag: ' + self.state_flag[flag])
        self.collection = self.mongo_client[dbName][collectionName]
        if flag == 0:
            collist = self.mongo_client[dbName].list_collection_names()
            if collectionName in collist:
                print("The collection exists")
                if self.collection.drop():
                    print('collection dropped')
                else:
                    print('collection cant be dropped')
            else:
                print('collection not exists')
        elif flag == 1:
            print('keep original collection')
        print('now db: {} collection: {}'.format(dbName, collectionName))

    def change_db(self, dbName, collectionName, flag):
        print('changing db collection')
        self.setup_db(dbName, collectionName, flag)

    def search(self, content, conditions='all'):
        res = []
        query = {'userID': content}
        if conditions == 'all':
            docRes = self.collection.find(query)
        else:
            docRes = self.collection.find(query, conditions)

        for record in docRes:
            res.append(record)

        if len(res) > 0:
            return True, res
        else:
            return False, None

    def log(self, content, replace=True):
        userID = content['userID']
        time_stamp, time_str = get_time()
        content['time_stamp'] = time_stamp
        content['time_str'] = time_str
        if replace:
            prev_search = self.search(userID)
        else:
            prev_search = [False]
        if prev_search[0]:
            prev_query = {"userID": userID}
            present_query = {"$set": content}
            self.collection.update_one(prev_query, present_query)
            post_id = prev_search[1][0]['_id']
        else:
            post_id = self.collection.insert_one(content).inserted_id
        return post_id

    def log_batch(self, batch_content):
        post_ids = self.collection.insert_many(batch_content)
        return post_ids


if __name__ == '__main__':
    user = 'abu'
    password = 'abu123'
    address = '10.252.73.99'
    Logger = DB_logger(user, password, address)
    Logger.setup_db('NX-database', 'personal-info', 1)

    content_step_1 = {
        'userID': 'abcd01234',
        'gender': 'male',
        'age': '30',
        'under-course': 'University of Northumbria',
        'under-major': 'Electronic Electrical Engineering',
        'prefer-country': 'UK',
        'prefer-university': 'Southampton University',
        'prefer-major': 'Electronic Electrical Engineering'
    }

    content_step_2 = {
        'userID': 'abcd0123',
        'GPA': '4',
        'GRE': '346',
        'SAT': '1600',
        'TOFEL': '120',
        'IELTS': '8'
    }

    content_step_3 = {
        'userID': 'abcd0123',
        'InterExe': '',
        'WorkingExe': '',
        'ProjectExe': '',
        'honor&award': ''
    }

    content_step_4 = {
        'userID': 'abcd0123',
        'university': '',
        'motivation': '',
        'long-term-program': ''
    }

    Logger.log(content_step_1)
    Logger.change_db('NX-database', 'score', 1)
    Logger.log(content_step_2)
    Logger.change_db('NX-database', 'experience', 1)
    Logger.log(content_step_3)
