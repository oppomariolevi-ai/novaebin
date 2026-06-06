"""
Libreria Novae - Sistema di Numerazione Non-Decimato
----------------------------------------------------
Fornisce i tipi `NovaeID`, `NovaeInt` e `NovaeFloat` per eliminare
l'ambiguità dello zero e operare nativamente in Novae.
"""

import os
import ctypes
import platform

# ============================================
# RILEVAMENTO E CARICAMENTO ALU C (OPZIONALE)
# ============================================
_alu_c = None

def _carica_alu_c():
    """Tenta di compilare e caricare l'ALU C. Restituisce l'oggetto ALU o None."""
    global _alu_c
    if _alu_c is not None:
        return _alu_c

    if os.path.exists('./alu_novae.so'):
        try:
            _alu_c = ctypes.CDLL('./alu_novae.so')
            _alu_c.add_novae.argtypes = [ctypes.c_int, ctypes.c_int]
            _alu_c.add_novae.restype = ctypes.c_int
            _alu_c.mul_novae.argtypes = [ctypes.c_int, ctypes.c_int]
            _alu_c.mul_novae.restype = ctypes.c_int
            return _alu_c
        except Exception:
            pass

    if platform.system() == 'Linux':
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
        with open('alu_novae.c', 'w') as f:
            f.write(codice_c)
        if os.system('gcc -shared -fPIC -O2 -o alu_novae.so alu_novae.c') == 0:
            try:
                _alu_c = ctypes.CDLL('./alu_novae.so')
                _alu_c.add_novae.argtypes = [ctypes.c_int, ctypes.c_int]
                _alu_c.add_novae.restype = ctypes.c_int
                _alu_c.mul_novae.argtypes = [ctypes.c_int, ctypes.c_int]
                _alu_c.mul_novae.restype = ctypes.c_int
                return _alu_c
            except Exception:
                pass
    return None

# ============================================
# TAVOLA DI ADDIZIONE PYTHON (FALLBACK)
# ============================================
_TABELLA_ADD = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [2, 3, 4, 5, 6, 7, 8, 9, 0, 1],
    [3, 4, 5, 6, 7, 8, 9, 0, 1, 2],
    [4, 5, 6, 7, 8, 9, 0, 1, 2, 3],
    [5, 6, 7, 8, 9, 0, 1, 2, 3, 4],
    [6, 7, 8, 9, 0, 1, 2, 3, 4, 5],
    [7, 8, 9, 0, 1, 2, 3, 4, 5, 6],
    [8, 9, 0, 1, 2, 3, 4, 5, 6, 7],
    [9, 0, 1, 2, 3, 4, 5, 6, 7, 8],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
]

def _add_novae_py(a: int, b: int) -> int:
    return _TABELLA_ADD[a][b]

def _add_novae(a: int, b: int) -> int:
    alu = _carica_alu_c()
    if alu:
        return alu.add_novae(a, b)
    return _add_novae_py(a, b)

# ============================================
# CLASSI
# ============================================

class NullPointerError(Exception):
    pass

class NovaeID:
    VUOTO = None

    def __init__(self, value: int):
        if value < 0:
            raise ValueError("NovaeID deve essere >= 0. Usa NovaeID.VUOTO per il vuoto.")
        self._value = value

    @property
    def value(self) -> int:
        if self.is_vuoto():
            raise NullPointerError("Impossibile dereferenziare un NovaeID vuoto.")
        return self._value

    def is_vuoto(self) -> bool:
        return False

    def __eq__(self, other):
        if isinstance(other, NovaeID):
            if self.is_vuoto() or other.is_vuoto():
                return self.is_vuoto() and other.is_vuoto()
            return self._value == other._value
        return NotImplemented

    def __hash__(self):
        return hash(self._value) if not self.is_vuoto() else 0

    def __repr__(self):
        return "∅" if self.is_vuoto() else f"NovaeID({self._value})"

    def __str__(self):
        return str(self._value) if not self.is_vuoto() else "∅"

    def __bool__(self):
        return not self.is_vuoto()

class _VuotoNovaeID(NovaeID):
    def __init__(self): pass
    def is_vuoto(self): return True
    def __repr__(self): return "∅"
    def __str__(self): return "∅"
    def __bool__(self): return False

NovaeID.VUOTO = _VuotoNovaeID()

def _successor(sym: str) -> str:
    if sym == '9':
        return '00'
    last = sym[-1]
    if last != '9':
        return sym[:-1] + str(int(last) + 1)
    prefix = sym[:-1]
    if prefix == '':
        return '00'
    return _successor(prefix) + '0'

class NovaeInt:
    def __init__(self, symbol: str):
        if not symbol or not all(c in '0123456789' for c in symbol):
            raise ValueError("Simbolo Novae non valido. Usa cifre 0-9.")
        self.symbol = symbol

    def __add__(self, other: 'NovaeInt') -> 'NovaeInt':
        result = self.symbol
        steps = other.to_int()
        for _ in range(steps):
            result = _successor(result)
        return NovaeInt(result)

    def __mul__(self, other: 'NovaeInt') -> 'NovaeInt':
        if other.symbol == '0':
            return NovaeInt(self.symbol)
        val_a = self.to_int()
        val_b = other.to_int()
        product_val = val_a * val_b
        return NovaeInt.from_int(product_val)

    def __sub__(self, other: 'NovaeInt') -> 'NovaeInt':
        val_a = self.to_int()
        val_b = other.to_int()
        if val_b > val_a:
            raise ValueError("Risultato negativo non supportato.")
        diff_val = val_a - val_b
        return NovaeInt.from_int(diff_val)

    def __truediv__(self, other: 'NovaeInt') -> 'NovaeInt':
        if other.symbol == '0':
            return NovaeInt(self.symbol)
        val_a = self.to_int()
        val_b = other.to_int()
        if val_a % val_b != 0:
            raise ValueError("Divisione non esatta.")
        div_val = val_a // val_b
        return NovaeInt.from_int(div_val)

    def to_int(self) -> int:
        val = 0
        for c in self.symbol:
            val = val * 10 + (int(c) + 1)
        return val

    @staticmethod
    def from_int(n: int) -> 'NovaeInt':
        if n <= 0:
            raise ValueError("Intero deve essere >= 1")
        n -= 1
        if n == 0:
            return NovaeInt('0')
        digits = []
        while n >= 0:
            digits.append(str(n % 10))
            n = n // 10 - 1
            if n < 0:
                break
        return NovaeInt(''.join(reversed(digits)))

    def __repr__(self): return f"NovaeInt('{self.symbol}')"
    def __str__(self): return self.symbol
    def __eq__(self, other): return self.symbol == other.symbol

class NovaeFloat:
    """
    Numero frazionario Novae.
    Esempi: ∅.4 (0.5 decimale), 0.8 (1.9 decimale), 9.9 (11 decimale).
    """
    def __init__(self, intero='∅', fraz=''):
        if intero == '': intero = '∅'
        self.intero = intero
        self.fraz = fraz

    def __repr__(self): return f"NovaeFloat('{self.intero}.{self.fraz}')"
    def __str__(self):
        if self.fraz == '':
            return self.intero
        return f"{self.intero}.{self.fraz}"

    def to_dec(self):
        val = 0.0
        if self.intero != '∅':
            for i, c in enumerate(reversed(self.intero)):
                val += (int(c) + 1) * (10 ** i)
        for j, c in enumerate(self.fraz):
            val += (int(c) + 1) * (10 ** (-j - 1))
        return val

    @staticmethod
    def da_decimale(valore, max_cifre=10):
        if valore < 0:
            raise ValueError("Valori negativi non ancora supportati")
        parte_intera = int(valore)
        if parte_intera == 0:
            intero_str = '∅'
        else:
            intero_str = NovaeInt.from_int(parte_intera).symbol
        resto = valore - parte_intera
        fraz_str = ''
        for _ in range(max_cifre):
            if resto < 1e-12:
                break
            resto *= 10
            cifra = int(resto)
            cifra_novae = cifra - 1
            if cifra_novae < 0:
                cifra_novae = 0
            fraz_str += str(cifra_novae)
            resto -= cifra
        return NovaeFloat(intero_str, fraz_str)

    def __add__(self, other):
        max_len = max(len(self.fraz), len(other.fraz))
        s_fraz = self.fraz.ljust(max_len, '0') if self.fraz else '0' * max_len
        o_fraz = other.fraz.ljust(max_len, '0') if other.fraz else '0' * max_len

        riporto = -1
        risultato_fraz = ''
        for i in range(max_len - 1, -1, -1):
            val_a = int(s_fraz[i]) + 1
            val_b = int(o_fraz[i]) + 1
            val_sum = val_a + val_b + (1 if riporto != -1 else 0)
            if val_sum > 10:
                val_sum -= 10
                riporto = 0
            else:
                riporto = -1
            cifra_novae = val_sum - 1
            risultato_fraz = str(cifra_novae) + risultato_fraz

        def intero_to_val(s):
            if s == '∅': return 0
            val = 0
            for c in s:
                val = val * 10 + (int(c) + 1)
            return val

        val_int_self = intero_to_val(self.intero)
        val_int_other = intero_to_val(other.intero)
        val_int_sum = val_int_self + val_int_other + (1 if riporto != -1 else 0)

        if val_int_sum == 0:
            intero_str = '∅'
        else:
            intero_str = NovaeInt.from_int(val_int_sum).symbol

        return NovaeFloat(intero_str, risultato_fraz)

    def __mul__(self, other):
        val_self = self.to_dec()
        val_other = other.to_dec()
        val_prod = val_self * val_other
        if abs(val_prod - round(val_prod)) < 1e-12:
            return NovaeFloat(NovaeInt.from_int(int(round(val_prod))).symbol, '')
        return NovaeFloat.da_decimale(val_prod)
