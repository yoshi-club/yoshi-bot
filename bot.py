#!/usr/bin/env python3
import discord
import markopy.marko
from functor import Contains, StartsWith, And, Not, Equals
from action import SendResponse, MarkovGenerator

try:
    with open('auth.txt', mode='r') as file:
        auth = file.readline().strip(' \n\r')
except FileNotFoundError:
    print('auth.txt not found')
    exit()

with open('strings.txt', 'r') as file:
    strings = {}
    for line in  file:
        key, value = line.partition('=')[::2]
        strings[key.strip()] = value
commands = [
    (Contains('yoshi'), SendResponse(strings['yoshi'])),
    (Contains('uwu'), SendResponse(strings['uwu'])),
    (And(StartsWith('>tfw'), Not(StartsWith('>tfwnogf'))), SendResponse(strings['tfw'])),
    (StartsWith('>tfwnogf'), SendResponse(strings['tfwnogf'])),
    (Equals('turn that poop'), SendResponse('into wine')),
    (Equals('>sophistry'), MarkovGenerator('republic.txt'))
]

class BotClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
    async def on_message(self, message):
        if message.author != self.user:
            for command in commands:
                if command[0](message.content):
                    await command[1](message)

def start_client():
    client = BotClient()
    client.run(auth)

def main():
    start_client()

if __name__ == '__main__':
    main()