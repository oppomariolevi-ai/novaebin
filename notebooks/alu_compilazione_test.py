"""
Compilazione e test dell'ALU Novae in C.
Dimostra il Capitolo 6 del Principia Novae Mathematicae v1.3.
"""

# Scrittura e compilazione dell'ALU
codice_c = '''
#include <stdio.h>
#include <stdlib.h>

#define N_SIMBOLI 21

static const int V_val[N_SIMBOLI] = {
    -10,-9,-8,-7,-6,-5,-4,-3,-2,-1,
    0,
    1,2,3,4,5,6,7,8,9,10
};

int V_to_idx(int v) {
    for (int i = 0; i < N_SIMBOLI; i++) if (V_val[i] == v) return i;
    return -1;
}

int add_novae(int a, int b) {
    int vsum = V_val[a] + V_val[b];
    while (vsum > 10) vsum -= 21;
    while (vsum < -10) vsum += 21;
    return V_to_idx(vsum);
}

int sub_novae(int a, int b) {
    int vb = V_val[b];
    int neg_b = V_to_idx(-vb);
    return add_novae(a, neg_b);
}

int mul_novae(int a, int b) {
    int vprod = V_val[a] * V_val[b];
    while (vprod > 10) vprod -= 21;
    while (vprod < -10) vprod += 21;
    return V_to_idx(vprod);
}

int div_novae(int a, int b) {
    if (b == 10) return -1;
    for (int c = 0; c < N_SIMBOLI; c++) {
        if (mul_novae(c, b) == a) return c;
    }
    return -1;
}
'''

with open('alu_novae.c', 'w') as f:
    f.write(codice_c)

import subprocess
subprocess.run(['gcc', '-shared', '-fPIC', '-O2', '-o', 'alu_novae.so', 'alu_novae.c'])

import ctypes

alu = ctypes.CDLL('./alu_novae.so')
alu.add_novae.argtypes = [ctypes.c_int, ctypes.c_int]
alu.add_novae.restype = ctypes.c_int
alu.mul_novae.argtypes = [ctypes.c_int, ctypes.c_int]
alu.mul_novae.restype = ctypes.c_int
alu.sub_novae.argtypes = [ctypes.c_int, ctypes.c_int]
alu.sub_novae.restype = ctypes.c_int

simboli = ['-9','-8','-7','-6','-5','-4','-3','-2','-1','-0',
           '∅',
           '+0','+1','+2','+3','+4','+5','+6','+7','+8','+9']
sym_to_idx = {s: i for i, s in enumerate(simboli)}

def test_op(a_str, b_str, op, expected):
    ia, ib = sym_to_idx[a_str], sym_to_idx[b_str]
    res = op(ia, ib)
    risultato = simboli[res]
    ok = "OK" if risultato == expected else f"ERRORE (atteso {expected})"
    print(f"{a_str} op {b_str} = {risultato} {ok}")

print("=== TEST ADDIZIONE ===")
test_op('+0', '+1', alu.add_novae, '+2')
test_op('+1', '+1', alu.add_novae, '+3')
test_op('-1', '+1', alu.add_novae, '∅')

print("\n=== TEST MOLTIPLICAZIONE ===")
test_op('+0', '+1', alu.mul_novae, '+1')
test_op('+1', '+1', alu.mul_novae, '+3')

print("\n=== TEST SOTTRAZIONE ===")
test_op('+2', '+1', alu.sub_novae, '+0')

print("\nTutti i test completati.")
