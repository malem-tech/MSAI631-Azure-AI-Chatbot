# # Copyright (c) Microsoft Corporation. All rights reserved.
# # Licensed under the MIT License.

# from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
# from botbuilder.schema import ChannelAccount


# class EchoBot(ActivityHandler):
#     async def on_members_added_activity(
#         self, members_added: [ChannelAccount], turn_context: TurnContext
#     ):
#         for member in members_added:
#             if member.id != turn_context.activity.recipient.id:
#                 await turn_context.send_activity("Hello and welcome!")

#     async def on_message_activity(self, turn_context: TurnContext):
#         return await turn_context.send_activity(
#             MessageFactory.text(f"Echo: {turn_context.activity.text}")
#         )


from typing import List

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hello and welcome! Type 'help' to see what I can do."
                )

    async def on_message_activity(self, turn_context: TurnContext):
        user_text = (turn_context.activity.text or "").strip().lower()

        if user_text in ["hello", "hi", "hey"]:
            response = (
                "Hello! I am a simple traditional chatbot. "
                "Type 'help' to see what I can do."
            )

        elif user_text in ["help", "capabilities", "what can you do"]:
            response = (
                "I can respond to greetings, explain this project, "
                "provide course information, and say goodbye."
            )

        elif "course" in user_text:
            response = (
                "This chatbot was created for MSAI 631: "
                "Artificial Intelligence for Human-Computer Interaction."
            )

        elif "project" in user_text:
            response = (
                "This project demonstrates a traditional rule-based chatbot "
                "that does not use a large language model."
            )

        elif user_text in ["bye", "goodbye", "exit"]:
            response = "Goodbye! Thanks for testing the chatbot."

        else:
            response = (
                "I'm sorry, I don't understand that request. "
                "Type 'help' to see the commands I understand."
            )

        await turn_context.send_activity(response)