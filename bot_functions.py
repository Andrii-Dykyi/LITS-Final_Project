import os
import random
import time

import cv2

import constant


def save_photo(message, bot):
    """Save photo taken by Telegram Bot."""
    file_info = bot.get_file(message.photo[0].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = os.path.join(constant.PATH_MAIN, file_info.file_path)
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    return save_path


def find_faces(path_to_photo):
    """Find faces's coordinates on saved photo."""
    image = cv2.imread(path_to_photo, 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    facecascade = cv2.CascadeClassifier(constant.CASCADEPATH)
    faces_coordinates = facecascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=8,
        minSize=(30, 30))
    return faces_coordinates


def change_faces(save_path, faces_coordinates):
    """
    Replace every face on the photo,
    using coordinates with randome templates.
    """
    for (x, y, w, h) in faces_coordinates:
        # Choose random template.
        template_img = cv2.imread(random.choice(constant.TROLLS), -1)

        # Resize template to width and height of face rectangle and save it.
        dim = (w, h)
        resized_temp = cv2.resize(template_img, dim,
                                  interpolation=cv2.INTER_AREA)

        # Save every resized template with unique name.
        resized_name = str(w) + str(h) + '_resized.png'
        cv2.imwrite(os.path.join(constant.PATH_1, resized_name), resized_temp)

        # Reading image and resized template.
        image = cv2.cvtColor(cv2.imread(save_path, 1), cv2.COLOR_RGB2RGBA)
        template = cv2.imread(os.path.join(constant.PATH_1, resized_name), -1)
        template = cv2.cvtColor(template, cv2.COLOR_RGB2RGBA)

        # Replacing faces with templates.
        for c in range(0, 3):
            image[y: y + template.shape[0], 
                  x: x + template.shape[1], 
                  c] = (template[:, :, c] * 
                       (template[:, :, 3] / 255.0) + 
                        image[y: y + template.shape[0], 
                        x: x + template.shape[1], c] * 
                       (1.0 - template[:, :, 3] / 255.0))

            # Saving photo with replaced templates.
            cv2.imwrite(os.path.join(constant.PATH, save_path[18:]), image)

        # Deleting "rubbish"
        os.remove(os.path.join(constant.PATH_1, resized_name))


def bot_answer(message, bot, face_coordinates, total_t):
    """Bot's answer according to number of found faces 
    and sends friendly sticker."""
    number_faces = len(face_coordinates)
    if number_faces > 1:
        answer = f"""Your photo is ready in {total_t} seconds.
            \nFound {number_faces} faces."""
        bot.send_message(message.chat.id, answer)
        bot.send_sticker(message.chat.id, random.choice(constant.STICKERS_OK))

    elif number_faces == 1:
        answer = f"""Your photo is ready in {total_t} seconds.
            \nFound {number_faces} face."""
        bot.send_message(message.chat.id, answer)
        bot.send_sticker(message.chat.id, random.choice(constant.STICKERS_OK))

    else:
        answer = "There is not any face at this photo."
        bot.send_message(message.chat.id, answer)
        bot.send_sticker(message.chat.id, random.choice(constant.STICKERS_NO))
