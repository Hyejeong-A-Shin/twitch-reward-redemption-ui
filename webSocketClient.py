import websockets
import asyncio
import uuid
import json
import webbrowser
from bs4 import BeautifulSoup

class WebSocketClient():

    def __init__(self):
        # list of topics to subscribe to
        self.topics = ["channel-points-channel-v1.<ChannelID>"]
        self.auth_token = "<Auth_Token>"
        pass

    def write_in_html(self, display_name, reward_type):
        with open("userDisplay.html", "r", encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, "html.parser")
        if (reward_type == 'cutest'):
            tag = soup.h9
            tag.string = display_name
        if (reward_type == 'best'):
            tag = soup.h10
            tag.string = display_name
        soup_file = str(soup)
        
        with open("userDisplay.html", "w", encoding="utf-8") as outfile:
            outfile.write(soup_file)   

    async def connect(self):
        '''
           Connecting to webSocket server
           websockets.client.connect returns a WebSocketClientProtocol, which is used to send and receive messages
        '''
        self.connection = await websockets.connect('wss://pubsub-edge.twitch.tv')
        if self.connection.open:
            print('Connection stablished. Client correcly connected')
            # Send greeting
            message = {"type": "LISTEN", "nonce": str(self.generate_nonce()), "data":{"topics": self.topics, "auth_token": self.auth_token}}
            json_message = json.dumps(message)
            await self.sendMessage(json_message)
            return self.connection

    def generate_nonce(self):
        '''Generate pseudo-random number and seconds since epoch (UTC).'''
        nonce = uuid.uuid1()
        oauth_nonce = nonce.hex
        return oauth_nonce

    async def sendMessage(self, message):
        '''Sending message to webSocket server'''
        await self.connection.send(message)

    async def receiveMessage(self, connection):

        #function to overwrite user name for reward redeemed
        
        '''Receiving all server messages and handling them'''
        while True:
            try:
                message = await connection.recv()
                print('Received message from server: ' + str(message))
                #load recieved message into json file
                message_body = json.loads(message)

                #checking if required data in message body
                if "data" in message_body:
                    if "message" in message_body['data']:
                        messageBody = json.loads(message_body['data']['message'])
                        reward_id = messageBody['data']['redemption']['reward']['id']
                        display_name = messageBody['data']['redemption']['user']['display_name']
                        # if reward redeemed is cutest viewer on earth
                        if reward_id == "<your reward id for the redemption>":
                            self.write_in_html(display_name, 'cutest')
                        # if reward redeemed is best viwer on earth
                        if reward_id == "<your reward id for the redemption>":
                            self.write_in_html(display_name, 'best')
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

    async def heartbeat(self, connection):
        '''
        Sending heartbeat to server every 1 minutes
        Ping - pong messages to verify/keep connection is alive
        '''
        while True:
            try:
                data_set = {"type": "PING"}
                json_request = json.dumps(data_set)
                print(json_request)
                await connection.send(json_request)
                await asyncio.sleep(60)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break
    