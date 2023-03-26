from app.Reporter.infor import dbReporter
from app.Reporter.const import stage_dict

user = 'admin'
password = 'admin123'
address = '121.41.58.52'
Recoder = dbReporter(user, password, address)
Recoder.setup_db('NX-database', 'personal-info', 1)

