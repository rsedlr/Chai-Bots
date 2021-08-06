import json
import requests
import time
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer
from chai_py import ChaiBot, Update


class Bot(ChaiBot):
    chat_history_ids = None

    def setup(self):
        self.first_response = "Hey, I'm Rick."

        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
        self.model = AutoModelForCausalLM.from_pretrained("output-small")

    async def on_message(self, update: Update) -> str:
        # do we acc wanna use the first response?? Should we not just let rick respond??
        userResponse = update.latest_message.text

        if userResponse == self.FIRST_MESSAGE_STRING:
            # self.get_response("", True)
            return self.first_response

        return self.get_response(userResponse)
        # payload = await self.get_payload(update)
        # return self.query(payload)

    def query(self, payload):
        data = json.dumps(payload)
        response = requests.post(self.ENDPOINT, headers=self.headers, data=data)

        # if (response.status_code == 503):
        #     # This means we need to wait for the model to load 😴.
        #     estimated_time = response.json()["estimated_time"]
        #     time.sleep(estimated_time)
        #     self.logger.info(f"Sleeping for model to load: {estimated_time}")
        #     data = json.loads(data)
        #     data["options"] = {"use_cache": False, "wait_for_model": True}
        #     data = json.dumps(data)
        #     response = requests.post(self.ENDPOINT, headers=self.headers, data=data)

        return json.loads(response.content.decode("utf-8"))["generated_text"]

    async def get_payload(self, update):
        messages = await self.get_messages(update.conversation_id)
        past_user_inputs = ["Hey"]  # You can change this!
        generated_responses = [self.first_response]
        for message in messages:
            content = message.content
            if content == self.FIRST_MESSAGE_STRING:
                continue  # We're not trying to keep track of our FIRST_MESSAGE_STRING (i.e. "__first")
            if message.sender_uid == self.uid:
                # Put the user's messages into past_user_inputs
                past_user_inputs.append(content)
            else:
                # Put the model generated messages into here
                generated_responses.append(content)
            return {
                "inputs": {
                    "past_user_inputs": past_user_inputs,
                    "generated_responses": generated_responses,
                    "text": update.latest_message.text,
                },
            }

    def get_response(self, userResponse, firstMessage=False):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = self.tokenizer.encode(
            userResponse + self.tokenizer.eos_token, return_tensors="pt"
        )
        # print(new_user_input_ids)

        # append the new user input tokens to the chat history
        bot_input_ids = (
            torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1)
            if firstMessage
            else new_user_input_ids
        )

        # generated a response while limiting the total chat history to 1000 tokens
        self.chat_history_ids = self.model.generate(
            bot_input_ids,
            max_length=1000,  # maybe increase max_length
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8,
        )

        # pretty print last output tokens from bot
        return "{}".format(
            self.tokenizer.decode(
                self.chat_history_ids[:, bot_input_ids.shape[-1] :][0],
                skip_special_tokens=True,
            )
        )
