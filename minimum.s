# minimum.asm program
# CS 64, Z.Matni, zmatni@ucsb.edu
#

#Text Area (i.e. instructions)
# add, and, slt, addi, lui, ori, lw, sw, beq
.text

main:
  addi $t0, $zero, 15
  addi $t1, $zero, -42

  sw $t0, 0($zero)
  sw $t1, 1($zero)

  lw $t2, 0($zero)
  lw $t3, 1($zero)

  # assert these
  add $t4, $t2, $t3 # -27
  slt $t5, $t4, $zero # 1
  and $t6, $t5, $zero # 0
  ori $s1, $t4, 0 # -27

  addi $t7, $zero, -27

  beq $t4, $t7, randomthing

  addi $t4, $zero, 314
  sw $t4, 2($zero)

  beq $zero, $zero, exit

  randomthing:
    lui $s0, 1 # 65536

exit:
  lw $v0, 0($zero)           # $v0 = mem[0]
  beq $v0, $v0, exit         # goto exit
