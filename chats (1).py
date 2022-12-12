#CHATS
import sqlite3

connect = sqlite3.connect("chats.db")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS chats(
    chatid INT,
    chatname STRING,
    chatusername STRING,
    chatbio TEXT,
    chatrules TEXT,
    chatwords INT,
    vipchat TEXT,
    chatregdata TEXT
)
""")
connect.commit()