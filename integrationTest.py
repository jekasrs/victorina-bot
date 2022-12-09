from pyrogram import Client, filters


import asyncio

api_id = 28963375
api_hash = "8b17f5707d7a743f8d08c4bc2772bdd2"

app = Client("my_account", api_id=api_id, api_hash=api_hash)


# queries = 12
# setup = 9

# Target chat. Can also be a list of multiple chat ids/usernames
TARGET = "party_victorina_bot"





# Filter in only new_chat_members updates generated in TARGET chat
@app.on_message(filters.chat(TARGET) & filters.new_chat_members )
async def welcome(client, message):

    await client.request_callback_answer(
        chat_id=message.chat.id,
        message_id=message.id,
        callback_data=1
    )



async def main():
    async with app:
        # Send a message, Markdown is enabled by default
        await app.send_message("party_victorina_bot", "/start")
        await asyncio.sleep(3)
        await app.send_message("party_victorina_bot", "Создать")
        await asyncio.sleep(3)
        await app.send_message("party_victorina_bot", "1")
        
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        await asyncio.sleep(3)
        
        
        # await app.send_message("party_victorina_bot", "1")
        # await asyncio.sleep(3)
        # await app.send_message("party_victorina_bot", "Film & TV")
        # await asyncio.sleep(3)
        # await app.send_message("party_victorina_bot", "10")
        # await asyncio.sleep(3)
        # await app.send_message("party_victorina_bot", "Начать игру")
        # await asyncio.sleep(3)




app.run(main())



# with TelegramClient(StringSession(), api_id, api_hash) as client:
#     print("Session string:", client.session.save())
#     client.send_message("/start", client.session.save())
#     results = await client.inline_query('like', 'Do you like Telethon?')
#     message = await results[0].click(0)

#     client.send_message("Создать", client.session.save())
#     client.send_message("1", client.session.save())
#     client.send_message("Film & TV", client.session.save())
    
#     client.send_message("10", client.session.save())
#     client.send_message("Начать игру", client.session.save())
#     client.send_message("1", client.session.save())
#     messages = client.get_messages('GOOGLE')
    
#     client.send_message("1", client.session.save())
#     client.send_message("1", client.session.save())
#     client.send_message("1", client.session.save())
#     client.send_message("1", client.session.save())
#     client.send_message("1", client.session.save())
#     client.send_message("1", client.session.save())
#     client.send_message("1", client.session.save())
#     client.send_message("1", client.session.save())
#     client.send_message("1", client.session.save())



# from telethon import TelegramClient, events, sync, utils

# api_id = "5593220196"
# api_hash = "AAG0qw4_B_ALDwMv2iWG0AW_pCRvn10CJE0"

# client = TelegramClient('session', api_id, api_hash)
# client.start()


# wwr = client.get_entity('party_victorina_bot')
# print(wwr)


# @client.on(events.NewMessage(from_users=wwr))
# async def handler(event):
#     buttons = await event.get_buttons()
#     for bline in buttons:
#         for button in bline:
#             print(button.button.text)
#             if 'Паззл' in button.button.text:
#                 await button.click()

# try:
#     print('(Press Ctrl+C to stop this)')
#     client.run_until_disconnected()
# finally:
#     client.disconnect()