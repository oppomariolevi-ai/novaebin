"""
Libreria Novae - Sistema di Numerazione Non-Decimato
----------------------------------------------------
Fornisce i tipi `NovaeID` e `NovaeInt` per eliminare
l'ambiguità dello zero e operare nativamente in Novae.
"""

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
        if self.is_vuoto(): return "∅"
        return f"NovaeID({self._value})"

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
    if sym == '9': return '00'
    last = sym[-1]
    if last != '9':
        return sym[:-1] + str(int(last) + 1)
    else:
        prefix = sym[:-1]
        if prefix == '': return '00'
        return _successor(prefix) + '0'

class NovaeInt:
    def __init__(self, symbol: str):
        if not symbol or not all(c in '0123456789' for c in symbol):
            raise ValueError("Simbolo Novae non valido.")
        self.symbol = symbol

    def __add__(self, other: 'NovaeInt') -> 'NovaeInt':
        result = self.symbol
        steps = other.to_int() + 1
        for _ in range(steps):
            result = _successor(result)
        return NovaeInt(result)

    def __mul__(self, other: 'NovaeInt') -> 'NovaeInt':
        if other.symbol == '0':
            return NovaeInt(self.symbol)
        val_a = self.to_int()
        val_b = other.to_int()
        product_val = (val_a + 1) * (val_b + 1) - 1
        return NovaeInt.from_int(product_val)

    def __sub__(self, other: 'NovaeInt') -> 'NovaeInt':
        val_a = self.to_int()
        val_b = other.to_int()
        if val_b > val_a:
            raise ValueError("Risultato negativo non supportato.")
        diff_val = (val_a + 1) - (val_b + 1)
        return NovaeInt.from_int(diff_val)

    def __truediv__(self, other: 'NovaeInt') -> 'NovaeInt':
        if other.symbol == '0':
            return NovaeInt(self.symbol)
        return self.divide_frazionaria(other)  # Ora restituisce una stringa, non un NovaeInt

    def divide_frazionaria(self, other: 'NovaeInt', max_cifre=10) -> str:
        """Restituisce la divisione frazionaria Novae come stringa (es. '0.222...')."""
        if other.symbol == '0':
            return self.symbol
        val_a = self.to_int()
        val_b = other.to_int()
        q_val = (val_a + 1) // (val_b + 1) - 1
        r_val = (val_a + 1) % (val_b + 1)
        if r_val == 0:
            return NovaeInt.from_int(q_val).symbol
        parte_intera = NovaeInt.from_int(q_val).symbol if q_val >= 0 else ''
        if parte_intera == '':
            parte_intera = '∅'
        parte_frazionaria = ''
        for _ in range(max_cifre):
            if r_val == 0:
                break
            r_val *= 10
            cifra_val = r_val // (val_b + 1)
            r_val = r_val % (val_b + 1)
            parte_frazionaria += str(cifra_val - 1)
        return parte_intera + '.' + parte_frazionaria

    def to_int(self) -> int:
        val = 0
        for c in self.symbol:
            val = val * 10 + (int(c) + 1)
        return val - 1

    @staticmethod
    def from_int(n: int) -> 'NovaeInt':
        if n < 0:
            raise ValueError("Intero negativo non supportato.")
        n += 1
        digits = []
        while n > 0:
            n -= 1
            digits.append(str(n % 10))
            n //= 10
        return NovaeInt(''.join(reversed(digits)) if digits else '0')

    def __repr__(self):
        return f"NovaeInt('{self.symbol}')"
    def __str__(self):
        return self.symbol
    def __eq__(self, other):
        return self.symbol == other.symbol
