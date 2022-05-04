# Notes

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