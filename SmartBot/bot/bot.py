import json
import requests
import time

from chai_py import ChaiBot, Update


class Bot(ChaiBot):
    def setup(self):
        self.ENDPOINT = (
            # "https://api-inference.huggingface.co/models/hyunwoongko/reddit-3B"
            # "https://api-inference.huggingface.co/models/abhiramtirumala/DialoGPT-sarcastic"
            "https://api-inference.huggingface.co/models/odinmay/joebot"
        )
        self.headers = {
            "Authorization": "Bearer api_oieZbocfGuGxzuQozzaqpFYnBrpBsSLwzP"
        }
        self.first_response = "Hey, I'm Joe."

    async def on_message(self, update: Update) -> str:
        if update.latest_message.text == self.FIRST_MESSAGE_STRING:
            return self.first_response
        payload = await self.get_payload(update)
        return self.query(payload)

    def query(self, payload):
        data = json.dumps(payload)
        response = requests.post(self.ENDPOINT, headers=self.headers, data=data)
        if (
            response.status_code == 503
        ):  # This means we need to wait for the model to load 😴.
            estimated_time = response.json()["estimated_time"]
            time.sleep(estimated_time)
            self.logger.info(f"Sleeping for model to load: {estimated_time}")
            data = json.loads(data)
            data["options"] = {"use_cache": False, "wait_for_model": True}
            data = json.dumps(data)
            response = requests.post(self.ENDPOINT, headers=self.headers, data=data)
        return json.loads(response.content.decode("utf-8"))["generated_text"]

    async def get_payload(self, update):
        messages = await self.get_messages(update.conversation_id)
        past_user_inputs = ["Hey", "How old are you?"]  # You can change this!
        generated_responses = [self.first_response, "69 years old"]
        for message in messages:
            content = message.content
            if content == self.FIRST_MESSAGE_STRING:
                continue  # We're not trying to keep track of our FIRST_MESSAGE_STRING (i.e. "__first")
            if message.sender_uid == self.uid:
                past_user_inputs.append(
                    content
                )  # Put the user's messages into past_user_inputs
            else:
                generated_responses.append(
                    content
                )  # Put the model generated messages into here
            return {
                "inputs": {
                    "past_user_inputs": past_user_inputs,
                    "generated_responses": generated_responses,
                    "text": update.latest_message.text,
                },
            }
