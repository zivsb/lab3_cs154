
	USER TEXT SEGMENT
[0x00400000]	0x2008000f  addi $8, $0, 15                 ; 10: addi $t0, $zero, 15
[0x00400004]	0x2009ffd6  addi $9, $0, -42                ; 11: addi $t1, $zero, -42
[0x00400008]	0xac080000  sw $8, 0($0)                    ; 13: sw $t0, 0($zero)
[0x0040000c]	0xac090001  sw $9, 1($0)                    ; 14: sw $t1, 1($zero)
[0x00400010]	0x8c0a0000  lw $10, 0($0)                   ; 16: lw $t2, 0($zero)
[0x00400014]	0x8c0b0001  lw $11, 1($0)                   ; 17: lw $t3, 1($zero)
[0x00400018]	0x014b6020  add $12, $10, $11               ; 20: add $t4, $t2, $t3 # -27
[0x0040001c]	0x0180682a  slt $13, $12, $0                ; 21: slt $t5, $t4, $zero # 1
[0x00400020]	0x01a07024  and $14, $13, $0                ; 22: and $t6, $t5, $zero # 0
[0x00400024]	0x35910000  ori $17, $12, 0                 ; 23: ori $s1, $t4, 0 # -27
[0x00400028]	0x200fffe5  addi $15, $0, -27               ; 25: addi $t7, $zero, -27
[0x0040002c]	0x118f0003  beq $12, $15, 12 [randomthing-0x0040002c]; 27: beq $t4, $t7, randomthing
[0x00400030]	0x200c013a  addi $12, $0, 314               ; 29: addi $t4, $zero, 314
[0x00400034]	0xac0c0002  sw $12, 2($0)                   ; 30: sw $t4, 2($zero)
[0x00400038]	0x10000001  beq $0, $0, 4 [exit-0x00400038] ; 32: beq $zero, $zero, exit
[0x0040003c]	0x3c100001  lui $16, 1                      ; 35: lui $s0, 1 # 65536
[0x00400040]	0x8c020000  lw $2, 0($0)                    ; 38: lw $v0, 0($zero)           # $v0 = mem[0]
[0x00400044]	0x1042fffe  beq $2, $2, -8 [exit-0x00400044]; 39: beq $v0, $v0, exit         # goto exit
