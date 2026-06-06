"""
NovaeFloat: Verifica dell'addizione frazionaria nativa Novae.
Test: ∅.4 + ∅.4 = 0 (equivalente a 1.0 decimale).
"""

import ctypes, os

# Compilazione ALU C
codice_c = """
#include <stdlib.h>
#define N_SIMBOLI 21
static const int V_val[N_SIMBOLI] = {
    -10,-9,-8,-7,-6,-5,-4,-3,-2,-1, 0, 1,2,3,4,5,6,7,8,9,10
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
int mul_novae(int a, int b) {
    int vprod = V_val[a] * V_val[b];
    while (vprod > 10) vprod -= 21;
    while (vprod < -10) vprod += 21;
    return V_to_idx(vprod);
}
"""
with open('alu_float.c', 'w') as f: f.write(codice_c)
os.system('gcc -shared -fPIC -O2 -o alu_float.so alu_float.c')

alu = ctypes.CDLL('./alu_float.so')
alu.add_novae.argtypes = [ctypes.c_int, ctypes.c_int]; alu.add_novae.restype = ctypes.c_int
alu.mul_novae.argtypes = [ctypes.c_int, ctypes.c_int]; alu.mul_novae.restype = ctypes.c_int

class NovaeFloat:
    def __init__(self, intero='∅', fraz='0'):
        if intero == '': intero = '∅'
        self.intero = intero
        self.fraz = fraz

    def __repr__(self): return f"NovaeFloat('{self.intero}.{self.fraz}')"
    def __str__(self): return f"{self.intero}.{self.fraz}"

    def __add__(self, other):
        max_len = max(len(self.fraz), len(other.fraz))
        s_fraz = self.fraz.ljust(max_len, '0')
        o_fraz = other.fraz.ljust(max_len, '0')
        riporto = 10
        risultato_fraz = ''
        for i in range(max_len-1, -1, -1):
            a_idx = 11 + int(s_fraz[i])
            b_idx = 11 + int(o_fraz[i])
            somma = alu.add_novae(a_idx, b_idx)
            if riporto != 10: somma = alu.add_novae(somma, riporto)
            cifra = somma - 11
            if cifra < 0:
                cifra += 10
                riporto = 11
            else:
                riporto = 10
            risultato_fraz = str(cifra) + risultato_fraz

        def intero_to_idx(s):
            if s == '∅': return 10
            if len(s) == 1: return 11 + int(s)
            return 11 + int(s[-1]) + 10 * (len(s)-1) + 10*(int(s[0]) if len(s)>1 else 0)

        a_int = intero_to_idx(self.intero)
        b_int = intero_to_idx(other.intero)
        somma_int = alu.add_novae(a_int, b_int)
        if riporto != 10: somma_int = alu.add_novae(somma_int, riporto)

        if somma_int == 10: intero_str = '∅'
        elif somma_int <= 20: intero_str = str(somma_int - 11)
        else:
            decine = (somma_int - 11) // 10
            unita = (somma_int - 11) % 10
            intero_str = str(decine-1) + str(unita)
        return NovaeFloat(intero_str, risultato_fraz)

    def to_dec(self):
        val = 0.0
        if self.intero != '∅':
            for i, c in enumerate(reversed(self.intero)): val += (int(c)+1) * (10**i)
        for j, c in enumerate(self.fraz): val += (int(c)+1) * (10**(-j-1))
        return val

# Test
print("=== TEST NOVAEFLOAT ===")
a = NovaeFloat('∅', '4')
b = NovaeFloat('∅', '4')
c = a + b
print(f"∅.4 + ∅.4 = {c}")
print(f"Valore decimale: {c.to_dec()} (atteso 1.0)")
assert abs(c.to_dec() - 1.0) < 1e-9
print("✅ Test superato: ∅.4 + ∅.4 equivale all'intero 0 Novae.")
