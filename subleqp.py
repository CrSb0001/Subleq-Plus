# Subleq+ master program
# Copyright (C) 2022 McChuck
# Released under GNU General Public License
# See LICENSE for more details.
# Many thanks to Chris Lloyd (github.com/cjrl) and Lawrence Woodman for inspiration and examples.
# Check out         https://techtinkering.com/articles/subleq-a-one-instruction-set-computer/
# And especially    https://techtinkering.com/2009/05/15/improving-the-standard-subleq-oisc-architecture/
# And maybe watch   https://www.youtube.com/watch?v=FvwcRaE9yxc

import sys

import subleqp_parser
import subleqp_vm

try:
    from getch import getch, getche         # Linux
except ImportError:
    try:
        from msvcrt import getch, getche        # Windows
    except ImportError:
        getch, getche = input, input


def write_slc(slc_file, mem):
    pc = 0
    mx_pc = len(mem) - 1
    while pc <= mx_pc:
        a, b, c = mem[pc], 0, 0
        if pc < mx_pc:
            b = mem[pc + 1]
        
        if pc + 1 < mx_pc:
            c = mem[pc + 2]
        
        slc_file.write(f"{a} {b} {c}\n")
        pc += 3


def write_subleqp(src_file, dest_file, /, flags = ["--print-c"]):
    parser = subleqp_parser.SubleqpParser()
    mem = []
    with open(src_file, "r") as sla_file:
        raw = sla_file.read()
        mem = parser.parse(raw)
        sla_file.close()
    
    with open(dest_file, "w") as slc_file:
        write_slc(slc_file, mem)
        slc_file.close()
    
    subleqp_vm.SubleqpVM(flags[0]).execute(mem)

def main(args):
    # Usage: subleqp.py src_file dest_file [--print-c | --print-i]
    flags = []
    if len(args) >= 3:
        if len(args) == 4:
            if args[3].strip() in ["--print-c", "--print-i"]:
                flags += [args[3].strip]
    
    if flags != []:
        write_subleqp(args[1], args[2], flags = flags)
    
    else:
        write_subleqp(args[1], args[2])


if __name__ == '__main__':
    main(sys.argv[1:])
