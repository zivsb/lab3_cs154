import pyrtl

# ucsbcs154lab3
# All Rights Reserved
# Copyright (c) 2023 Regents of the University of California
# Distribution Prohibited


# Initialize your memblocks here: 
i_mem = pyrtl.MemBlock(bitwidth=32, addrwidth=32)
d_mem = pyrtl.MemBlock(bitwidth=32, addrwidth=32, asynchronous=True)
rf = pyrtl.MemBlock(bitwidth=32, addrwidth=5, asynchronous=True)
pc = pyrtl.Register(bitwidth=32)

# When working on large designs, such as this CPU implementation, it is
# useful to partition your design into smaller, reusable, hardware
# blocks. We have indicated where you should put different hardware blocks 
# to help you get write your CPU design. You have already worked on some 
# parts of this logic in prior labs, like the decoder and alu.

## DECODER
# decode the instruction


instr = i_mem[pc]

op = pyrtl.WireVector(bitwidth=6, name='op')
rs = pyrtl.WireVector(bitwidth=5, name='rs')
rt = pyrtl.WireVector(bitwidth=5, name='rt')
rd = pyrtl.WireVector(bitwidth=5, name='rd')
sh = pyrtl.WireVector(bitwidth=5, name='sh')
func = pyrtl.WireVector(bitwidth=6, name='func')
imm = pyrtl.WireVector(bitwidth=16, name='imm')
addr = pyrtl.WireVector(bitwidth=26, name='addr')

op <<= instr[26:32]
rs <<= instr[21:26]
rt <<= instr[16:21]
rd <<= instr[11:16]
sh <<= instr[6:11]
func <<= instr[0:6]
imm <<= instr[0:16]
addr <<= instr[0:26]

## CONTROLLER
# define control signals for the following instructions
# add, and, addi, lui, ori, slt, lw, sw, beq
REG_DST = pyrtl.WireVector(bitwidth=1, name='REG_DST')
BRANCH = pyrtl.WireVector(bitwidth=1, name='BRANCH')
REGWRITE = pyrtl.WireVector(bitwidth=1, name='REGWRITE')
ALU_SRC = pyrtl.WireVector(bitwidth=2, name='ALU_SRC')
MEM_WRITE = pyrtl.WireVector(bitwidth=1, name='MEM_WRITE')
MEM_TO_REG = pyrtl.WireVector(bitwidth=1, name='MEM_TO_REG')
ALU_OP = pyrtl.WireVector(bitwidth=3, name='ALU_OP')

with pyrtl.conditional_assignment:
   # r-types
   with op == 0:
      # Add
      with func == 0x20:
         REG_DST |= 1
         BRANCH |= 0
         REGWRITE |= 1
         ALU_SRC |= 0
         MEM_WRITE |= 0
         MEM_TO_REG |= 0
         ALU_OP |= 0
      # And
      with func == 0x24:
         REG_DST |= 1
         BRANCH |= 0
         REGWRITE |= 1
         ALU_SRC |= 00
         MEM_WRITE |= 0
         MEM_TO_REG |= 0
         ALU_OP |= 1
      # SLT
      with func == 0x2a:
         REG_DST |= 1
         BRANCH |= 0
         REGWRITE |= 1
         ALU_SRC |= 0
         MEM_WRITE |= 0
         MEM_TO_REG |= 0
         ALU_OP |= 4
   # Addi
   with op == 0x8:
      REG_DST |= 0
      BRANCH |= 0
      REGWRITE |= 1
      ALU_SRC |= 0
      MEM_WRITE |= 0
      MEM_TO_REG |= 0
      ALU_OP |= 0
   # Lui
   with op == 0xf:
      REG_DST |= 0
      BRANCH |= 0
      REGWRITE |= 1
      ALU_SRC |= 1
      MEM_WRITE |= 0
      MEM_TO_REG |= 1
      ALU_OP |= 2
   # Ori
   with op == 0xd:
      REG_DST |= 0
      BRANCH |= 0
      REGWRITE |= 1
      ALU_SRC |= 2
      MEM_WRITE |= 0
      MEM_TO_REG |= 1
      ALU_OP |= 3
   # Lw
   with op == 0x23:
      REG_DST |= 0
      BRANCH |= 0
      REGWRITE |= 1
      ALU_SRC |= 1
      MEM_WRITE |= 0
      MEM_TO_REG |= 1
      ALU_OP |= 0
   # Sw
   with op == 0x23:
      BRANCH |= 0
      REGWRITE |= 0
      ALU_SRC |= 1
      MEM_WRITE |= 1
      ALU_OP |= 0
   # Beq
   with op == 0x23:
      BRANCH |= 1
      REGWRITE |= 0
      ALU_SRC |= 00
      MEM_WRITE |= 0
      ALU_OP |= 5
       
      

## WRITE REGISTER mux
# create the mux to choose among rd and rt for the write register
write_reg = pyrtl.WireVector(bitwidth=32, name="write_reg")

with pyrtl.conditional_assignment:
   with REG_DST == 1:
      rf[rd] |= write_reg
   with REG_DST == 0:
      rf[rt] |= write_reg


## READ REGISTER VALUES from the register file
# read the values of rs and rt registers from the register file
rdata1 = pyrtl.WireVector(bitwidth=32, name='rdata1')
rdata2 = pyrtl.WireVector(bitwidth=32, name='rdata2')
rdata1 <<= rf[rs]
rdata2 <<= rf[rt]

## ALU INPUTS
# define the ALU inputs after reading values of rs and rt registers from
# the register file
# Hint: Think about ALU inputs for instructions that use immediate values
alu_inpt1 = pyrtl.WireVector(bitwidth=32, name="alu_inpt1")
alu_inpt2 = pyrtl.WireVector(bitwidth=32, name="alu_inpt2")

alu_inpt1 <<= rdata1
with pyrtl.conditional_assignment:
   with ALU_SRC == 0:
      alu_inpt2 |= rdata2
   with ALU_SRC == 1:
      alu_inpt2 |= imm.sign_extended(bitwidth=32)
   with ALU_SRC == 2:
      alu_inpt2 |= imm.zero_extended(bitwidth=32)

## FIND ALU OUTPUT
# find what the ALU outputs are for the following instructions:
# add, and, addi, lui, ori, slt, lw, sw, beq
# Hint: you want to find both ALU result and zero. Refer the figure in the
# lab document
alu_out = pyrtl.WireVector(bitwidth=32, name="alu_out")

with pyrtl.conditional_assignment:
   with ALU_OP == 0:
      # Add, Sw, Addi, Lw
      alu_out |= alu_inpt1 + alu_inpt2
   with ALU_OP == 1:
      # And
      alu_out |= alu_inpt1 & alu_inpt2
   with ALU_OP == 2:
      # Lui
      alu_out |= alu_inpt1 + pyrtl.shift_left_logical(alu_inpt2, pyrtl.Const(16))
   with ALU_OP == 3:
      # Or
      alu_out |= alu_inpt1 | alu_inpt2
   with ALU_OP == 4:
      # Slt
      alu_out |= alu_inpt1 < alu_inpt2
   with ALU_OP == 5:
      # Sub
      alu_out |= alu_inpt1 - alu_inpt2


## DATA MEMORY WRITE
# perform the write operation in the data memory. Think about which 
# instructions will need to write to the data memory
with pyrtl.conditional_assignment:
   with MEM_WRITE == 0:
      d_mem[alu_out] |= rdata2

## REGISTER WRITEBACK
# Create the mux to select between ALU result and data memory read.
# Writeback the selected value to the register file in the 
# appropriate write register
with pyrtl.conditional_assignment:
   with MEM_TO_REG == 1:
      #Choose the mem read
      write_reg |= d_mem[alu_out]
   with MEM_TO_REG == 0:
      # Choose ALU out 
      write_reg |= alu_out

## PC UPDATE
# finally update the program counter. Pay special attention when updating 
# the PC in the case of a branch instruction. 
pc.next <<= pc + 1


if __name__ == '__main__':

    """

    Here is how you can test your code.
    This is very similar to how the autograder will test your code too.

    1. Write a MIPS program. It can do anything as long as it tests the
       instructions you want to test.

    2. Assemble your MIPS program to convert it to machine code. Save
       this machine code to the "i_mem_init.txt" file. You can use the 
       "mips_to_hex.sh" file provided to assemble your MIPS program to 
       corresponding hexadecimal instructions.  
       You do NOT want to use QtSPIM for this because QtSPIM sometimes
       assembles with errors. Another assembler you can use is the following:

       https://alanhogan.com/asu/assembler.php

    3. Initialize your i_mem (instruction memory).

    4. Run your simulation for N cycles. Your program may run for an unknown
       number of cycles, so you may want to pick a large number for N so you
       can be sure that all instructions of the program are executed.

    5. Test the values in the register file and memory to make sure they are
       what you expect them to be.

    6. (Optional) Debug. If your code didn't produce the values you thought
       they should, then you may want to call sim.render_trace() on a small
       number of cycles to see what's wrong. You can also inspect the memory
       and register file after every cycle if you wish.

    Some debugging tips:

        - Make sure your assembly program does what you think it does! You
          might want to run it in a simulator somewhere else (SPIM, etc)
          before debugging your PyRTL code.

        - Test incrementally. If your code doesn't work on the first try,
          test each instruction one at a time.

        - Make use of the render_trace() functionality. You can use this to
          print all named wires and registers, which is extremely helpful
          for knowing when values are wrong.

        - Test only a few cycles at a time. This way, you don't have a huge
          500 cycle trace to go through!

    """

    # Start a simulation trace
    sim_trace = pyrtl.SimulationTrace()

    # Initialize the i_mem with your instructions.
    i_mem_init = {}
    with open('i_mem_init.txt', 'r') as fin:
        i = 0
        for line in fin.readlines():
            i_mem_init[i] = int(line, 16)
            i += 1

    sim = pyrtl.Simulation(tracer=sim_trace, memory_value_map={
        i_mem : i_mem_init
    })

    # Run for an arbitrarily large number of cycles.
    for cycle in range(500):
        sim.step({})

    # Use render_trace() to debug if your code doesn't work.
    # sim_trace.render_trace()

    # You can also print out the register file or memory like so if you want to debug:
    # print(sim.inspect_mem(d_mem))
    # print(sim.inspect_mem(rf))

    # Perform some sanity checks to see if your program worked correctly
   #  assert(sim.inspect_mem(d_mem)[0] == 10)
   #  assert(sim.inspect_mem(rf)[8] == 10)    # $v0 = rf[8]
    print('Passed!')