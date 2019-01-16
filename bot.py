import os
from dotenv import load_dotenv
import telepot
from telepot.loop import MessageLoop
import time

def get_token():
    """ gets token from .env in current folder """

    cur_dir = os.curdir
    path = os.path.join(cur_dir, ".env")
    load_dotenv(path)
    token = os.environ.get("token")
    return token

class AudioConverterBot():
    def __init__(self, token):
        self.bot = telepot.Bot(token)
        self.formats = ["mp3", "wav", "ogg"]

    def convert_audio(self, chat_id, extension):
        """ converts audio from user with specified chat_id to specified extension """

        path = "audio/" + str(chat_id) + "." + extension
        self.bot.sendAudio(chat_id, open(path, "rb"))

    def handle_audio(self, chat_id, file_id):
        """ handles incoming audios
        saves sent audio in all formats from self.formats
        """

        self.bot.getFile(file_id)
        cur_dir = os.curdir
        for format in self.formats:
            path = os.path.join(cur_dir, "audio", str(chat_id) + "." + format)
            self.bot.download_file(file_id, path)

        self.bot.sendMessage(chat_id, "Ok. Now send me extension into which you want to convert this audio.")

    def handle_start(self, chat_id):
        """ handles /start """

        start_message = "Hey there!\nI am AudioConverterBot and I can convert your audio in another file format. Just send it to me."
        self.bot.sendMessage(chat_id, start_message)

    def handle_message(self, msg):
        """ handles incoming messages """

        _, _, chat_id = telepot.glance(msg)

        if "text" in msg: # if message has text field
            if msg["text"] == "/start":
                self.handle_start(chat_id)
            elif msg["text"] in self.formats: # if message is a file extension
                self.convert_audio(chat_id, msg["text"])
        if "audio" in msg: # if message has audio field
            file_id = msg["audio"]["file_id"]
            self.handle_audio(chat_id, file_id)

    def run(self):
        """ runs our bot :) """

        MessageLoop(self.bot, self.handle_message).run_as_thread()
        while True:
            time.sleep(5)

token = get_token()
bot = AudioConverterBot(token)
bot.run()
