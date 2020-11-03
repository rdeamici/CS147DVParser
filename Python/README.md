# CS147DVPyParser

This program was inspired by Jordan Conragan and written humbly by Rick DeAmicis in the fall semester of 2020 to quickly convert CS147DV instructions to hexadecimal. It may not work as intented if CS147DV has been changed/updated since it was last updated in December of 2019. Pull requests are encouraged.

# Requirements
The program is known to work with Python 3.7+. It should also work with Python2.7, but is untested.

Dependencies include the built-in packages `sys`, `os`, and `argparse`

# Quick set-up
There are two main ways to interact with this program

## 1. Run the program from the command line

The program can be run directly from the command line. It has a fairly robust set of features, and comes in 3 modes.

### interactive mode
  When run with no arguments, the program will enter interactive mode:
      
  ```python
  $ python AssemblyParser.py

  WELCOME TO CS147DV INTERACTIVE INSTRUCTION PARSER!
  ENTER IN YOUR INSTRUCTIONS ONE AT A TIME
  THE RESULT WILL BE PRINTED TO THE SCREEN
  INPUT SHOULD BE OF THE TYPE:
    R-Type:  <mnemonic> <rd>,<rs>,<rt|shamt>
    I-Type:  <mnemonic> <rt>,<rs>, <imm>
    J-Type:  <mnemonic> <address>
  OUTPUT WILL BE A 32 BIT HEXADECIMAL NUMBER
  PRESS ctrl-c TO EXIT AT ANY TIME
  
  enter your intruction: _
  ```
      
  press `ctrl-c` to exit.

### non-interactive mode
There are two non-interactive modes available
1. write instructions directly in the commandline.

   One instruction:
   ```
   $ python AssemblyParser.py "addi r2 r3 5"
   
   I-Type
   <mnemonic> <rt> <rs> <imm> [base]
   input: addi r2 r3 5
    ___________________________________
   |opcode| rs  | rt  |   immediate    |
   |______|_____|_____|________________|
   
   opcode  rs      rt      imm
   001000  00011   00010   0000000000000101
   
   binary_string
   0010 0000 0110 0010 0000 0000 0000 0101
   
   hexadecimal_string result:
   20620005
   
   $ _
   ``` 
  
   More than one instruction:  
  
        $ python AssemblyParser.py "<instruction1>" "<instruction2>"
2. file-read mode. Instructions are read in from a file
    
      $ python AssemblyParser.py -f instructions.txt  

**note:** modes can be mixed and matched. You can even run all three modes at once:

      $ python AssemblyParser.py "addi r1 r2 3" -f instructions.txt -i 

When mixing and matching modes, the instructions always be read in the following order
1. from the command line
2. from a file
3. from interactive mode.

click here for information about proper [instruction formatting](#CS147DV-Instruction-Format)
---

## 2. import the program as a module    
You can import AssemblyParser.py as a module into your own program.

```python
import AssemblyParser
hex_result = AssemblyParser.parse_instruction('addi r2 r3 5')
print(hex_result)
```

the script's default setting is verbose. The call to `parse_instructions()` will send the following output to `stderr` by default:

```
I-Type
<mnemonic> <rt> <rs> <imm> [base]
input: addi r2 r3 5
 ___________________________________
|opcode| rs  | rt  |   immediate    |
|______|_____|_____|________________|

opcode  rs      rt      imm
001000  00011   00010   0000000000000101

binary_string
0010 0000 0110 0010 0000 0000 0000 0101
```

the call to `print(hex_result)` in the above example will print: `20620005`

To suppress the meta-information entirely, redirect that outpufrom `sys.stderr` to 'devnull'. Do this by passing in the strin'devnull' as a second argument to `parse_instructions()`

```python
hex_result = AssemblyParser.parse_instruction('addi r2 r3 5''devnull')
print(hex_result)
```
The above script will only print out the result to stdout: `20620005`

To parse many instructions:

```python
import AssemblyParser

instructions = ['addi r12 r12 12','addi r14 r14 14', 'sll r2 r2 5']
results = [AssemblyParser(i) for i in instructions]
for r in results:
  print(r)
```



# Command Line options
The command line script support numerous options, or flags.

* `-h, --help` : display help information and exit
* `-q, --quiet` : suppress meta-information. This can be used in any mode.
* `-f, --file` : parse instructions from a file
* `-o, --outfile` : provide a file to save results to
* `-a, --append` : append results to outfile, instead of overwriting
* `-i, --interactive` : evoke interactive mode. This can be combined with `-f` flag and instructions added from commandline


## CS147DV Instruction Format

Instructions must be of the form:
* R-Type :
    * \<mnemonic> \<rd> \<rs> \<rt|shamt> [base]
    * \<mnemonic> \<rd>, \<rs>, \<rt|shamt> [base]

    examples: 
    
    * `"add r2 r3 r4"`
    * `"and r2, r3, r4"`
    * `"or r2,r3,r4"`
    * `"sll r2 R3,0x08"`
    * `"srl R2,3, 10 bin"`
    * `"SLL r2 R3 10 decimal"`
    * `"SRL R2 r3 10 hex"`
    * `"jr r15"`

* I-Type :
  * \<mnemonic> \<rt> \<rs> \<immediate> [base]
  * \<mnemonic>,\<rt>,\<rs>,\<immediate> [base]

  examples
 
  * `"addi r2 r2 3"`
  * `"lui, r5,5"`
  * `"beq,r5,r6,0xaf"`
  * `"lw r10 r11 1010,bin"`

* J-Type :
  * \<mnemonic> \<address> [base]
  * \<mnemonic>, \<address> [base]

  examples:
  * `"jmp 0x2b3da9f"`
  * `"push"`

---  

Registers must begin with an `r` or and `R` and must be followed by a decimal. T
`r10` will always map to binary 10d: `001010` and never binary 2d: `00010`

If you choose an R-type instruction that requires a `shamt` instead of a register `rt`, the script will fail if the value passed in begins with an `[rR]`

example:
 ```
enter your intruction: sll r2 r3 r4
shift operations require a shamt, not a register
try again


enter your intruction: sll r2 r3 4

R-Type
<mnemonic> <rd> <rs> <rt|shamt> [base]
input: sll r2 r3 4
 _____________________________________
|opcode| rs  | rt  | rd  |shamt| funct|
|______|_____|_____|_____|_____|______|

opcode  rs      rt      rd      shamt   funct
000000  00011   00000   00010   00100   000001

binary_string
0000 0000 0110 0000 0001 0001 0000 0001

hexadecimal_string result:
00601101
```

---

`[base]` is used to directly specify what your data type is. 

it can be applied to the following fields:
* `<shamt>`
* `<ìmmediate>`
* `<address>`

Options for `[base]`:
* `bin`, `binary`
* `decimal`
* `hex`, `hexadecimal`

**note:** you can also simply prefix a hexadecimal with `0x` to ensure it is converted to hexadecimal


If not specified, the script will attempt to convert `shamt` in the following order:
1. binary
2. decimal
3. hexadecimal

This order is necessary since all binary strings are also valid decimal and hexadecimal strings. 

Similarly, all decimal strings are also valid hexadecimal strings.

example:
* `[base]` not specified: 
  ```
  enter your intruction: sll r2 r3 10
  
  R-Type
  <mnemonic> <rd> <rs> <rt|shamt> [base]
  input: sll r2 r3 10
   _____________________________________
  |opcode| rs  | rt  | rd  |shamt| funct|
  |______|_____|_____|_____|_____|______|
  
  opcode  rs      rt      rd      shamt   funct
  000000  00011   00000   00010   00010   000001
  
  binary_string
  0000 0000 0110 0000 0001 0000 1000 0001
  
  hexadecimal_string result:
  00601081
  ```
* `[base]` set to binary (same as above):
  ```
  enter your intruction: sll r2 r3 10 bin
  
  R-Type
  <mnemonic> <rd> <rs> <rt|shamt> [base]
  input: sll r2 r3 10
   _____________________________________
  |opcode| rs  | rt  | rd  |shamt| funct|
  |______|_____|_____|_____|_____|______|
  
  opcode  rs      rt      rd      shamt   funct
  000000  00011   00000   00010   00010   000001
  
  binary_string
  0000 0000 0110 0000 0001 0000 1000 0001
  
  hexadecimal_string result:
  00601081
  ```
* with `[base]` set to decimal:
  ```
  enter your intruction: sll r2 r3 10 decimal

  R-Type
  <mnemonic> <rd> <rs> <rt|shamt> [base]
  input: sll r2 r3 10 d
   _____________________________________
  |opcode| rs  | rt  | rd  |shamt| funct|
  |______|_____|_____|_____|_____|______|
  
  opcode  rs      rt      rd      shamt   funct
  000000  00011   00000   00010   01010   000001
  
  binary_string
  0000 0000 0110 0000 0001 0010 1000 0001
  
  hexadecimal_string result:
  00601281
  ```
* with `[base]` set to hexadecimal:
  ```
  R-Type
  <mnemonic> <rd> <rs> <rt|shamt> [base]
  input: sll r2 r3 10 hex
   _____________________________________
  |opcode| rs  | rt  | rd  |shamt| funct|
  |______|_____|_____|_____|_____|______|
  
  opcode  rs      rt      rd      shamt   funct
  000000  00011   00000   00010   10000   000001
  
  binary_string
  0000 0000 0110 0000 0001 0100 0000 0001
  
  hexadecimal_string result:
  00601401
  ```
  
Notice how the value of `shamt` and thus the `binary_string` and `hexadecmal_string result` change as the `[base]` is specified.

[CS147DVPyParser website](https://rdeamici.github.io/CS147DVParser)
