#!/usr/bin/python3

import re
num_re = r'\d+'
id_start = r'\w_.$:'
id_re = '[' + id_start + '][' + id_start + r'\d]*'
op_re = r'[=;()@+\-&|!]'
expr = re.compile(num_re + '|' + id_re + '|' + op_re)
comment = re.compile('//.*$')
NUM = 1  # number e.g. '123'
ID = 2  # symbol e.g. 'LOOP'
OP = 3  # = ; ( ) @ + - & | !
ERROR = 4  # error in file

class Parser(object):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    def __init__(self, infile):
        fo = open(infile, 'r')
        self.contents = fo.read()
        self.commands = self.contents.split('\n')
        self.show_commands()
        self.tokens = self.parse(self.commands)
        self.show_tokens()
        self.index = 0

    def command_init(self):
        self.cur_symbol = ''
        self.cmd_type = -1
        self.cur_dest = ''
        self.cur_comp = ''
        self.cur_jump = ''

    # interfaces
    def hasMoreCommand(self):
        return self.index < len(self.tokens)

    def advance(self):
        self.command_init()
        self.cur_command = self.tokens[self.index]
        self.index += 1
        print self.cur_command
        if(self.cur_command[0][1] == '@'):
            self.a_command()
        elif(self.cur_command[0][1] == '('):
            self.l_command()
        else:
            self.c_command()


    def command_type(self):
        return self.cmd_type

    def symbol(self):
        return self.cur_symbol

    def dest(self):
        return self.cur_dest

    def comp(self):
        return self.cur_comp

    def jump(self):
        return self.cur_jump

    def remove_comment(self, command):
        return comment.sub('', command)

    def parse(self, commands):
        return [token for token in [self.parse_line(command) for command in commands] if token != []]

    def parse_line(self, command):
        return [self.tokenize(word) for word in expr.findall(self.remove_comment(command))]

    def tokenize(self, word):
        if self.is_num(word):
            return (NUM, word)
        elif self.is_id(word):
            return (ID, word)
        elif self.is_op(word):
            return (OP, word)
        else:
            return (ERROR, word)

    def is_num(self, word):
        return re.match(num_re, word) != None

    def is_id(self, word):
        return re.match(id_re, word) != None

    def is_op(self, word):
        return re.match(op_re, word) != None

    def show_commands(self):
        print self.commands

    def show_tokens(self):
        print self.tokens

    def a_command(self):
        print ('a cmd')
        self.cmd_type = Parser.A_COMMAND
        self.cur_symbol = self.cur_command[1][1]

    def l_command(self):
        print ('l cmd')
        self.cmd_type = Parser.L_COMMAND
        self.cur_symbol = self.cur_command[1][1]

    def c_command(self):
        print ('c cmd')
        self.cmd_type = Parser.C_COMMAND
        if self.cur_command[1][1] == ';':
            self.cur_comp = self.cur_command[0][1]
            self.cur_jump = self.cur_command[2][1]
        elif self.cur_command[1][1] == '=':
            self.cur_dest = self.cur_command[0][1]
            if len(self.cur_command) == 3:
                self.cur_comp = self.cur_command[2][1]
            elif len(self.cur_command) == 4:
                self.cur_comp = self.cur_command[2][1] + self.cur_command[3][1]
            else:
                self.cur_comp = self.cur_command[2][1] + self.cur_command[3][1] + self.cur_command[4][1]
