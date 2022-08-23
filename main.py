import discord
from mycustomclient import MyClient

if __name__ == '__main__':
    token = ''

    with open('token.txt', 'r') as f:
        token = f.readline()

    mycustomclient = MyClient()
    mycustomclient.run(token)
