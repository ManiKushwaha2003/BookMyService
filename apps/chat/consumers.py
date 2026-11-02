import asyncio
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from .rag import get_chatbot_response


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept"
        })

        await self.send({
            "type": "websocket.send",
            "text": "Hello! I am BookMyService Assistant. Ask me anything."
        })

    async def websocket_receive(self, event):
        question = (event.get("text") or "").strip()


        try:
            response = await asyncio.to_thread(
                get_chatbot_response,
                question
            )

            await self.send({
                "type": "websocket.send",
                "text": str(response)
            })

        except Exception as e:
            print("Chatbot error:", e)



    async def websocket_disconnect(self, event):
        print("Disconnected:", event)
        raise StopConsumer()