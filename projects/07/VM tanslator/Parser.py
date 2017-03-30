#!/usr/bin/python3

import re
num_re = r'\d+'
id_start = r'\w_.$:'
id_re = '[' + id_start + '][' + id_start + r'\d]*'
expr = re.compile(num_re + '|' + id_re)
comment = re.compile('//.*$')
NUM = 1  # number e.g. '123'
ID = 2  # symbol e.g. 'LOOP'

class Parser(object):
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABLE = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8
    C_ERROR = 9
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
        self.cur_type = -1
        self.cur_arg1 = ''
        self.cur_arg2 = -1

    # interfaces
    def hasMoreCommands(self):
        return self.index < len(self.tokens)

    def advance(self):
        self.command_init()
        self.cur_command = self.tokens[self.index]
        self.index += 1
        print self.cur_command
        self.cur_type = self.get_type(self.cur_command[0][1])
        print self.cur_type
        if len(self.cur_command) >= 2:
            self.cur_arg1 = self.get_arg1_1(self.cur_command[0][1])
            if len(self.cur_command) >= 3:
                self.cur_arg2 = self.cur_command[2][1]
        else:
            self.cur_arg1 = self.get_arg1(self.cur_command[0][1])
        print self.cur_arg1

    def command_type(self):
        return self.cur_type

    def arg1(self):
        return self.cur_arg1

    def arg2(self):
        return self.cur_arg2

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
        else:
            pass

    def is_num(self, word):
        return re.match(num_re, word) != None

    def is_id(self, word):
        return re.match(id_re, word) != None

    def show_commands(self):
        print self.commands

    def show_tokens(self):
        print self.tokens

    def get_type(self, str):
        return{
            "add" : Parser.C_ARITHMETIC,
            "sub" : Parser.C_ARITHMETIC,
            "neg" : Parser.C_ARITHMETIC,
            "eq" : Parser.C_ARITHMETIC,
            "gt" : Parser.C_ARITHMETIC,
            "lt" : Parser.C_ARITHMETIC,
            "and" : Parser.C_ARITHMETIC,
            "or" : Parser.C_ARITHMETIC,
            "not" : Parser.C_ARITHMETIC,
            "push" : Parser.C_PUSH,
            "pop" : Parser.C_POP,
            "label" : Parser.C_LABLE,
            "goto" : Parser.C_GOTO,
            "if-goto" : Parser.C_IF,
            "function" : Parser.C_FUNCTION,
            "call" : Parser.C_CALL,
            "return" : Parser.C_RETURN,
        }.get(str, Parser.C_ERROR)

    def get_arg1(self, str):
        return{
            "add" : "add",
            "sub" : "sub",
            "neg" : "neg",
            "eq" : "eq" ,
            "gt" : "gt" ,
            "lt" : "lt" ,
            "and" : "and",
            "or" : "or" ,
            "not" : "not",
        }.get(str, "error")

    def get_arg1_1(self, str):
        return{
            "push" : self.cur_command[1][1],
            "pop" : self.cur_command[1][1],
            "label" : self.cur_command[1][1],
            "goto" : self.cur_command[1][1],
            "if-goto" : self.cur_command[1][1],
            "function" : self.cur_command[1][1],
            "call" : self.cur_command[1][1],
        }.get(str, "error")
