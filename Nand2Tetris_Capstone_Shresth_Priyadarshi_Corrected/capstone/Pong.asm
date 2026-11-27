// Compact Pong-named assembler smoke-test fixture (not the full course game).
// Reads the keyboard and repeatedly writes the key value to SCREEN[0].
(LOOP)
@KBD
D=M
@SCREEN
M=D
@LOOP
0;JMP
