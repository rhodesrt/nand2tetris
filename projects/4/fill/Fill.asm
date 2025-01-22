// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// Screen is 32x16 (16 bit)
// KBD is either an input or 0

// LOOP
// Check if key is pressed
// If pressed, write -1 to all SCREEN registers
// Else, write 0 to all SCREEN registers

(LOOP)
@512
D=A
@count
M=D
@n
M=0
@SCREEN
D=A
@current
M=D

@KBD
D=M
@WHITE
D;JEQ
@BLACK
D;JNE

(WHITE)
@n
D=M
@count
D=D-M
@LOOP
D;JEQ

@current
A=M
M=0
@current
M=M+1

@n
M=M+1
@WHITE
0;JMP

(BLACK)
@n
D=M
@count
D=D-M
@LOOP
D;JEQ

@current
A=M
M=-1
@current
M=M+1

@n
M=M+1
@BLACK
0;JMP

@LOOP
0;JMP