# client-and-server-apps-for-work-with-metrics
final project of MIPT course about Python3

This project is endpoint of my education via MIPT and Mail.ru group course at Coursera

First part is the client for sending metrics
It's synchronous app for sending metrics in to the server or receiving them from it.
Client can determine right response, handles it and returns notification about successful operation. If response is wrong
client raises ClientError

Second part is the server part.
Server provides opportunities for a safekeeping of metrics in frames of current session and sending them on request from clients.
Server is asynchronous bases on Asyncio and supports work with several clients at a time.

Conversation between these apps defined by rigorous protocol of interaction
