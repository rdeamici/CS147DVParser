# CS147DVParser

This program was written by Jordan Conragan in the fall semester of 2019 to quickly convert CS147DV instructions to hexadecimal. It may not work as intented if CS147DV has been changed/updated since it was last updated in December of 2019. Pull requests are encouraged. 

# How to use
Though it is called CS147DVParser, it is really a console interperter. You can run it either by creating a program and calling ```AssemblyParser.startConsoleParser()``` or by running the ```ParseTest``` program included in the repo. Once it is running, you can type your commands into the console and it will output the hexedecimal value of that command. You can also type ```help``` into the console to see an example command. To exit the console, type ```quit``` or ```null```.

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
