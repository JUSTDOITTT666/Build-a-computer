import fileinput
import sys

comp_dic = {'0': {"0": '101010',
                  '1': '111111',
                  '-1': '111010',
                  'D': '001100',
                  'A': '110000',
                  '!D': '001101',
                  '!A': '110001',
                  '-D': '001111',
                  '-A': '110011',
                  'D+1': '011111',
                  'A+1': '110111',
                  'D-1': '001110',
                  'A-1': '110010',
                  'D+A': '000010',
                  'D-A': '010011',
                  'A-D': '000111',
                  'D&A': '000000',
                  'D|A': '010101'},
            '1': {'M': '110000',
                  '!M': '110001',
                  '-M': '110011',
                  'M+1': '110111',
                  'M-1': '110010',
                  'D+M': '000010',
                  'D-M': '010011',
                  'M-D': '000111',
                  'D&M': '000000',
                  'D|M': '010101'}}

dest_dic = {'null': '000',
            'M': '001',
            'D': '010',
            'MD': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'AMD': '111'}

jump_dic = {'null': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'}

pre_var_dic = {'R0': 0,
               'R1': 1,
               'R2': 2,
               'R3': 3,
               'R4': 4,
               'R5': 5,
               'R6': 6,
               'R7': 7,
               'R8': 8,
               'R9': 9,
               'R10': 10,
               'R11': 11,
               'R12': 12,
               'R13': 13,
               'R14': 14,
               'R15': 15,
               'SCREEN': 16384,
               'KBD': 24576,
               'SP': 0,
               'LCL': 1,
               'ARG': 2,
               'THIS': 3,
               'THAT': 4}

var_dic = {}
label_dic = {}

"""
Delete  whitespace and some line like:
    //......
    ......//
"""
def delete_whitespace(filename):
    f = open(filename, "r")
    f1 = open(out_filename, "w")

    for line in f:
        if line.find("//") != -1:
            line = line[0:line.find("//")]
        if line != "\n" and line != '':
            f1.write(line.strip() + "\n")

    f.close()
    f1.close()


"""
Create a filename, for example:
    if out_filename = get_outfilename("test.asm")
    the out_filename is "test.hack"
"""
def get_outfilename(filename):
    return filename[0:filename.find('.')] + ".hack"


"""
Translate A-instructions to binary, for example:
    @21 ==> 0000 0000 0001 0101
"""
def translat_a_ins(filename):
    for line in fileinput.input(filename, inplace=1):
        if line[0:1] == "@":
            i = int(line[1:])
            i = format(i, 'b').zfill(16)
            line = line.replace(line, str(i) + "\n")
        sys.stdout.write(line)


"""
Translate C-instructions to binary, for example:
    MD=D+1 ==> 111 0 011111 011 000
"""
def translat_c_ins(filename):
    for line in fileinput.input(filename, inplace=1):
        line = line.strip('\n')
        out = '111'
        # deal with dest = comp
        if line.find("=") != -1:
            x = line.split("=")
            if x[1] in comp_dic['0']:
                out = out + '0' + comp_dic['0'][x[1]] + dest_dic[x[0]] + '000'
            else:
                out = out + '1' + comp_dic['1'][x[1]] + dest_dic[x[0]] + '000'
        # deal with comp;jump
        elif line.find(";") != -1:
            x = line.split(";")
            if x[0] in comp_dic['0']:
                out = out + '0' + comp_dic['0'][x[0]] + '000' + jump_dic[x[1]]
            else:
                out = out + '1' + comp_dic['0'][x[0]] + '000' + jump_dic[x[1]]
        else:
            out = line

        line = line.replace(line, out + "\n")
        sys.stdout.write(line)


"""
Handing pre-defined symbols:
    @R10  ===>   @10
    @i   ===>  @16(if i is the first variable)
"""
def hand_symbols(filename):
    i = 0
    create_label_dic(out_filename)

    for line in fileinput.input(filename, inplace=1):
        if line[0:1] == '(':
            continue
        elif line[0:1] == "@":
            symbol = line[1:].strip('\n')
            if is_number(symbol):
                line = line
            elif symbol in pre_var_dic:
                line = line.replace(line[1:], str(pre_var_dic[symbol]) + '\n')
            elif symbol in label_dic:
                line = line.replace(line[1:], str(label_dic[symbol]) + '\n')
            elif symbol in var_dic:
                line = line.replace(line[1:], str(var_dic[symbol]) + '\n')
            # create var_dic
            else:
                i += 1
                var_dic[symbol] = 15 + i
                line = line.replace(line[1:], str(var_dic[symbol]) + '\n')

        sys.stdout.write(line)


def create_label_dic(filename):
    i = -1

    f = open(filename, 'r')
    for line in f:
        i += 1
        if line[0:1] == '(':
            symbol = line[1:line.find(')')]
            i -= 1
            label_dic[symbol] = i + 1
    f.close()


"""
Test s is number or not:
    i ===> false
    10 ===> true
"""
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass


out_filename = get_outfilename("Pong.asm")
delete_whitespace("Pong.asm")
hand_symbols(out_filename)
translat_a_ins(out_filename)
translat_c_ins(out_filename)
