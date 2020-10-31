# CS147DVPyParser

This program was inspired by Jordan Conragan and written humbly by Rick DeAmicis in the fall semester of 2020 to quickly convert CS147DV instructions to hexadecimal. It may not work as intented if CS147DV has been changed/updated since it was last updated in December of 2019. Pull requests are encouraged.

## Requirements
The program is known to work with Python 3.7+. It should also work with Python2.7, but is untested.

Dependencies include the built-in packages `sys`, `os`, and `argparse`

## Quick set-up
The main function that does all the work is `AssemblyParser.parse_instructions()`. There are two main ways to interact with this method.
        
1. by importing it into your own script.
    ```python
    import AssemblyParser
    hex_result = AssemblyParser.parse_instruction('addi r2 r3 5')
    print(hex_result)
    ```
    the script's default setting is verbose. The call to `parse_instructions()` will send the following output to `stderr` by default
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
    the call to `print(hex_result)` in the above example will print:
    ```
    20620005
    ```
    To suppress the meta-information entirely, redirect that output from `sys.stderr` to 'devnull'. Do this by passing in the string 'devnull' as a second argument to `parse_instructions()`
    ```python
    hex_result = AssemblyParser.parse_instruction('addi r2 r3 5', 'devnull')
    print(hex_result)
    ```
    The above script will only print out the result to stdout:
        
        20620005
    

2. The script also works as a command line utility:
    
    * to type and parse instructions interactively:
      
      ```python
      $ python AssemblyParser.py
      ```
      
      With no arguments, the script will enter interactive mode:
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
  
      enter your intruction: _
      ```
      
      press `ctrl-c` at any time to exit.

    * You can also parse one or more instructions by passing them directly in on the command line.
      
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
    * Finally, you can pass in an entire file of instructions, one instruction per line in the file:

            $ python AssemblyParser.py -f instructions.txt  
      
      
## Command Line options
The command line script support numerous options, or flags.

      suppress meta-information with the `-q` flag. This can be used in any mode.

    interactive :
    ```
    $ python AssemblyParser.py -q

    enter in your instruction: addi r2 r3 5
    20620005


    enter in your instruction: _
    ```
    non-interactive :
    ```
    $ python AssemblyParser.py "addi r2 r3 5" -q
    20620005

    $ _
    ```


## CS147DV Instruction Format

Instructions must be of the form:
* R-Type
    * \<mnemonic> \<rd> \<rs> \<rt|shamt> [base]
    * \<mnemonic> \<rd>, \<rs>, \<rt|shamt> [base]
        
        ex: 
        * "add r2 r3 r4"
        * "add r2, r3, r4"
        * "add r2,r3,r4"
        
        Registers must begin with an `r` or and `R` and must be followed by a decimal. Thus `r10` will always map to binary 10d: `001010` and never binary 2d: `00010`

        If you choose an R-type instruction that requires a `shamt` instead of a register `rt`, the script will fail if the value passed in begins with an `[rR]`

        ex:
        * ```
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
        `[base]` is used to directly specify what your data type is for `shamt`.
        
        Acceptable data types are: `binary`, `decimal`, `hexadecimal`

        If not specified, the script will attempt to detect the `shamt` first as a binary, then as a decimal, and finally as a hexadecimal.

        example:
        * with no `[base]` specified: 
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
        * with `[base]` set to binary (same as above):
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

        * with `[base]` set to decimal:
          ```
          enter your intruction: sll r2 r3 10 d

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
          input: sll r2 r3 10 h
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

        This example illustrates the danger of not specifying your `[base]` data type. If you type in a valid binary string like `10` without specifying the `[base]`, it will be evaluated as binary.

        Another gotcha: `d` is a valid character in hexadecimal. Thus, if you pass in `"sll r2 r3 10d"` the `10d` will be evaluated as a hexadecimal number.
        ```
        enter your intruction: sll r2 r3 10d

        R-Type
        <mnemonic> <rd> <rs> <rt|shamt> [base]
        input: sll r2 r3 10d
         _____________________________________
        |opcode| rs  | rt  | rd  |shamt| funct|
        |______|_____|_____|_____|_____|______|

        10d = 100001101 is too large. max size for this component is 5 bits
        try again
        ```
        Luckily `10d` is too large to fit in 5 bits, so an error will occur.

        It is best to use the long form of `[base]`:
        * binary: 
            * long forms: `bin`, `binary`
            * short form: `b`
        * decimal:
            * long forms: `dec`, `decimal`, `decamal`
            * short form: `d`
        * hexadecimal:
            * long forms: `hex`,`hexadecimal`, `hexidecimal`
            * short form: `h`
