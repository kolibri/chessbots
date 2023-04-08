[![Creative Commons BY NC SA](https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

# Chessbots

## What is this about?

You probably have seen something like this:
[![Street chess picture from wikipedia](./devblog/images/street-chess-wikipedia.jpg)](https://commons.wikimedia.org/wiki/File:Katushakki_-_Street_chess,_Finland.jpg)

My idea is, to make the pieces movable. You play a game on your mobile phone or any other device that has a webbrowser, and the real pieces on the street will also make every move you and your opponent will make.

So, we are talking about 32 individual robots, each one is a selfmoving chesspiece, that play our game.

## Conecpt, Idea, or what I am prototyping

Each piece is build with a ESP32-CAM board with two wheel attached, camera facing down. So we talk about a robot, that takes a picture of what is under it.
Hopefully, this is the board, that we play on. Because, this will have special markings, that help us to determine the position of the bot and where it is heading at.
Because, if we know that, we can check all the positions against an ongoing chess game, and so on.
This is the first main goals: Make the bots recognize its position and make it able to move to another position.

[.] Make the bots recognice their positions
    [.] Make the Position Picture readable by opencv
    [x] Find marker points in position picture
    [x] Transform found marker to a Grid
    [x] Resolve GridPattern to a position
[ ] Make the bots able to move to another position
    [ ] Build a moveable robot
    [ ] Switch on the LED!!!
    [ ] Register this robot as chessbot
        Native|Via Mockbot
[.] Frontend tools
    [x] Field view
    [x] Bot overview
    [.] Bot register
    




This is a very early project state.  I'm prototyping the general concepts of how to move, how to keep track of movements, how to power each robot long enough for at least one game, and so on.

You may contact me (have a look at my github profile, or leave an issue), if you are interested in this project or want to contribute. There are plenty of issues, that are not solved yet. (languages I understand: german and english)

## Languages

Currently: Arduino with C, rest mostly HTML+Javascript, OpenCV-Research with python

Goal: All with python.

# Devblog 

newest first

- [2022-04-26 complete restart with python](devblog/2022-04-26-the_case_with_snakes.md)
- [2018-09-26 independent from arduino ide](devblog/2018-09-26-independent-from-arduino-ide.md)
- [2018-08-05 soldered motor board and nfc testing](devblog/2018-08-05-soldered-motor-board-and-nfc-testing.md)
- [2018-06-26 controlling wheels](devblog/2018-06-26-controlling-wheels.md)