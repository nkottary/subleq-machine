import sys

EXIT_FAILURE_CMD = 2
EXIT_FAILURE = 1
EXIT_SUCCESS = 0

if len(sys.argv) != 2:
    print("Usage: python main.py <sl file name>")
    exit(EXIT_FAILURE_CMD)

try:    
    sl_file = open(sys.argv[1], "r")
except IOError as err:
    print("Error occured while opening file %s" % sys.argv[1])
    print(err)
    exit(EXIT_FAILURE)

line_lst = sl_file.readlines()

token_lst = []
for line_num, line in enumerate(line_lst):
    line = line.strip().split('#')[0]  # Ignore comments
    if line:
        tok_lst = line.split()
        token_lst.extend(zip(tok_lst, [line_num + 1]*len(tok_lst)))

# Build symbol table
sym_table = {}
for tok_num, tok_tup in enumerate(token_lst):
    token, line_num = tok_tup
    if ':' in token:
        sub_toks = token.split(':')
        if len(sub_toks) != 2 or not sub_toks[0] or not sub_toks[1] \
           or not sub_toks[0].isalpha():
            print("Declaration error in line number %d: %s" % \
                  (line_num, token))
            exit(EXIT_FAILURE)
        else:
            try:
                _ = int(sub_toks[1])
            except ValueError as ve:
                print("Declaration error in line number %d: %s" % \
                      (line_num, token))
                exit(EXIT_FAILURE)

            token_lst[tok_num] = sub_toks[1], line_num
            sym_table[sub_toks[0]] = tok_num

# Resolve symbols
for tok_num, tok_tup in enumerate(token_lst):
    token, line_num = tok_tup
    if token[0].isalpha():
        tok_add = sym_table.get(token)
        if not tok_add:
            print("Symbol %s not found, in line number %d" % (token, line_num))
            exit(EXIT_FAILURE)
        token_lst[tok_num] = tok_add, line_num
    else:
        try:
            token_lst[tok_num] = int(token), line_num
        except ValueError as ve:
            print("Expected integer in line number %d got %s instead." \
                  % (line_num, token))
            exit(EXIT_FAILURE)

pc = 0
while 1:
    if pc == -1:
        exit(EXIT_SUCCESS)
    if pc < -1 or pc >= len(token_lst) - 2:
        print("Erroneous program counter occured!")
        exit(EXIT_FAILURE)
        
    a, lna = token_lst[pc]
    b, lnb = token_lst[pc + 1]
    c, lnc = token_lst[pc + 2]

    if lna != lnb or lna != lnc:
        print("Invalid instruction in line number %d" % lna)
        exit(EXIT_FAILURE)

    if b == -1:
        if a < 0 or a > len(token_lst):
            print("Attempt to output out of bounds memory location %d in line"
                  " number %d" % (a, line_num))
            exit(EXIT_FAILURE)

        try:
            chr_val = chr(token_lst[a][0])
        except ValueError as ve:
            print("Attempt to output non-ascii character in line number %d"
                  ", non-ascii character in line number %d"
                  % (line_num, token_lst[a][1]))
            exit(EXIT_FAILURE)

        print(chr_val)
        pc = c
        continue

    b = b - a
    token_lst[pc + 1] = b, lnb

    if b <= 0:
        pc = c
    else:
        pc += 3
