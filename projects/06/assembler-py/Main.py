#!/usr/bin/python3

import Parser, Code, SymbolTables, sys

class Main(object):
    def __init__(self):
        self.symbols = SymbolTables.SymbolTables()
        self.symbol_addr = 16
        self.cur_addr = 0

    def round0(self, infile):
        print ("round0")
        parser = Parser.Parser(infile)
        while parser.hasMoreCommand():
            parser.advance()
            cmd = parser.command_type()
            if cmd == parser.A_COMMAND or cmd == parser.C_COMMAND:
                self.cur_addr += 1
            else:
                print ('add ' + parser.symbol() + ' ' + str(self.cur_addr))
                self.symbols.addEntry(parser.symbol(), self.cur_addr)

    def round1(self, infile, outfile):
        print ("round1")
        parser = Parser.Parser(infile)
        code = Code.Code()
        fo = open(outfile, 'w')
        while parser.hasMoreCommand():
            parser.advance()
            cmd = parser.command_type()
            if cmd == parser.A_COMMAND:
                print ("code for a")
                fo.write(code.for_a(self.getAddress(parser.symbol())) + '\n')
            elif cmd == parser.C_COMMAND:
                print ("code for c")
                fo.write(code.for_c(parser.dest(), parser.comp(), parser.jump()) + '\n')
            else:
                pass
        fo.close()

    def getAddress(self, symbol):
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbols.contains(symbol):
                self.symbols.addEntry(symbol, self.symbol_addr)
                self.symbol_addr += 1
            return self.symbols.getAddress(symbol)

    def run(self, infile):
        self.round0(infile)
        self.round1(infile, self.outfile(infile))

    def outfile(self, infile):
        if infile.endswith('.asm'):
            return infile.replace( '.asm', '.hack' )
        else:
            return infile + '.hack'

if __name__ == "__main__":
    infile = sys.argv[1]
#    infile = 'Rect.asm'
    sess = Main()
    sess.run(infile)

