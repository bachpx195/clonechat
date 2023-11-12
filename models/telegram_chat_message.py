from configs.database.pymysql_conn import DataBase
from datetime import datetime

db = DataBase()
UCSTWOMAX = 65536 

class TelegramChatMessage:
  def __init__(self, msg_id, content, chat_date):
    self.msg_id = msg_id
    # https://stackoverflow.com/questions/73225995/how-to-remove-some-bytes-from-a-byte-string
    self.content = content
    self.chat_date = chat_date

  def create(self):
    sql_query = 'INSERT INTO `DailyTradingJournal_development`.`telegram_chat_messages` (`telegram_chat_id`, `msg_id`, `content`, `chat_date`, `created_at`, `updated_at`) VALUES (1, %s, %s, %s, %s, %s);'
    if self.content is not None:
      print(sql_query)
      db.create(sql_query, (self.msg_id, self.TryDecode(self.content), self.chat_date, datetime.now(), datetime.now()))

  @classmethod
  def get_last_msg_id(cls):
    sql_query = "SELECT * FROM DailyTradingJournal_development.telegram_chat_messages order by chat_date DESC limit 1"
    db.cur.execute(sql_query)
    datas = list(db.cur.fetchall())
    return datas

  # Max value for UCS-2 formatting
  def TryDecode(self, toParse):
    try:
        parsed = toParse.encode().decode('utf-8', 'ignore')
        result = ''
        for c in parsed:
            if ord(c) < UCSTWOMAX:
                result += c
    except UnicodeEncodeError:
        result = 'error'
    return result