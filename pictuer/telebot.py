
from pyrogram import filters
from pictuer.config import *
from pyrogram.raw import functions




print(1)
bot = Client('bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token, session_string=session_string)



def ss ():
    d = bot.get_chat(5408137895)
    print(d)

@bot.on_message()
async def get_message(client,message):
    x = functions.messages.GetAllChats()
    print(x)
    # test = message.text
    # id = int(message.from_user.id)
    # await bot.send_message(id,f'http://127.0.0.1:8000/video/{id}')

if __name__ == "__main__":
    bot.run()


