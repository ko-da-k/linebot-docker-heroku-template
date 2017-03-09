import os
import json
from flask import Flask, request, abort
from wsgiref import simple_server

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, SourceUser, LocationMessage, StickerMessage,
                            ImageMessage, AudioMessage, VideoMessage)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask(__name__)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    target = event.reply_token
    if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        print(profile.display_name)
    else:
        print("not catch source")
    line_bot_api.reply_message(target, TextSendMessage(text=event.message.text))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    target = event.reply_token
    if isinstance(event.message, LocationMessage):
        address = event.message.address
        lat = event.message.latitude
        lon = event.message.longitude
    line_bot_api.reply_message(target, TextSendMessage(text="{0}\n{1}\n{2}".format(address,lat,lon)))


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    pass


# other message
@handler.add(MessageEvent, message=[ImageMessage, VideoMessage, AudioMessage])
def handle_content_message(event):
    pass


if __name__ == "__main__":
    app.run()
