from datetime import datetime

from ..utils.apis import send_request


class writer:
    def __init__(self, recorder, requestID, user_data):
        self.userdata = user_data
        self.requestID = requestID
        self.recorder = recorder

    def get_article(self, requestID, user_data):
        res = send_request('request_txt', user_data, requestID)
        return res

    def save_article(self, article_record):
        save_dict = {
            'userID': self.userdata['userID'],
            'article': article_record,
            'school': self.userdata['preferUniversity'],
            'major': self.userdata['preferMajor']
        }
        articel_id = self.recorder.log(save_dict, False)
        return articel_id

    def get_save_article(self, logger):
        # try:
        article = self.get_article('request_txt', self.requestID, self.userdata)
        logger.info('article received')
        _, = self.save_article(article)
        logger.info('article saved')
        return 0
        # except:
        #     return 1

    def search_article(self, userID, date=None):
        flag = False
        result = []

        if date:
            pass
        else:
            flag, result = self.recorder.search(userID)
        return flag, result

    def get_article_records(self, userID, date=None):
        output = []
        flag, articles = self.save_article(userID, date)
        if flag:
            for article in articles:
                anRecord = {
                    'txt': article['article'],
                    'save_time': article['time_str'],
                    'school': article['school'],
                    'major': article['major']
                }
                output.append(anRecord)
        return output
