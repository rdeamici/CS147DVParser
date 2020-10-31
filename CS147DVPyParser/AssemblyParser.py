#!/usr/bin/env/python

import sys
import os
import argparse
import re

if hasattr(__builtins__, 'raw_input'):
      input=raw_input
'''
 * a python implementation of
 * @author Jordan's java project
 *
 *	A class that can parse CS147DV instructions into their hexadecimal value
'''

class MnemonicError(KeyError):
    def __init__(self, mnemonic, message="invalid mnemonic: "):
        self.message = message + mnemonic
        super().__init__(self.message)

class RtypeError(IndexError):
    def __init__(self, mnemonic, specifics, message="invalid R-type Instruction: "):
        self.mnemonic = mnemonic
        self.message = message+mnemonic+specifics+'\n'
        super().__init__(self.message)

rtype_mnemonics = ["add", "sub", "mul", "and", "or", "nor", "slt", "sll", "srl","jr"]
itype_mnemonics = ["addi", "muli", "andi", "ori", "lui", "slti", "beq", "bne", "lw", "sw"]
jtype_mnemonics = ["jmp" ,"jal" ,"push" ,"pop"]
numTypes = {
    'bin':2,
    'binary':2,
    'hex': 16,
    'hexadecimal':16,
    'hexidecimal':16,
    'decimal':10,
    'decamal':10
}
functs = {
    "add": "100000",
    "sub": "100010",
    "mul": '101100',
    "and": '100100',
    "or" : '100101',
    "nor": '100111',
    "slt": '101010',
    "sll": "000001",
    "srl": "000010",
    "jr" : "001000",
    
}
opCodes = {
    # r-type
    "add" : "000000",
    "sub" : "000000",
    "mul" : "000000",
    "and" : "000000",
    "or"  : "000000",
    "nor" : "000000",
    "slt" : "000000",
    "sll" : "000000",
    "srl" : "000000",
    "jr"  : "000000",
    # i-type
    "addi": '001000',
    "muli": '011101',
    "andi": '001100',
    "ori" : "001101",
    "lui" : "001111",
    "slti": '001010',
    "beq" : "000100",
    "bne" : "000101",
    "lw"  : "100011",
    "sw"  : "101011",
    # J-type
    "jmp" : "000010",
    "jal" : "000011",
    "push": "011011",
    "pop" : "011100"
}

def x_to_binary(s, base, pad, component):
    try:
        binary = bin(int(s,base))[2:].zfill(pad)
    except ValueError as e:
        assert False, "invalid base of "+str(base)+" for " +component+ " input '" + s + "'"
    
    assert (len(binary) <= pad), s+' = '+binary+' is too big! binary length is ' + str(len(binary)) +', max size is '+str(pad)
    return binary
def get_funct(mnemonic):
    if mnemonic in functs:
        return functs[mnemonic]
    else:
        raise MnemonicError(mnemonic)

def get_base(numType):
    if numType in numTypes:
        return numTypes[numType]
    else:
        raise ValueError("invalid data Type: "+numType+'\noptions are '+", ".join([k for k in numTypes]))

def get_opcode(mnemonic):
    if mnemonic in opCodes:
        return opCodes[mnemonic]
    else:
        raise MnemonicError(mnemonic)

def validate_reg_beginning(reg):
    assert reg.lower().startswith('r'), 'register must start with [rR]. Your input: '+reg

def convert_to_bin(s,padding):
    # vprint('in convert_to_bin\n')
    # print('converting '+s+' into '+str(padding) + ' bit binary string')
    num = ''
    try: # have to do binary first, all binary is also valid decimal
        num = int(s,2)
    except:
        # print(s+' is not a binary num')
        try: # have to do decimal next. All decimal is valid hex
            num = int(s)
        except: # try converting to hexadecimal
            try:
                num = int(s,16)
            except ValueError:
                raise ValueError('could not convert '+s+' to a binary|decimal|hexadecimal number')
    
    # remove first 2 characters from bin(num), which will be '0b'
    # then pad with leading 0s to the size as requested by padding variable
    bin_str = bin(num)[2:].zfill(padding)
    assert len(bin_str) <= padding, s+' = '+bin_str+' is too large. max size for this component is '+str(padding) + ' bits'
    return bin_str

def parse_rtype(mnemonic,rest):
    # will fail if rest is not 3 items long
    numType=''
    base = ''

    if mnemonic == 'jr' and len(rest) != 1:
        raise RtypeError(mnemonic,' only takes one argument')
    elif mnemonic in ('sll','srl') and 3 > len(rest) < 4:
        raise RtypeError(mnemonic, ' requires 3 arguments and an optional data type for shift operations')
    elif mnemonic not in ('jr','sll','srl') and len(rest) != 3:
        raise RtypeError(mnemonic, ' requires exactly 3 arguments')
    
    try:
        rd, rs, rt_or_shamt,numType = rest
    except ValueError:
        try:
            rd,rs,rt_or_shamt = rest
        except ValueError:
            try: # jr instruction only uses rs
                rs = rest[0]
                rd = '00000'
                rt_or_shamt = '00000' 
            except IndexError as e:
                raise RtypeError(mnemonic, ' unknown error')

        registers = [rd,rs] if mnemonic != 'jr' else [rs]
        for r in registers:
            validate_reg_beginning(r)

    if mnemonic in ('sll', 'srl'):
        # print('rt_or_shamt = '+rt_or_shamt)
        assert not rt_or_shamt.startswith('r'), 'shift operations require a shamt, not a register'
        shamt = rt_or_shamt
        if numType: base = get_base(numType)
        rt = '00000'
    else:
        if mnemonic != 'jr':
            validate_reg_beginning(rt_or_shamt)
        rt = rt_or_shamt
        shamt = '00000'
    return rd, rs, rt, shamt, base


def parse_itype(mnemonic, rest):
    numType = ''
    base = ''
    if mnemonic == 'lui' and (len(rest) < 2 or len(rest) > 3):
        assert False, "invalid lui instruction:\n expected 2-3 values, got " +str(len(rest))
    elif mnemonic != 'lui' and (len(rest)< 3 or len(rest) > 4):
        assert False, 'invalid '+mnemonic+' instruction:\n expected 3-4 values, got '+str(len(rest))
    
    try: #check if user gave a number type
        rt, rs, immediate, numType = rest
    except ValueError:
        try:
            rt, rs, immediate = rest
            assert mnemonic != 'lui'
        except Exception:
            try: # lui instruction
                rt, immediate, numType = rest
                rs = '00000'
            except ValueError as e:
                try:
                    rt, immediate = rest
                    rs = '00000'
                except ValueError as E:
                    raise ValueError('invalid string for i-type instruction: '+mnemonic+'.\n'+str(e))
    
    registers = [rt,rs] if mnemonic != 'lui' else [rt]
    for r in registers:
        validate_reg_beginning(r)
    
    if mnemonic == 'lui':
        assert rs == '00000', 'invalid lui instruction'
    imm_err = 'immediate must be a hex|decimal|binary number. Your input: '+immediate
    assert not immediate.lower().startswith('r'), imm_err
    

    if numType: base = get_base(numType)
    return rt,rs,immediate,base

def parse_jtype(mnemonic, rest):
    numType = ''
    base = ''
    if mnemonic in ('push','pop'):
        assert not rest , mnemonic+' instruction takes no arguments'
    else:
        assert rest and len(rest) <= 2, mnemonic+' instruction takes 1 argument and an optional number type'
    
    try:
        address, numType = rest
    except Exception:
        try:
            address  = rest[0]
        except Exception:
            address = '0x00'
            base = 16
    if numType: base = get_base(numType)
    return address, base

def convert_bin_to_hex(bin_s, length):
    try:
        hex_val = hex(int(bin_s,2))[2:].zfill(length)
        assert len(hex_val) <= length, 'hex val is too big'
    except TypeError:
        raise TypeError('could not convert '+bin_s+ ' to hexadecimal')
    else:
        return hex_val
def usage():
    error = 'invalid instruction format'
    error += '\ninstruction must be one of the following types:'
    error += '\nR-type'
    error += '\n\t<mnemonic> <rd>, <rs>, <rt|shamt>'
    error += '\n\t<mnemonic> <rd>,<rs>,<rt|shamt>'
    error += '\nR-type must have 4 arguments'
    error += '\n\nI-type'
    error += '\n\t<mnemonic> <rt>, <rs>, <immediate>'
    error += '\n\t<mnemonic> <rt>,<rs>,<immediate>'
    error += '\nI-type must have 4 arguments'
    error += '\n\nJ-type'
    error += '\n\t<mnemonic> <address>'
    error += '\nJ-type must have 4 arguments'
    error += '\nDo not forget the space after the mnemonic!'
    error += "\n\n registers <rd>, <rs>, <rt> must start with an r followed by 1-2 digits:"
    error += '\n\t (rR)<digit>[<digit>]'
    error += '\n<shamt> must be a binary|hexadecimal|decimal number such that 0 < shamt < ((2^5) -1)'
    error += '\n<immediate> must be a binary|hexadecimal|decimal number such that 0 < immediate < ((2^32) -1)'
    error += '\n<address> must be a binary|hexadecimal|decimal number such that, when converted to a binary string,'
    error += '\nthe number of digits is no more than 26'
    error += '\n\nthe mnemonic must be a member of this set:'
    error += '\n{}'.format(opCodes.keys()) 
    print(error)
    
def parse_instruction(instruction, vprint=sys.stderr):
    assert instruction, "No instruction provided"
    if vprint=='devnull':
        vprint = open(os.devnull,'w')

    # remove trailing comments if applicable
    comment_starters = ['//','#','/*']
    for comment_starter in comment_starters:
        comment_index = instruction.find(comment_starter)
        if comment_index != -1:
            instruction = instruction[:comment_index]
    opcode = ''
    rd = ''
    rs = ''
    rt = ''
    shamt = ''
    funct = ''
    immediate = ''
    address = ''

    components = instruction.lower().replace(',',' ').split()
    mnemonic, rest = components[0], components[1:]
    opcode = get_opcode(mnemonic)
    if mnemonic in rtype_mnemonics:
        vprint.write('\n R-Type detected\n')
        vprint.write(' <mnemonic> <rd> <rs> <rt|shamt> [base]\n\n')
        rd, rs, rt, shamt, base = parse_rtype(mnemonic,rest)
        funct = get_funct(mnemonic)
        vprint.write(' input: '+instruction+'\n')
        vprint.write('  _____________________________________\n')
        vprint.write(' |opcode| rs  | rt  | rd  |shamt| funct|\n')
        vprint.write(' |______|_____|_____|_____|_____|______|\n\n')
        if base: shamt = x_to_binary(shamt,base,5, 'shamt')
        else: shamt = convert_to_bin(shamt,5)

    elif mnemonic in itype_mnemonics:
        vprint.write('\n I-Type detected\n')
        vprint.write(' <mnemonic> <rt> <rs> <imm> [base]\n\n')
        rt, rs, immediate, base = parse_itype(mnemonic,rest)
        vprint.write(' input: '+instruction+'\n')
        vprint.write('  ___________________________________\n')
        vprint.write(' |opcode| rs  | rt  |   immediate    |\n')
        vprint.write(' |______|_____|_____|________________|\n\n')
        if base:
            immediate = x_to_binary(immediate, base, 16, 'immediate')
        else:
            immediate = convert_to_bin(immediate, 16)
    else:
        vprint.write('\n J=Type detected\n')
        vprint.write(' <mnemonic> <address> [base]\n')
        address, base = parse_jtype(mnemonic, rest)
        vprint.write(' input: '+instruction+'\n')
        vprint.write('  _________________________________\n\n')
        vprint.write(' |opcode|          address         |\n')
        vprint.write(' |______|__________________________|\n\n')
        if base: address = x_to_binary(address,base,26, 'address')
        else: address = convert_to_bin(address,26)
    
    if rd: rd = x_to_binary(rd[1:],10,5, 'rd')
    if rt: rt = x_to_binary(rt[1:],10,5, 'rt')
    if rs: rs = x_to_binary(rs[1:],10,5, 'rt')

    to_print = []
    vprint.write(' ')
    for i, s in [[opcode, 'opcode'],[address,'address'],[rs,'rs'],[rt, 'rt'],
                 [immediate, 'imm'],[rd, 'rd'],[shamt,'shamt'],[funct,'funct']]:
        if i:
            vprint.write(s+'\t')
            to_print.append(i)

    vprint.write('\n ')
    vprint.write('\t'.join(to_print)+'\n\n')
    bin_inst = opcode+address+rs+rt+immediate+rd+shamt+funct
    assert len(bin_inst) <= 32, " binary string too long!\n" +bin_inst
    vprint.write(' binary_string\n ')
    for i in range(len(bin_inst)):
        if (i == 0) or (i%4 > 0):
            vprint.write(bin_inst[i])
        else:
            vprint.write(' '+bin_inst[i])
    vprint.write('\n')
    hex_inst = convert_bin_to_hex(bin_inst,8)
    return hex_inst


def interactive_mode(vprint, first_time):
    if first_time:
        vprint.write('\n WELCOME TO CS147DV INTERACTIVE INSTRUCTION PARSER!\n')
        vprint.write(' ENTER IN YOUR INSTRUCTIONS ONE AT A TIME\n')
        vprint.write(' THE RESULT WILL BE PRINTED TO THE SCREEN\n')
        vprint.write(' INPUT SHOULD BE OF THE TYPE:\n')
        vprint.write('   R-Type:  <mnemonic> <rd>,<rs>,<rt|shamt>\n')
        vprint.write('   I-Type:  <mnemonic> <rt>,<rs>, <imm>\n')
        vprint.write('   J-Type:  <mnemonic> <address>\n')
        vprint.write(' OUTPUT WILL BE A 32 BIT HEXADECIMAL NUMBER\n')
        vprint.write(' PRESS ctrl-c TO EXIT AT ANY TIME\n\n')

    instruction = input("\n enter your intruction: ")
    return instruction 

if __name__ == "__main__":
    epilog = 'input: an instruction or set of instructions\n'
    epilog += '       passed in via the command line, as a file, or interactively.\n\n'
    epilog += 'instruction types: R-type: <mnemonic> <rd> <rs> <rt|shamt>\n'
    epilog += '                   I-type: <mnemonic> <rt> <rs> <immediate>\n'
    epilog += '                   J-type: <mnemonic> <address>\n\n'
    epilog += 'output: instruction will be parsed into its component parts.\n'
    epilog += '        By default the:\n'
    epilog += '        \t- instruction type\n'
    epilog += '        \t- bit values of each component\n'
    epilog += '        \t- result in the form of a 32-bit binary string\n'
    epilog += '        will be output to stderr\n\n'
    epilog += '        the resulting hexadecimal string will be output to stdout.\n'
    parser = argparse.ArgumentParser(description="Program to parse CS147DV instructions into hexadecimal",
                            prog = 'CS147DVInstructionParser',
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            epilog = epilog)

    parser.add_argument('instructions',nargs='*', default=[], help = 'CS147DV instructions wrapped in "quotes"')
    parser.add_argument('-f','--file', nargs='?',type=argparse.FileType('r'), help='file of CS147DV instructions, one per line')
    parser.add_argument_group()
    parser.add_argument('-o','--outfile', nargs='?',
                        default=sys.stdout, help='File to save results to. Default setting will write over whatever is already in this file, if it exists')
    parser.add_argument('-a','--append', action='store_true',help='append results to outfile, instead of writing over the outfile.')
    parser.add_argument('-i','--interactive',action='store_true', help='evoke interactive mode.')
    parser.add_argument('-q','--quiet', action='store_true', help='suppress meta-info about each instruction')
    args = parser.parse_args()

    # create a list of instructions to parse that 
    # are passed in from command line and/or file
    instructions = args.instructions
    if args.file:
        with args.file as f:
            instructions += [i.strip() for i in f]
    
    outfile = args.outfile
    if args.append:
        assert outfile != sys.stdout, "outfile must be a real file and not stdout if you want to append to it."
    
    if outfile != sys.stdout: 
        mode = 'a' if args.append else 'w'
        outfile = open(args.outfile, mode)
    
    interactive = args.interactive
    # if they don't provide any input, automatically set interactive to True
    if not interactive:
        interactive = not instructions

    # set file to print meta information to stdout
    #  or to devnull for 'quiet' mode
    if args.quiet:
        vprint = open(os.devnull,'w')
    else:
        vprint = sys.stdout
    
    for i in instructions:
        # hex_result = parse_instruction(i,vprint)
        # print(hex_result)
        try:
            hex_result = parse_instruction(i,vprint)
        except Exception as e:
            sys.stderr.write(str(e))
            sys.stderr.write('\n')
        else:
            vprint.write('\n hexadecimal_string result: \n')
            outfile.write(' '+hex_result+'\n')
    
    first_time=True
    while interactive:
        try:
            i = interactive_mode(vprint, first_time)
            hex_result = parse_instruction(i,vprint)
        except Exception as e:
            sys.stderr.write(' '+str(e))
            sys.stderr.write('\n try again\n\n')
        except KeyboardInterrupt:
            # these could both possibly be sys.stdout, however its
            # safe to close sys.stdout here since immediately exiting
            outfile.close()
            vprint.close()
            sys.exit(0)
        else:
            vprint.write('\n hexadecimal_string result:\n')
            outfile.write(' '+hex_result+'\n\n')
        first_time = False
            
