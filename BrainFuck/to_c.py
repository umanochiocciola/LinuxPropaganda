from sys import argv
import os

if len(argv) < 2:
    print("arguments:\nfile [flags]")
    print("flags:\n\t-c or --compile\t\tautomatically compyle using gcc\n\t--clean\t\t\tremove out.c\n\t-o <name>\t\tname of output file")
    
    exit(1)

flags = []
for i in argv[1:]:
    if i[0] in ['-', '--']:
        flags.append(i.replace('-', ''))

def debug(txt, typ='info'):
    print(f'[{typ}] {txt}')

try:
    with open(argv[1], 'r') as f:
        program = f.read()
except:
    debug("no such file", "error"); exit(1)


if 'cells' in flags:
    try:
        cells = int(flags[flags.index('cells')+1])
    except:
        debug('bad --cells usage', 'error')
else:
    cells = 16
    debug('using default number (16) of cells because not specified with --cells <N>', 'note')



debug('-- Compiler started --')

WDIR = os.path.dirname(os.path.abspath(argv[1]))+'/'
debug(f'working directory: {WDIR}', 'info')

debug('setting up')

debug('initializing')

signature = ''

init = '#include <stdio.h>\n#define CELLS ' + str(cells) + '\nint main() {\nint tape[CELLS] = {0}; int ptr = 0;'

OUTPUT = signature + init

debug('creating references')

repls = {
    '+': 'tape[ptr]++; if (tape[ptr]>255) {tape[ptr] = 0;}',
    '-': 'tape[ptr]--; if (tape[ptr]<0) {tape[ptr] = 255;}',
    '#': 'tape[ptr] = 0;',
    '<': 'ptr++; if (ptr>=CELLS) ptr=0;',
    '>': 'ptr--; if (ptr<0) ptr = CELLS-1;',
    '.': 'printf("%d", tape[ptr]);',
    ':': 'putchar(tape[ptr]);',
    ',': 'scanf("%d", &tape[ptr]);',
    ';': 'tape[ptr] = getchar();',
    '[': 'while (tape[ptr]) {',
    ']': '}'
}

debug('compiling')


for ch in program:
    if not (ch in repls): continue
    OUTPUT += repls[ch] + '\n'

OUTPUT += 'return 0;}'

debug('writing to out.c')

with open('out.c', 'w') as f:
    f.write(OUTPUT)

if 'c' in flags or 'compile' in flags:
    out = 'out'
    if 'o' in flags:
        out = argv[argv.index('-o')+1]
    
    debug(f'compiling to {out}')
    
    if 'v' in flags:
        debug(f"starting gcc '{WDIR}out.c' -o '{WDIR+out}'", 'info')
        os.system(f"gcc '{WDIR}out.c' -o '{WDIR+out}'")
    else:
        os.system(f"gcc '{WDIR}out.c' -o '{WDIR+out}' >.garbage 2>&1")
        os.system('rm .garbage')
    
    if 'clean' in flags:
        os.system(f"rm '{WDIR}out.c'")
    else:
        debug('to automatically remove out.c use --clean', 'note')
else:
    debug('to automatically compile use -c or --compile', 'note')


debug('done!')
