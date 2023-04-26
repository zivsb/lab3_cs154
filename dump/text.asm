
	USER TEXT SEGMENT
[0x00400000]	0x01004024  and $8, $8, $0                  ; 20: and $t0, $t0, $zero        # $t0 = 0
[0x00400004]	0x01204824  and $9, $9, $0                  ; 21: and $t1, $t1, $zero        # $t1 = 10
[0x00400008]	0x2129000a  addi $9, $9, 10                 ; 22: addi $t1, $t1, 10
[0x0040000c]	0x11090006  beq $8, $9, 24 [exit-0x0040000c]; 25: beq $t0, $t1, exit         # if ($t0 == 10) exit
[0x00400010]	0x01405024  and $10, $10, $0                ; 27: and $t2, $t2, $zero        # $t2 = 0
[0x00400014]	0x8d4b0000  lw $11, 0($10)                  ; 28: lw $t3, 0($t2)             # $t3 = mem[$t2]
[0x00400018]	0x216b0001  addi $11, $11, 1                ; 29: addi $t3, $t3, 1           # $t3 += 1
[0x0040001c]	0xad4b0000  sw $11, 0($10)                  ; 30: sw $t3, 0($t2)             # mem[$t2] = $t3
[0x00400020]	0x21080001  addi $8, $8, 1                  ; 32: addi $t0, $t0, 1           # $t0 += 1
[0x00400024]	0x1000fff9  beq $0, $0, -28 [loop-0x00400024]; 33: beq $zero, $zero, loop     # goto loop
[0x00400028]	0x8c020000  lw $2, 0($0)                    ; 36: lw $v0, 0($zero)           # $v0 = mem[0]
[0x0040002c]	0x1042fffe  beq $2, $2, -8 [exit-0x0040002c]; 37: beq $v0, $v0, exit         # goto exit
