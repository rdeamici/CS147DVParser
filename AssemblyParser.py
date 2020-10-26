import os, sys
import re
import getopt
'''
 * a python implementation of
 * @author Jordan's java project
 *
 *	A class that can parse CS147DV instructions into their hexadecimal value
'''     
rtype_mnemonics = ["add", "sub", "mul", "and", "or", "nor", "slt", "sll", "srl","jr"]
itype_mnemonics = ["addi", "muli", "andi", "ori", "lui", "slti", "beq", "bne", "lw", "sw"]
jtype_mnemonics = ["jmp" ,"jal" ,"push" ,"pop"]
functs = {
    "add": "20",
    "sub": "02",
    "mul": "2c",
    "and": "24",
    "or" : "25",
    "nor": "27",
    "slt": "2a",
    "sll": "01",
    "srl": "02",
    "jr" : "08",
    
}
opCodes = {
    # r-type
    "add" : "00",
    "sub" : "00",
    "mul" : "00",
    "and" : "00",
    "or"  : "00",
    "nor" : "00",
    "slt" : "00",
    "sll" : "00",
    "srl" : "00",
    "jr"  : "00",
    # i-type
    "addi": '08',
    "muli": "1d",
    "andi": "0c",
    "ori" : "0d",
    "lui" : "0f",
    "slti": "0a",
    "beq" : "04",
    "bne" : "05",
    "lw"  : "23",
    "sw"  : "2b",
    # J-type
    "jmp" : "02",
    "jal" : "03",
    "push": "1b",
    "pop" : "1c"
}

def get_funct(mnemonic):
    return functs[mnemonic]

def get_opcode(mnemonic):
    return opCodes[mnemonic]

def validate_reg_beginning(reg):
    assert reg.lower().startswith('r')

def convert_to_bin(s,padding):
    num = ''
    try: # try converting to binary
        num = int(s,2)
    except:
        try: # try converting to decimal
            num = int(s)
        except: # try converting to hexadecimal
            num = int(s,16)
            # dont catch last exception so it fails on any other input
    
    # remove first 2 characters from bin(num), which will be '0b'
    # then pad with leading 0s to the size as requested by padding variable
    return bin(num)[2:].zfill(padding)


def parse_rtype(rest):
    # will fail if rest is not 3 items long
    rd, rs, rt_or_shamt = rest
    for r in [rd,rs]:
        validate_reg_beginning(r)
    rd, rs = rd[1:], rs[1:]

    if rt_or_shamt.lower().startswith('r'):
        rt_or_shamt = rt_or_shamt[1:]

    rd, rs, rt_or_shamt = [convert_to_bin(r,5) for r in [rd,rs,rt_or_shamt]]
    for i in [rd,rs,rt_or_shamt]:
        assert len(i) <= 5

    return rd, rs, rt_or_shamt


def parse_itype(rest):
    rt, rs, immediate = rest
    for r in [rt, rs]:
        validate_reg_beginning(r)
    
    rt, rs = [convert_to_bin(r[1:],5) for r in [rt,rs]]
    immediate = convert_to_bin(immediate,16)
    assert len(rt) <= 5
    assert len(rs) <= 5
    assert len(immediate) <= 16

    return rt,rs,immediate

def parse_jtype(rest):
    return convert_to_bin(rest, 26)


def convert_bin_to_hex(bin_s):
    return hex(int(bin_s,2))[2:].zfill(8)

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
    
def parse_instruction(instruction):
    opcode = ''
    rd = ''
    rs = ''
    rt_or_shamt = ''
    rt = ''
    funct = ''
    immediate = ''
    address = ''
    
    instruction = instruction.replace(',',' ').split()
    mnemonic, rest = instruction[0], instruction[1:]
    [print("mnemonic = "+mnemonic)]
    opcode = convert_to_bin(get_opcode(mnemonic), 6)
    print('opcode = '+opcode)
    print(mnemonic in rtype_mnemonics)
    if mnemonic in rtype_mnemonics:
        print('its a rtype')
        rd, rs, rt_or_shamt = parse_rtype(rest)
        print('rd = '+rd + '\n\n')
        print('rs = '+rs + '\n\n')
        print('rt_or_shamt = '+rt_or_shamt + '\n\n')
    
        funct = convert_to_bin(get_funct(mnemonic),5)
        
    elif mnemonic in itype_mnemonics:
        rt, rs, immediate = parse_itype(rest)
    else:
        address = parse_jtype(rest)    
    
    print('opcode = '+opcode+ '\n\n')
    print('function = '+funct + '\n\n')
    print('rd = '+rd + '\n\n')
    print('rs = '+rs + '\n\n')
    print('rt_or_shamt = '+rt_or_shamt + '\n\n')
    print('address = '+address + '\n\n')
    print('immediate = '+ immediate+ '\n\n')
    for i in [opcode,address,rs,rt,immediate,rd,rt_or_shamt,funct]:
        if not isinstance(i,str):
            print('{} is not a string'.format(i))

    bin_inst = opcode+address+rs+rt+immediate+rd+rt_or_shamt+funct
    print (bin_inst)
    hex_inst = convert_bin_to_hex(bin_inst) 
    print(convert_bin_to_hex(bin_inst))

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        else:
            assert False, 'unhandled option'
    
    not_done = True
    while not_done:
        if args:
            instruction = " ".join(args)
        else:
            try: # python2
                instruction = raw_input("enter your intruction: ")
            except: #python3
                instruction = input('enter your instruction: ')
        
        try:
            parse_instruction(instruction)
            try:
                ans = 'i'
                while ans.lower() not in ('y','n'):
                    ans = raw_input('\nparse another instruction?(y/n) ')
            except:
                while ans.lower() not in ('y','n'):
                    ans = input('\nparse another instruction?(y/n) ')            
            if ans.lower() == 'n':
                not_done = False

        except:
            print('\ntry again (press ctrl c to exit)\n\n')
