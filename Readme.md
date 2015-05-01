# Assembly language for subleq machine.

Subleq machine is a one instruction set computer (OISC). The instruction subleq works as follows.
```
subleq A B C :-  mem[B] = mem[B] - mem[A]
                 if mem[B] <= 0:
                     program_counter = C
```

## Special instructions
1. If B is -1 then mem[A] is printed as a character and program counter is set to C.
2. if program_counter is -1 then execution stops.