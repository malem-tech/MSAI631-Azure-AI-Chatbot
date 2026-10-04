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
    def __init__(self, text_analytics_client):
        self.text_analytics_client = text_analytics_client

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hello and welcome! Type 'help' to see what I can do."
                )

    async def on_message_activity(self, turn_context: TurnContext):
        user_text = (turn_context.activity.text or "").strip()
        normalized_text = user_text.lower()

        if normalized_text in ["hello", "hi", "hey"]:
            response = (
                "Hello! I am a traditional chatbot connected to Azure AI Language. "
                "Type 'help' to see what I can do."
            )

        elif normalized_text in ["help", "capabilities", "what can you do"]:
            response = (
                "I can respond to greetings, explain this project, provide course "
                "information, and analyze sentiment using Azure AI Language. "
                "Try typing: sentiment I really enjoyed this project"
            )

        # Check sentiment requests before broader keyword rules.
        elif normalized_text.startswith("sentiment "):
            text_to_analyze = user_text[len("sentiment "):].strip()

            if not text_to_analyze:
                response = (
                    "Please provide text after the word 'sentiment'. "
                    "For example: sentiment I love this class"
                )
            else:
                try:
                    result = self.text_analytics_client.analyze_sentiment(
                        documents=[text_to_analyze]
                    )[0]

                    if result.is_error:
                        response = (
                            "Azure AI Language could not analyze that text. "
                            "Please try again."
                        )
                    else:
                        response = (
                            f"Azure AI Language detected the sentiment as "
                            f"{result.sentiment}.\n"
                            f"Positive score: "
                            f"{result.confidence_scores.positive:.2f}\n"
                            f"Neutral score: "
                            f"{result.confidence_scores.neutral:.2f}\n"
                            f"Negative score: "
                            f"{result.confidence_scores.negative:.2f}"
                        )

                except Exception as error:
                    response = (
                        "I could not connect to Azure AI Language. "
                        f"Error: {str(error)}"
                    )

        elif "course" in normalized_text:
            response = (
                "This chatbot was created for MSAI 631: "
                "Artificial Intelligence for Human-Computer Interaction."
            )

        elif "project" in normalized_text:
            response = (
                "This project extends a traditional rule-based chatbot by connecting "
                "it to Azure AI Language for sentiment analysis."
            )

        elif normalized_text in ["bye", "goodbye", "exit"]:
            response = "Goodbye! Thanks for testing the chatbot."

        else:
            response = (
                "I'm sorry, I don't understand that request. "
                "Type 'help' to see the commands I understand."
            )

        await turn_context.send_activity(response)