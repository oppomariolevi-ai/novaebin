
---

### File 2: `binario_novae.py`

```python
"""
Interprete Binario Novae v1.1
Successione pura: ∅, 0, 1, 00, 01, 10, 11, 000, ...
Nessuna conversione decimale.
"""

class NovaeBinary:
    def __init__(self):
        self.str_to_ord = {}
        self.ord_to_str = {}
        self._build_table(20)

    def _build_table(self, max_len):
        pos = 0
        for s in ['0', '1']:
            self.str_to_ord[s] = pos
            self.ord_to_str[pos] = s
            pos += 1
        for length in range(2, max_len + 1):
            for i in range(2 ** length):
                s = bin(i)[2:].zfill(length)
                self.str_to_ord[s] = pos
                self.ord_to_str[pos] = s
                pos += 1

    def successor(self, s):
        if s not in self.str_to_ord:
            raise ValueError(f"Stringa '{s}' non valida")
        ord_num = self.str_to_ord[s]
        next_ord = ord_num + 1
        if next_ord not in self.ord_to_str:
            max_len = max(len(x) for x in self.str_to_ord)
            self._build_table(max_len + 1)
            return self.successor(s)
        return self.ord_to_str[next_ord]

    def add(self, a, b):
        result = a
        steps = self.str_to_ord[b] + 1
        for _ in range(steps):
            result = self.successor(result)
        return result

    def multiply(self, a, b):
        if b == '0':
            return a
        result = '0'
        times = self.str_to_ord[b] + 1
        for _ in range(times):
            result = self.add(result, a)
        return result

    def value(self, s):
        return self.str_to_ord.get(s, -1)

    def string(self, ord_num):
        return self.ord_to_str.get(ord_num, None)


if __name__ == "__main__":
    nb = NovaeBinary()
    
    print("=== BINARIO NOVAE v1.1 ===")
    print("Successione iniziale:")
    for i in range(15):
        print(f"  {nb.string(i)} (posizione {i})")
    
    print("\n=== ADDIZIONE ===")
    print(f"0 + 0 = {nb.add('0', '0')}")
    print(f"0 + 1 = {nb.add('0', '1')}")
    print(f"1 + 1 = {nb.add('1', '1')}")
    print(f"00 + 01 = {nb.add('00', '01')}")
    
    print("\n=== MOLTIPLICAZIONE ===")
    print(f"0 * 0 = {nb.multiply('0', '0')}")
    print(f"0 * 1 = {nb.multiply('0', '1')}")
    print(f"1 * 1 = {nb.multiply('1', '1')}")
    print(f"1 * 00 = {nb.multiply('1', '00')}")
    print(f"00 * 01 = {nb.multiply('00', '01')}")

    print("\n=== DENSITÀ ===")
    print("Con stringhe fino a 3 bit: 14 valori (∅ escluso)")
