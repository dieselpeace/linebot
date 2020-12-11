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

app = Flask(__name__)

line_bot_api = LineBotApi('AKqqyBznmYQOaXCY7J3SMp5dP+tZoVxi2hBzmiB1I4JsNTSt9uDpth9auOLx+Mz1IvNNix3u1gn9HwuJxjwS3hYx28S0FM8tSAntIIAQrkEcHJtPz36qMK4lPMA8kWbb/vDvIC1T60zai08zUOjrOAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('268bad15d45220b168ddb473f236e935')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()