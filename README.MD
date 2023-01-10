# Commision Work
* This code was originally commisioned by KimchiCurryTV on twitch to use on her stream.

# Example Setup
* The current set up is setup to grab the user name of whoever redeemed the "cutest" or "best" viewer reward using channel points.
* The grabbed user names then will be written into the html file which updates to the most recent redeemed viewer. Ex- Cutested viewer on Earth: ....

# Setup topics, auth and install requirement
* Open `webSocketClient.py` and edit value for `self.topics` and `self.auth_token` to include your channel id for channel you want to listen to and auth token for the channel
* Replace reward ID with you're specific reward ID
* Install the requirement with `pip3 install websockets`
* import the html file as a broswer source into your stream elements or other streaming app. (Tested only on streamlabs). Ajust size to liking.

# Run the pubsub client
`python3 main.py`

# Note
* Auth token for channel must have required scopes for topic you want to listen to.
* This client doesnt handle all the connection management, for ex. it doen't reconnect when twitch send `RECONNECT` signal or when connection between this client and twitch has failed.
* Please refer to Twitch's official documents to see how connections should be handled <https://dev.twitch.tv/docs/pubsub#connection-management>
* Credit to @SlackingVeteran for the PubSub Websocket recieve message code
