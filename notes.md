# Notes

## NEXT: recreate mockbot pictures inside new chessbots module (feb 23)


- You need 5 bits to address each bot (31 => 11111).
- Yoou need 3 bits to address a piece name (6+1 => 111)
- With fieldsize 2000mm, you can have a piece diameter of 140mm ((2000 / 10) * 0.70) (0.75 would be touching, so 10% tolerance)



```
esp32 camera pinout:
f = flash
p  = piece display (4x)
b = piece select button (1x)
s = status led (1x)
m = motor

bottom:
mf  5v
sbp gnd
p 12
p 13
p 14
p 15
s 2
b 4

top:
3.3V
16
f  0
gnd
3,3/5V
mf  3
mf  1
mf  GND


- - - - - 
2x2 matrix piece display
?=top-left is color, rest is piece

?x
xx  - 111 king 7

?x
0x - 101 queen 5

?0
0x - 001 bishop 1

?0
x0 - 010 night 2

?0
xx - 011 rook 3

?0
00 - 000 pawn 0

?x
x0 - 110 special 6

?x
00 - 100 special 4

```



0010
0111
0001
0000


## Micropython

https://lemariva.com/blog/2019/09/micropython-how-about-taking-photo-esp32

```bash
export MICROPYTHON=$PWD
. venv/bin/activate
pip3 install pyserial pyparsing
```



# 

        '''
            1x1 1x1   2x1 2x1   3x1 3x1  
            1x1 1x1   2x1 2x1   3x1 3x1
        
            1x2 1x2   2x2 2x2   3x2 3x2
            1x2 1x2   2x2 2x2   3x2 3x2
        
            1x3 1x3   2x3 2x3   3x3 3x3
            1x3 1x3   2x3 2x3   3x3 3x3
        
        -
            1x1   1x1 2x1   2x1 3x1   3x1
              
            1x1   1x1 2x1   2x1 3x1   3x1 4x1
            1x2   1x2 2x2   2x2 3x2   3x2 4x2
            
            1x2   1x2 2x2   2x2 3x2   3x2
            1x3   1x3 2x3   2x3 3x3   3x3
            
            1x3   1x3 2x3   2x3 3x3   3x3
        -
        
        0x0  0x0
            0x0 0x0  
            0x0 0x0
        0x1  0x4
            0x0 0x0  
            0x1 0x1
        1x0  4x0:
            0x0 1x0  
            0x0 1x0
        1x1  4x4
            0x0 1x0
            0x1 1x1
        2x2 8x8
            1x1 1x1
            1x1 1x1
        3x3 12x12
            1x1 2x1
            1x2 2x2
        4x4 16x16
            2x2 2x2
            2x2 2x2
        5x5
           2x2 3x2
           2x3 3x3

            # 0 - 1x1 1x1 1x1 1x1 
        '''


0......10......10......10......10......10......1
.-....-..-....-..-....-..-....-..-....-..-....-.
..-..-....-..-....-..-....-..-....-..-....-..-..
...00......00......00......00......00......00...
...01......01......01......01......01......01...
..-..-....-..-....-..-....-..-....-..-....-..-..
.-....-..-....-..-....-..-....-..-....-..-....-.
1......11......11......11......11......11......1
0......10......10......10......10......10......1
.-....-..-....-..-....-..-....-..-....-..-....-.
..-..-....-..-....-..-....-..-....-..-....-..-..
...00......00......00......00......00......00...
...01......01......01......01......01......01...
..-..-....-..-....-..-....-..-....-..-....-..-..
.-....-..-....-..-....-..-....-..-....-..-....-.
1......11......11......11......11......11......1
0......10......10......10......10......10......1
.-....-..-....-..-....-..-....-..-....-..-....-.
..-..-....-..-....-..-....-..-....-..-....-..-..
...00......00......00......00......00......00...
...01......01......01......01......01......01...
..-..-....-..-....-..-....-..-....-..-....-..-..
.-....-..-....-..-....-..-....-..-....-..-....-.
1......11......11......11......11......11......1




# Arduino setup:

Arduino IDE Board manager settings:
https://dl.espressif.com/dl/package_esp32_index.json

Goto Tools -> Board -> Board manager
    -> download esp32 expressif systems stuff



# board json payload

```json

{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "bots": [],
  "board": {
    "pieces": [
      {
        "piece": "bq",
        "field": [
          "a",
          "1"
        ],
        "bot_pos": [
          300,
          300
        ]
      }
    ],
    "rest_bots": [
      {
        "piece": "wk",
        "pos": [
          100,
          100
        ]
      }
    ]
  }
}

```