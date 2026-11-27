// Test program: draws a rectangle 16 pixels wide and R0 pixels high
// R0 must contain a positive height before execution.
@R0
D=M
@n
M=D
@SCREEN
D=A
@addr
M=D
(LOOP)
    @n
    D=M
    @END
    D;JEQ
    @addr
    A=M
    M=-1
    @addr
    M=M+1
    @n
    M=M-1
    @LOOP
    0;JMP
(END)
    @END
    0;JMP
