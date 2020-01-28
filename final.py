import random
import os
import time
import telebot

import bot_functions
import constant


# Створення об'єкта класу TeleBot
bot = telebot.TeleBot(constant.TOKEN)


@bot.message_handler(content_types=['photo'])
def take_photo(message):
    """Work when Telegram Bot takes message type photo."""
    try:
        # Start point for time counting.
        start_t = time.time()
        
        # Saving taken photo.
        save_path = bot_functions.save_photo(message, bot)
        
        # Bot answers when photo was saved successfully.
        answer = "Thanks, photo's taken!!\nWait a while..."
        bot.reply_to(message, answer)
        
        # Finding coordinates of faces on saved photo.
        faces_coordinates = bot_functions.find_faces(save_path)
        
        # Replace every face on the photo.
        bot_functions.change_faces(save_path, faces_coordinates)
    
        # Bot sends and then deletes finished photo.
        bot.send_photo(message.chat.id, 
                       open(os.path.join(constant.PATH, save_path[18:]), 'rb'))
        os.remove(os.path.join(constant.PATH, save_path[18:])) 

        # End point for time counting.
        end_t = time.time()
        # Total time of editing photo.
        total_t = round(end_t - start_t, 2)

        # Bot send message and sticker
        bot_functions.bot_answer(message, bot, faces_coordinates, total_t)

    except Exception:
        answer = 'Opps...Something whet wrong.'
        bot.reply_to(message, answer)
        bot.send_sticker(message.chat.id, random.choice(constant.STICKERS_BAD))


# Bot works nonstop.
if __name__ == '__main__':
    bot.polling(none_stop=True)
