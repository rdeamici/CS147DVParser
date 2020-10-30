# CS147DVPyParser

This program was inspired greatly by Jordan Conragan and written humbly by Rick DeAmicis in the fall semester of 2020 to quickly convert CS147DV instructions to hexadecimal. It may not work as intented if CS147DV has been changed/updated since it was last updated in December of 2019. Pull requests are encouraged. 

# How to use
there are two ways to interact with this program.
1. by importing it into your own script.
    ```
    >>> import AssemblyParser
    >>> hex_result = AssemblyParser.parse_instruction('addi r2 r3 5')

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
    >>> print(hex_result)
    20620005
    ```
    If you don't want to see all the meta-information, send it to 'devnull'
    Do this by passing in the string 'devnull' as a second argument to parse_instructions()
    ```
    >>> hex_result = AssemblyParser.parse_instruction('addi r2 r3 5', 'devnull')
    >>> print(hex_result)
    20620005
    ```

2. by using it as a command line utility. The command line utility has many options.
    to run it in basic interactive mode:
    ```python
    $ python AssemblyParser.py
    ```
    which will output the following:
    ```
    WELCOME TO CS147DV INTERACTIVE INSTRUCTION PARSER!
    ENTER IN YOUR INSTRUCTIONS ONE AT A TIME
    THE RESULT WILL BE PRINTED TO THE SCREEN
    INPUT SHOULD BE OF THE TYPE:
      R-Type:  <mnemonic> <rd>,<rs>,<rt|shamt>
      I-Type:  <mnemonic> <rt>,<rs>, <imm>
      J-Type:  <mnemonic> <address>
    OUTPUT WILL BE A 32 BIT HEXADECIMAL NUMBER
    PRESS ctrl-c TO EXIT AT ANY TIME
    
    
    enter your intruction:
    ```
You can run it either by creating a program and calling ```AssemblyParser.startConsoleParser()``` or by running the ```ParseTest``` program included in the repo. Once it is running, you can type your commands into the console and it will output the hexedecimal value of that command. You can also type ```help``` into the console to see an example command. To exit the console, type ```quit``` or ```null```.

## CS147DV Instruction Format
This program was written fast and so there are two formatting rules in addition to the rules of CS147DV that need to be followed.
- All integers must be in decimal form.
- There must be a space between the each mnemonic, register (regardless if it is also seperated by a comma), and immediate value.

Examples of good instructions:
- ```addi r1 r2 16```
- ```or r0, r3, r2```
- ```jmp 15```

Examples of bad instructions:
- ```addi r1 r2 0x10```
- ```or r0,r3,r2```
- ```jmp 0x15```
