// Nand2Tetris-I Capstone: Make the Computer Draw a Box
// Student: Shresth Priyadarshi
// Roll number: 2501420026
// K = 26
// Box: rows 26 through 45 (20 rows), 48 pixels wide (3 words).
// First screen word = SCREEN + 32*K = 16384 + 832 = 17216.

(LOOP)
    @KBD
    D=M
    @PRESSED
    D;JNE

    @color
    M=0
    @DRAW
    0;JMP

    @color
    M=-1


    @17216
    D=A
    @addr
    M=D

    @20
    D=A
    @rows
    M=D


    @color
    D=M
    @addr
    A=M
    M=D
    A=A+1
    M=D
    A=A+1
    M=D

    @32
    D=A
    @addr
    M=D+M

    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT

    @LOOP
    0;JMP
