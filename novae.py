"""
Libreria Novae - Sistema di Numerazione Non-Decimato
----------------------------------------------------
Fornisce i tipi `NovaeID` e `NovaeInt` per eliminare
l'ambiguità dello zero e operare nativamente in Novae.
"""

class NullPointerError(Exception):
    """Eccezione sollevata quando si tenta di dereferenziare un NovaeID vuoto."""
    pass

class NovaeID:
    VUOTO = None  # Sarà inizializzato dopo la definizione

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
        if self.is_vuoto():
            return "∅"
        return f"NovaeID({self._value})"

    def __str__(self):
        return str(self._value) if not self.is_vuoto() else "∅"

    def __bool__(self):
        # Un NovaeID valido è sempre True (anche 0!)
        return not self.is_vuoto()

class _VuotoNovaeID(NovaeID):
    def __init__(self):
        pass
    def is_vuoto(self):
        return True
    def __repr__(self):
        return "∅"
    def __str__(self):
        return "∅"
    def __bool__(self):
        return False

NovaeID.VUOTO = _VuotoNovaeID()

def _successor(sym: str) -> str:
    if sym == '9':
        return '00'
    last = sym[-1]
    if last != '9':
        return sym[:-1] + str(int(last) + 1)
    else:
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
        steps = other.to_int()  # Il valore decimale di other è il numero di passi
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
        """
        Restituisce il valore decimale del simbolo Novae.
        Esempi: '0' -> 1, '5' -> 6, '9' -> 10, '00' -> 11.
        """
        val = 0
        for c in self.symbol:
            val = val * 10 + (int(c) + 1)
        return val

    @staticmethod
    def from_int(n: int) -> 'NovaeInt':
        """
        Converte un intero decimale (quantità) in simbolo Novae.
        Esempi: 1 -> '0', 2 -> '1', 10 -> '9', 11 -> '00'.
        """
        if n <= 0:
            raise ValueError("Intero deve essere >= 1")
        n -= 1  # shift perché 0 Novae = 1 decimale
        if n == 0:
            return NovaeInt('0')
        digits = []
        while n >= 0:
            digits.append(str(n % 10))
            n = n // 10 - 1
            if n < 0:
                break
        return NovaeInt(''.join(reversed(digits)))

    def __repr__(self):
        return f"NovaeInt('{self.symbol}')"
    def __str__(self):
        return self.symbol
    def __eq__(self, other):
        return self.symbol == other.symbol
