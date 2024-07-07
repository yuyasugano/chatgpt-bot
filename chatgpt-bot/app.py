import os
import json
import logging

from openai import OpenAI
from linebot import LineBotApi
from linebot.models import TextSendMessage

logger = logging.getLogger()
logger.setLevel(logging.INFO)

OPENAI_KEY = os.environ.get("OPENAI_KEY")
CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")

def lambda_handler(event, context):
    reqBody = json.loads(event["body"]);
    logger.info("Request Body: " + json.dumps(reqBody));

    if reqBody["events"][0]["message"]["type"] == "text":
        client = OpenAI(
            api_key = OPENAI_KEY,
        );

        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            # prompt = reqBody["events"][0]["message"]["text"],
            messages = [
                { "role": "user", "content": reqBody["events"][0]["message"]["text"] }
            ],
            max_tokens = 1000,
            temperature = 0
        );

        # message = completion.choices[0].text.strip();
        message = completion.choices[0].message.content.strip();
    else:
        message = "only text input is accepted.";

    if reqBody["events"][0]["source"]["type"] == "user":
        toId = reqBody["events"][0]["source"]["userId"];
    elif reqBody["events"][0]["source"]["type"] == "group":
        toId = reqBody["events"][0]["source"]["groupId"];
    elif reqBody["events"][0]["source"]["type"] == "room":
        toId = reqBody["events"][0]["source"]["roomId"];

    try:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN);
        messages = TextSendMessage(text=message);
        line_bot_api.push_message(toId, messages);
    except Exception as e:
        logger.info("Exception raised: " + json.dumps(e));

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }

