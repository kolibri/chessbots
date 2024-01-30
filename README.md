[![Creative Commons BY NC SA](https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

# Chessbots

## What is this about?

You probably have seen something like this:
[![Street chess picture from wikipedia](./devblog/images/street-chess-wikipedia.jpg)](https://commons.wikimedia.org/wiki/File:Katushakki_-_Street_chess,_Finland.jpg)

My idea is, to make the pieces movable. You play a game on your mobile phone or any other device that has a webbrowser, and the real pieces on the street will also make every move you and your opponent will make.

So, we are talking about 32 individual robots, each one is a selfmoving chesspiece, that play our game.

## Concept, Idea

Each piece is build with a ESP32-CAM board with two wheel attached, camera facing down. So we talk about a robot, that takes a picture of what is under it.
Hopefully, this is the board, that we play on. Because, this will have special markings, that help us to determine the position of the bot and where it is heading at.
Because, if we know that, we can check all the positions against an ongoing chess game, and so on.
This is the first main goals: Make the bots recognize its position and make it able to move to another position.

This is a very early project state. And it is slow moving. 

You may contact me (have a look at my github profile, or leave an issue), if you are interested in this project or want to contribute. There are plenty of issues, that are not solved yet. (languages I understand: german and english)

## Languages

Python (Flask), Micropython, ReactJs for Debug Frontend

Docker for dev env
