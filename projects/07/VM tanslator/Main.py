#!/usr/bin/python3

import Parser, CodeWriter

class Main(object):
    def __init__(self):
        parser = Parser.Parser(infile)
        codewriter = CodeWriter.CodeWriter()
        codewriter.setFileName(infile)
        while parser.hasMoreCommands():
            parser.advance()
            cmd = parser.command_type()
            if cmd == parser.C_ARITHMETIC:
                codewriter.writeArithmetic(parser.arg1())
            elif cmd == parser.C_PUSH or cmd == parser.C_POP:
                codewriter.writePushPop(parser.command_type(), parser.arg1(), parser.arg2())
            else:
                print ("other")
        codewriter.close()

if __name__ == "__main__":
    infile = "../MemoryAccess/PointerTest/PointerTest.vm"
#    infile = "../StackArithmetic/StackTest/StackTest.vm"
    sess = Main()
