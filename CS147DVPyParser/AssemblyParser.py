import sys
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

def x_to_binary(s, base, pad):
    return bin(int(s,base))[2:].zfill(pad)

def get_funct(mnemonic):
    try:
        return functs[mnemonic]
    except KeyError:
        raise KeyError('could not get funct code for ' +mnemonic+': invalid mnemonic')

def get_opcode(mnemonic):
    try:
        return opCodes[mnemonic]
    except KeyError:
        raise KeyError('could not get funct code for ' +mnemonic+': invalid mnemonic')

def validate_reg_beginning(reg):
    assert reg.lower().startswith('r'), 'register must start with [rR]'

def convert_to_bin(s,padding):
    # sys.stderr.write('in convert_to_bin\n')
    # print('converting '+s+' into '+str(padding) + ' bit binary string')
    num = ''
    try: # try converting to binary
        num = int(s,2)
    except:
        # print(s+' is not a binary num')
        try:
            num = int(s)
        except: # try converting to hexadecimal
            try:
                # print(s+'is not a decimal')
                num = int(s,16)
            except ValueError:
                raise ValueError('could not convert '+s+' to a ' + str(padding)+' bit binary string')
    
    # remove first 2 characters from bin(num), which will be '0b'
    # then pad with leading 0s to the size as requested by padding variable
    bin_str = bin(num)[2:].zfill(padding)
    assert len(bin_str) <= padding, s+' = '+bin_str+' is too large. max size for this component is '+str(padding) + ' bits'
    return bin_str

def parse_rtype(mnemonic,rest):
    # will fail if rest is not 3 items long
    try:
        rd, rs, rt_or_shamt = rest
    except ValueError as e:
        raise ValueError('invalid string for an r-type instruction.\n'+str(e))
    for r in [rd,rs]:
        validate_reg_beginning(r)
    rd, rs = rd[1:], rs[1:]
    # print('mnemonic is '+mnemonic)
    if mnemonic in ('sll', 'srl'):
        # print('rt_or_shamt = '+rt_or_shamt)
        assert not rt_or_shamt.startswith('r'), 'shift operations require a shamt, not a register'
        shamt = rt_or_shamt
        rt = '00000'
    else:
        validate_reg_beginning(rt_or_shamt)
        rt = rt_or_shamt[1:]
        shamt = '00000'

    rd, rs = [x_to_binary(r,10,5) for r in [rd,rs]]
    if rt != '00000': rt = x_to_binary(rt,10,5)
    if shamt != '00000': shamt = convert_to_bin(shamt,5)
    return rd, rs, rt, shamt


def parse_itype(rest):
    try:
        rt, rs, immediate = rest
    except ValueError as e:
        raise ValueError('invalid string for an i-type instruction.\n'+str(e))
    for r in [rt, rs]:
        validate_reg_beginning(r)
    rt, rs = [convert_to_bin(r[1:],5) for r in [rt,rs]]
    imm_err = 'immediate must be a hex|decimal|binary number. Your input: '+immediate
    assert not immediate.lower().startswith('r'),imm_err
    immediate = convert_to_bin(immediate,16)
    return rt,rs,immediate

def parse_jtype(rest):
    try:
        address = rest[0]
    except ValueError as e:
        raise ValueError('invalid string for a j-type instruction.\n'+str(e))
    return convert_to_bin(rest, 26)

def convert_bin_to_hex(bin_s):
    try:
        hex_val = hex(int(bin_s,2))[2:].zfill(8)
        assert len(hex_val) <= 8, 'hex val is too big'
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
    
def parse_instruction(instruction):
    opcode = ''
    rd = ''
    rs = ''
    rt_or_shamt = ''
    rt = ''
    shamt = ''
    funct = ''
    immediate = ''
    address = ''
    
    instruction = instruction.replace(',',' ').split()
    mnemonic, rest = instruction[0].lower(), instruction[1:]
    opcode = get_opcode(mnemonic)
    # print('opcode = '+opcode)
    # print(mnemonic in rtype_mnemonics)
    if mnemonic in rtype_mnemonics:
        print('rtype')
        print('<mnemonic> <rd> <rs> <rt|shamt>\n')
        rd, rs, rt, shamt = parse_rtype(mnemonic,rest)
        # print('rd = '+rd + '\n\n')
        # print('rs = '+rs + '\n\n')
        # print('rt_or_shamt = '+rt_or_shamt + '\n\n')
        funct = get_funct(mnemonic)
        # print('funct = '+funct)
    elif mnemonic in itype_mnemonics:
        print('itype')
        print('<mnemonic> <rt> <rs> <imm>\n')
        rt, rs, immediate = parse_itype(rest)
    else:
        # print('parsing jtype...')
        # print(rest)
        print('jtype')
        print('<mnemonic> <address>\n')
        address = parse_jtype(rest[0])
        # print('done')    
    
    # print('opcode = '+opcode+ '\n\n')
    # print('function = '+funct + '\n\n')
    # print('rd = '+rd + '\n\n')
    # print('rs = '+rs + '\n\n')
    # print('rt_or_shamt = '+rt_or_shamt + '\n\n')
    # print('address = '+address + '\n\n')
    # print('immediate = '+ immediate+ '\n\n')
    to_print = []
    for i, s in [[opcode, 'opcode'],[address,'address'],[rs,'rs'],[rt, 'rt'],[immediate, 'imm'],
              [rd, 'rd'],[shamt,'shamt'],[funct,'funct']]:
        if i:
            sys.stderr.write(s+'\t')
            to_print.append(i)
    sys.stderr.write('\n')
    bin_inst = opcode+address+rs+rt+immediate+rd+shamt+funct
    print('\t'.join(to_print))
    print('binary_string')
    for i in range(len(bin_inst)):
        if not i or i%4:
            sys.stderr.write(bin_inst[i])
        else:
            sys.stderr.write(' '+bin_inst[i])
    sys.stderr.write('\n')
    hex_inst = convert_bin_to_hex(bin_inst) 
    return hex_inst

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
                instruction = raw_input("enter your intruction (ctrl-c to exit): ")
            except: #python3
                instruction = input('enter your instruction(ctrl-c to exit): ')
        
        try:
            hex_instructions = parse_instruction(instruction)
        # hex_instructions = parse_instruction(instruction)
        except Exception as e:
            print('\n')
            print(e)
            print('try again (ctrl-c to exit)\n\n')
        else:
            print('hexadecimal_string')
            print(hex_instructions)