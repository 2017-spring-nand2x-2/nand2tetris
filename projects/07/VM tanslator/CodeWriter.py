#!/usr/bin/python


class CodeWriter():
    S_LCL = "local"
    S_ARG = "argument"
    S_THIS = "this"
    S_THAT = "that"
    S_PTR = "pointer"
    S_TEMP = "temp"
    S_CONST = "constant"
    S_STATIC = "static"
    S_REG = "reg"

    R_R0 = R_SP = 0
    R_R1 = R_LCL = 1
    R_R2 = R_ARG = 2
    R_R3 = R_THIS = R_PTR = 3
    R_R4 = R_THAT = 4
    R_R5 = R_TEMP = 5
    R_R6 = 6
    R_R7 = 7
    R_R8 = 8
    R_R9 = 9
    R_R10 = 10
    R_R11 = 11
    R_R12 = 12
    R_R13 = R_FRAME = 13
    R_R14 = R_RET = 14
    R_R15 = R_COPY = 15

    def __init__(self):
        self.lable_index = 0

    # interfaces
    def setFileName(self, infile):
        if infile.endswith('.vm'):
            outfile = infile.replace('.vm', '.asm')
        else:
            outfile = infile + '.asm'
        self.fo = open(outfile, 'w')

    def writeArithmetic(self, arith):
        self.fo.write(self.get_arith(arith).replace('SP', '0'))

    def writePushPop(self, cmd, obj, index):
        self.fo.write(self.get_pp(cmd, obj, index).replace('SP', '0'))

    def close(self):
        self.fo.close()

    # implement
    def get_arith(self, arith):
        # translate each command
        return {
            "add": "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M+D\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "sub": "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "neg": "@SP\nM=M-1\nA=M\nD=-M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "eq": self.get_eq("eq"),
            "gt": self.get_eq("gt"),
            "lt": self.get_eq("lt"),
            "and": "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M&D\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "or": "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M|D\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "not": "@SP\nM=M-1\nA=M\nD=!M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
        }.get(arith, "default_arith")

    def get_eq(self, type):
        self.lable_index += 1
        return "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@"\
               + type + str(self.lable_index)\
               + "\nD," + self.get_eq_jump(type) + "\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@end"\
               + str(self.lable_index) + "\n0,JMP\n("\
               + type + str(self.lable_index)\
               + ")\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(end"\
               + str(self.lable_index) + ")\n"

    def get_eq_jump(self, type):
        return{
            "eq" : "JEQ",
            "lt" : "JLT",
            "gt" : "JGT"
        }.get(type, "default")

    def get_pp(self, cmd, obj, index):
        return {
            1: self.get_push(obj, index),
            2: self.get_pop(obj, index)
        }.get(cmd, "default_pp")

    def get_push(self, obj, index):
        # some common asm commands
        push = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        prefix = "@" + index + "\nD=A\n"
        suffix = "A=M+D\nD=M\n" + push
        const_suffix = "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        return {
            CodeWriter.S_LCL: prefix + "@1\n" + suffix,
            CodeWriter.S_ARG: prefix + "@2\n" + suffix,
            CodeWriter.S_THIS: prefix + "@3\n" + suffix,
            CodeWriter.S_THAT: prefix + "@4\n" + suffix,
            CodeWriter.S_CONST: "@SP\nA=M\n@" + index + const_suffix,
            CodeWriter.S_STATIC: prefix + "@16\n" + "A=A+D\nD=M\n" + push,
            CodeWriter.S_TEMP: prefix + "@5\n" + "A=A+D\nD=M\n" + push,
            CodeWriter.S_PTR: self.get_ptr(index) + "\nD=M\n" + push
        }.get(obj, "default_push")

    def get_pop(self, obj, index):
        pop = "@SP\nM=M-1\n@SP\nA=M\nD=M\n@14\nM=D\n"
        prefix = pop + "@" + index + "\nD=A\n"
        suffix = "D=A+D\n@13\nM=D\n@14\nD=M\n@13\nA=M\nM=D\n"
        pointer_suffix = "A=M\n" + suffix
        return {
            CodeWriter.S_LCL: prefix + "@1\n" + pointer_suffix,
            CodeWriter.S_ARG: prefix + "@2\n" + pointer_suffix,
            CodeWriter.S_THIS: prefix + "@3\n" + pointer_suffix,
            CodeWriter.S_THAT: prefix + "@4\n" + pointer_suffix,
            CodeWriter.S_STATIC: prefix + "@16\n" + suffix,
            CodeWriter.S_TEMP: prefix + "@5\n" + suffix,
            CodeWriter.S_PTR: pop + self.get_ptr(index) + "\nM=D\n"
        }.get(obj, "default_pop")

    def get_ptr(self, index):
        return {
            "0" : "@3",
            "1" : "@4"
        }.get(index, "default_ptr")
