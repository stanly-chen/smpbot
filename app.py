from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import requests

import os

app = Flask(__name__)


# 填入你的 message api 資訊
line_bot_api = LineBotApi('SRUcrtdO+7KHgmCOyyuVhJqDHI1BID+W3lyUaxrBZKF7PZ8MxeRNU1m7b2/CqyYwUDgZuj9QKF5KIbKTz+5BDy811+w4W9gBb/sdqbgfnWoC7o8S2MsqDajt6m38Aamx0S2ToSf+C8GD3pf2bn8wDgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('495192b49d94de1ef72da683cd3cf3f4')

# 設定你接收訊息的網址，如 https://YOURAPP.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    content = "{}: {}".format(event.source.user_id, event.message.text)

    text = event.message.text
    if text.lower() == 'me':
        content = str(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
            )
    elif text.lower() == 'open':
        content = '已為您啟動'
        param = {'temp': '1', 'wet': '1000'}
        requests.get('https://dweet.io/dweet/for/stanlykuasled', params=param)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
            )

     
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['PORT'])