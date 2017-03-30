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
        pass


    # api
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
        return {
            "add": self.get_add()
        }.get(arith, "default")

    def get_add(self):
        return "@SP\nM=M-1\n@SP\nA=M\nD=M\n@SP\nA=M-1\nD=M+D\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    def get_pp(self, cmd, obj, index):
        return {
            1: self.get_push(obj, index),
            2: self.get_pop(obj, index)
        }.get(cmd, "default")


    def get_push(self, obj, index):
        push = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        suffix = "A=M+" + index + "\nD=M\n" + push
        return {
            CodeWriter.S_LCL: "@LCL\n" + suffix,
            CodeWriter.S_ARG: "@ARG\n" + suffix,
            CodeWriter.S_THIS: "@THIS\n" + suffix,
            CodeWriter.S_THAT: "@THAT\n" + suffix,
            CodeWriter.S_CONST: "@SP\nA=M\nD=" + index + "\nM=D\n@SP\nM=M+1\n",
            CodeWriter.S_STATIC: "@" + str(16) + suffix,
            CodeWriter.S_TEMP: "@" + str(5) + suffix,
            CodeWriter.S_PTR: self.get_ptr(index)
        }.get(obj, "default")


    def get_pop(self, obj, index):
        pop = "@SP\nA=M\nD=M\n@SP\nM=M-1\n"
        suffix = "A=M+" + index + "\nM=D\n"
        return {
            CodeWriter.S_LCL: pop + "@LCL\n" + suffix,
            CodeWriter.S_ARG: pop + "@ARG\n" + suffix,
            CodeWriter.S_THIS: pop + "@THIS\n" + suffix,
            CodeWriter.S_THAT: pop + "@THAT\n" + suffix,
            CodeWriter.S_STATIC: "@" + str(16) + suffix,
            CodeWriter.S_TEMP: "@" + str(5) + suffix,
            CodeWriter.S_PTR: self.get_ptr(index)
        }.get(obj, "default")

    def get_ptr(self, index):
        return{
            0 : "@THAT",
            1 : "@THIS"
        }.get(index, "default")
