# project/comment/comment_utils.py
import re
import statistics
import operator
import math

FUNCTION_HINTS = {
    # ... (keep existing dict)
    "SUM": "SUM(value1, [value2], ...)",
    "AVERAGE": "AVERAGE(value1, [value2], ...)",
    "MAX": "MAX(value1, [value2], ...)",
    "MIN": "MIN(value1, [value2], ...)",
    "COUNT": "COUNT(value1, [value2], ...)",
    "IF": "IF(logical_test, value_if_true, [value_if_false])",
    "AND": "AND(logical1, [logical2], ...)",
    "OR": "OR(logical1, [logical2], ...)",
    "NOT": "NOT(logical)",
    "TRUE": "TRUE()",
    "FALSE": "FALSE()",
    "UPPER": "UPPER(text)",
    "LOWER": "LOWER(text)",
    "LEN": "LEN(text)",
    "LEFT": "LEFT(text, [num_chars])",
    "RIGHT": "RIGHT(text, [num_chars])",
    "MID": "MID(text, start_num, num_chars)",
    "CONCAT": "CONCAT(text1, [text2], ...)",
    "INT": "INT(number)",
    "DEC2HEX": "DEC2HEX(number)",
    "DEC2BIN": "DEC2BIN(number)",
    "DEC2OCT": "DEC2OCT(number)",
    "HEX2DEC": "HEX2DEC(hex_number)",
    "HEX2BIN": "HEX2BIN(hex_number)",
    "HEX2OCT": "HEX2OCT(hex_number)",
    "BIN2DEC": "BIN2DEC(binary_number)",
    "BIN2HEX": "BIN2HEX(binary_number)",
    "BIN2OCT": "BIN2OCT(binary_number)",
    "OCT2DEC": "OCT2DEC(octal_number)",
    "OCT2BIN": "OCT2BIN(octal_number)",
    "OCT2HEX": "OCT2HEX(octal_number)",
    "BITAND": "BITAND(number1, number2)",
    "BITOR": "BITOR(number1, number2)",
    "BITXOR": "BITXOR(number1, number2)",
    "BITLSHIFT": "BITLSHIFT(number, shift_amount)",
    "BITRSHIFT": "BITRSHIFT(number, shift_amount)",
    "CHAR": "CHAR(number)",
    "CODE": "CODE(text)",
    "BASE": "BASE(number, radix, [min_length])",
    "DECIMAL": "DECIMAL(text, radix)",
    "VLOOKUP": "VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])",
    "HLOOKUP": "HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup])",
    "TRIM": "TRIM(text)",
    "REPLACE": "REPLACE(old_text, start_num, num_chars, new_text)",
    "SUBSTITUTE": "SUBSTITUTE(text, old_text, new_text, [instance_num])",
    "IFERROR": "IFERROR(value, value_if_error)",
    "IFNA": "IFNA(value, value_if_na)",
}

def col_str_to_int(col_str):
    num = 0
    for char in col_str:
        num = num * 26 + (ord(char.upper()) - ord('A')) + 1
    return num - 1

def col_int_to_str(col_idx):
    col_str = ""
    temp = col_idx
    while temp >= 0:
        col_str = chr(ord('A') + temp % 26) + col_str
        temp = temp // 26 - 1
    return col_str

def adjust_formula_references(formula, row_offset, col_offset, min_row=0, min_col=0, delete_row=-1, delete_col=-1):
    if not formula.startswith('='):
        return formula

    ref_regex = re.compile(r"(\$?[A-Z]+)(\$?\d+)")

    def replacement(match):
        col_part = match.group(1)
        row_part = match.group(2)
        
        # Check if column is absolute (starts with $)
        is_col_absolute = col_part.startswith('$')
        # Check if row is absolute (contains $)
        is_row_absolute = row_part.startswith('$')
        
        # Extract column letter (without $) and row number (without $)
        col_letter = col_part.lstrip('$')
        row_number = row_part.lstrip('$')
        
        col_idx = col_str_to_int(col_letter)
        row_idx = int(row_number) - 1

        # Check for deleted row/column references
        if (delete_row != -1 and row_idx == delete_row) or \
           (delete_col != -1 and col_idx == delete_col):
            return "#REF!"

        # Only shift row if it's not absolute and >= threshold
        if not is_row_absolute and row_idx >= min_row:
            row_idx += row_offset
        # Only shift column if it's not absolute and >= threshold
        if not is_col_absolute and col_idx >= min_col:
            col_idx += col_offset
            
        if row_idx < 0 or col_idx < 0:
            return "#REF!"
        
        # Reconstruct reference with proper $ markers
        col_str = ('$' if is_col_absolute else '') + col_int_to_str(col_idx)
        row_str = ('$' if is_row_absolute else '') + str(row_idx + 1)
        return f"{col_str}{row_str}"

    parts = re.split(r'("[^"]*")', formula)
    for i, part in enumerate(parts):
        if not part.startswith('"'):
            parts[i] = ref_regex.sub(replacement, part)
    
    return "".join(parts)


class FormulaParser:
    def __init__(self, table_interface, current_cell_coords):
        self.table = table_interface
        self.current_cell = current_cell_coords
        self.pos = 0
        self.tokens = []
        
        self.functions = {
            'SUM': lambda *args: sum(float(x) for x in args if self._is_number(x)),
            'AVERAGE': lambda *args: statistics.mean(float(x) for x in args if self._is_number(x)) if any(self._is_number(x) for x in args) else 0,
            'MAX': lambda *args: max((float(x) for x in args if self._is_number(x)), default=0),
            'MIN': lambda *args: min((float(x) for x in args if self._is_number(x)), default=0),
            'COUNT': lambda *args: sum(1 for x in args if self._is_number(x)),
            'AND': lambda *args: all(args),
            'OR': lambda *args: any(args),
            'NOT': lambda x: not x,
            'TRUE': lambda: True,
            'FALSE': lambda: False,
            'UPPER': lambda s: str(s).upper(),
            'LOWER': lambda s: str(s).lower(),
            'LEN': lambda s: len(str(s)),
            'LEFT': lambda s, n=1: str(s)[:int(n)],
            'RIGHT': lambda s, n=1: str(s)[-int(n):],
            'MID': lambda s, start, n: str(s)[int(start)-1:int(start)-1+int(n)],
            'CONCAT': lambda *args: "".join(map(str, args)),
            'INT': int,
            'TRIM': lambda s: str(s).strip(),
            'CHAR': lambda n: chr(int(n)),
            'CODE': lambda s: ord(str(s)[0]) if s else 0,
            'DEC2HEX': lambda n: hex(int(n))[2:].upper(),
            'DEC2BIN': lambda n: bin(int(n))[2:],
            'DEC2OCT': lambda n: oct(int(n))[2:],
            'HEX2DEC': lambda h: int(str(h), 16),
            'HEX2BIN': lambda h: bin(int(str(h), 16))[2:],
            'HEX2OCT': lambda h: oct(int(str(h), 16))[2:],
            'BIN2DEC': lambda b: int(str(b), 2),
            'BIN2HEX': lambda b: hex(int(str(b), 2))[2:].upper(),
            'BIN2OCT': lambda b: oct(int(str(b), 2))[2:],
            'OCT2DEC': lambda o: int(str(o), 8),
            'OCT2BIN': lambda o: bin(int(str(o), 8))[2:],
            'OCT2HEX': lambda o: hex(int(str(o), 8))[2:].upper(),
            'BASE': self._base,
            'DECIMAL': lambda text, radix: int(str(text), int(radix)),
            'BITAND': lambda a, b: int(a) & int(b),
            'BITOR': lambda a, b: int(a) | int(b),
            'BITXOR': lambda a, b: int(a) ^ int(b),
            'BITLSHIFT': lambda n, s: int(n) << int(s),
            'BITRSHIFT': lambda n, s: int(n) >> int(s),
            'VLOOKUP': self._vlookup,
            'HLOOKUP': self._hlookup,
            'REPLACE': lambda old, start, n, new: str(old)[:int(start)-1] + str(new) + str(old)[int(start)-1+int(n):],
            'SUBSTITUTE': self._substitute
        }

    def _is_number(self, s):
        try:
            float(s)
            return True
        except (ValueError, TypeError):
            return False

    def _base(self, number, radix, min_length=0):
        res = ""
        num = int(number)
        rad = int(radix)
        if rad < 2 or rad > 36: return "#NUM!"
        
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if num == 0: res = "0"
        else:
            while num > 0:
                res = chars[num % rad] + res
                num //= rad
        
        if min_length and len(res) < int(min_length):
            res = res.zfill(int(min_length))
        return res

    def _compare(self, a, b, op):
        if isinstance(a, str) and isinstance(b, str):
            return op(a.lower(), b.lower())
        try:
            return op(a, b)
        except TypeError:
            return False

    def evaluate(self, expression):
        if not expression: return ""
        try:
            self.tokens = self._tokenize(expression)
            self.pos = 0
            result = self._parse_expression()
            return result
        except Exception as e:
            return f"#ERROR: {str(e)}"

    def _tokenize(self, expression):
        token_specification = [
            ('FUNCTION',  r'[A-Z][A-Z0-9_]*\('),
            ('CELLRANGE', r'[A-Z]+[0-9]+:[A-Z]+[0-9]+'),
            ('CELL',      r'[A-Z]+[0-9]+'),
            ('NUMBER',    r'[0-9]+(\.[0-9]*)?'),
            ('BOOLEAN',   r'TRUE|FALSE'),
            ('STRING',    r'"[^"]*"'),
            ('OP_CMP',    r'<=|>=|<>|!=|==|<|>|='), 
            ('OP_ADD',    r'[\+\-]'),
            ('OP_MUL',    r'[\*/]'),
            ('OP_POW',    r'\^'),
            ('LPAREN',    r'\('),
            ('RPAREN',    r'\)'),
            ('COMMA',     r','),
            ('WHITESPACE',r'\s+'),
            ('IDENTIFIER',r'[A-Z][A-Z0-9_]*'), # Catch-all for text like 'SUM' without parens or 's'
            ('MISMATCH',  r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        tokens = []
        for mo in re.finditer(tok_regex, expression, re.IGNORECASE):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'WHITESPACE':
                continue
            if kind == 'FUNCTION':
                tokens.append((kind, value[:-1].upper()))
                tokens.append(('LPAREN', '('))
            elif kind == 'STRING':
                tokens.append((kind, value[1:-1]))
            elif kind == 'BOOLEAN':
                tokens.append((kind, value.upper() == 'TRUE'))
            elif kind == 'NUMBER':
                tokens.append((kind, float(value)))
            elif kind == 'IDENTIFIER':
                # Keep it as is, will raise #NAME? in parser
                tokens.append((kind, value))
            elif kind == 'MISMATCH':
                raise ValueError(f"Unexpected character: {value}")
            else:
                tokens.append((kind, value))
        return tokens

    def _peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _consume(self, kind=None):
        token = self._peek()
        if not token:
            raise ValueError("Unexpected end of formula")
        if kind and token[0] != kind:
            raise ValueError(f"Expected {kind}, got {token[0]}")
        self.pos += 1
        return token

    def _parse_expression(self):
        return self._parse_comparison()

    def _parse_comparison(self):
        left = self._parse_additive()
        while True:
            token = self._peek()
            if token and token[0] == 'OP_CMP':
                op_str = self._consume()[1]
                right = self._parse_additive()
                if op_str in ['=', '==']: left = self._compare(left, right, operator.eq)
                elif op_str == '<': left = self._compare(left, right, operator.lt)
                elif op_str == '>': left = self._compare(left, right, operator.gt)
                elif op_str == '<=': left = self._compare(left, right, operator.le)
                elif op_str == '>=': left = self._compare(left, right, operator.ge)
                elif op_str in ['!=', '<>']: left = self._compare(left, right, operator.ne)
            else:
                break
        return left

    def _parse_additive(self):
        left = self._parse_multiplicative()
        while True:
            token = self._peek()
            if token and token[0] == 'OP_ADD':
                op_str = self._consume()[1]
                right = self._parse_multiplicative()
                if op_str == '+': left += right
                elif op_str == '-': left -= right
            else:
                break
        return left

    def _parse_multiplicative(self):
        left = self._parse_power()
        while True:
            token = self._peek()
            if token and token[0] == 'OP_MUL':
                op_str = self._consume()[1]
                right = self._parse_power()
                if op_str == '*': left *= right
                elif op_str == '/': 
                    if right == 0: raise ValueError("Div by Zero")
                    left /= right
            else:
                break
        return left
    
    def _parse_power(self):
        left = self._parse_atom()
        token = self._peek()
        if token and token[0] == 'OP_POW':
            self._consume()
            right = self._parse_power()
            left = left ** right
        return left

    def _parse_atom(self):
        token = self._peek()
        if not token:
            raise ValueError("Unexpected end of formula")

        kind, value = token

        if kind == 'NUMBER':
            self._consume()
            return value
        elif kind == 'STRING':
            self._consume()
            return value
        elif kind == 'BOOLEAN':
            self._consume()
            return value
        elif kind == 'LPAREN':
            self._consume()
            val = self._parse_expression()
            self._consume('RPAREN')
            return val
        elif kind == 'CELL':
            self._consume()
            return self._resolve_cell(value)
        elif kind == 'CELLRANGE':
            self._consume()
            return self._resolve_range(value)
        elif kind == 'FUNCTION':
            self._consume()
            return self._parse_function_call(value)
        elif kind == 'IDENTIFIER':
            self._consume()
            # Treat unknown text as #NAME? error
            raise ValueError(f"#NAME? {value}")
        elif kind == 'OP_ADD' and value == '-':
            self._consume()
            return -self._parse_atom()
        else:
            raise ValueError(f"Unexpected token {value}")

    def _parse_function_call(self, func_name):
        self._consume('LPAREN')

        if func_name == 'IF':
            return self._handle_if()
        elif func_name == 'IFERROR':
            return self._handle_iferror()
        elif func_name == 'IFNA':
            return self._handle_ifna()
        
        args = []
        if self._peek()[0] != 'RPAREN':
            while True:
                args.append(self._parse_expression())
                if self._peek()[0] == 'COMMA':
                    self._consume()
                else:
                    break
        self._consume('RPAREN')
        
        if func_name in ['VLOOKUP', 'HLOOKUP']:
            final_args = args
        else:
            final_args = []
            for arg in args:
                if isinstance(arg, list):
                    for sub in arg:
                        if isinstance(sub, list): final_args.extend(sub)
                        else: final_args.append(sub)
                else:
                    final_args.append(arg)

        if func_name in self.functions:
            return self.functions[func_name](*final_args)
        else:
            raise ValueError(f"Unknown function {func_name}")

    def _handle_if(self):
        condition = self._parse_expression()
        self._consume('COMMA')
        
        result = False
        if condition:
            result = self._parse_expression()
            if self._peek()[0] == 'COMMA':
                self._consume()
                self._skip_expression() 
        else:
            self._skip_expression()
            if self._peek()[0] == 'COMMA':
                self._consume()
                result = self._parse_expression()
            else:
                result = False
        
        self._consume('RPAREN')
        return result

    def _handle_iferror(self):
        start_pos = self.pos
        try:
            val = self._parse_expression()
            self._consume('COMMA')
            self._skip_expression()
            self._consume('RPAREN')
            return val
        except Exception:
            self.pos = start_pos
            self._skip_expression()
            self._consume('COMMA')
            val_error = self._parse_expression()
            self._consume('RPAREN')
            return val_error

    def _handle_ifna(self):
        val = self._parse_expression()
        self._consume('COMMA')
        val_if_na = self._parse_expression()
        self._consume('RPAREN')
        if str(val) == "#N/A":
            return val_if_na
        return val

    def _skip_expression(self):
        nesting = 0
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token[0] == 'LPAREN':
                nesting += 1
            elif token[0] == 'RPAREN':
                if nesting == 0: break
                nesting -= 1
            elif token[0] == 'COMMA':
                if nesting == 0: break
            self.pos += 1

    def _resolve_cell(self, ref):
        match = re.match(r"([A-Z]+)(\d+)", ref.upper())
        if not match: raise ValueError("Invalid cell ref")
        col_str, row_str = match.groups()
        row = int(row_str) - 1
        col = col_str_to_int(col_str)
        if hasattr(self.table, 'add_dependency'):
            self.table.add_dependency(self.current_cell, (row, col))
        return self.table.get_cell_value(row, col)

    def _resolve_range(self, ref_range):
        start_ref, end_ref = ref_range.split(':')
        r1, c1 = self._cell_coords(start_ref)
        r2, c2 = self._cell_coords(end_ref)
        vals = []
        for r in range(min(r1, r2), max(r1, r2) + 1):
            row_vals = []
            for c in range(min(c1, c2), max(c1, c2) + 1):
                if hasattr(self.table, 'add_dependency'):
                    self.table.add_dependency(self.current_cell, (r, c))
                row_vals.append(self.table.get_cell_value(r, c))
            vals.append(row_vals)
        return vals

    def _cell_coords(self, ref):
        match = re.match(r"([A-Z]+)(\d+)", ref.upper())
        col_str, row_str = match.groups()
        return int(row_str) - 1, col_str_to_int(col_str)

    def _vlookup(self, lookup_val, table_array, col_idx_num, range_lookup=True):
        col_idx = int(col_idx_num) - 1
        lookup_str = str(lookup_val).lower()
        if not isinstance(table_array, list) or not table_array: return "#N/A"
        
        if str(range_lookup).upper() == 'FALSE' or range_lookup is False or range_lookup == 0:
            for row in table_array:
                if len(row) > 0 and str(row[0]).lower() == lookup_str:
                    return row[col_idx] if col_idx < len(row) else "#REF!"
            return "#N/A"
        
        best = None
        for row in table_array:
            if not row: continue
            val = row[0]
            try:
                if val == lookup_val: 
                    return row[col_idx] if col_idx < len(row) else "#REF!"
                if val <= lookup_val: 
                    best = row
                else: break
            except: continue
        
        if best and col_idx < len(best): return best[col_idx]
        return "#N/A"

    def _hlookup(self, lookup_val, table_array, row_idx_num, range_lookup=True):
        row_idx = int(row_idx_num) - 1
        lookup_str = str(lookup_val).lower()
        if not isinstance(table_array, list) or not table_array: return "#N/A"
        
        if str(range_lookup).upper() == 'FALSE' or range_lookup is False:
            for c in range(len(table_array[0])):
                val = table_array[0][c]
                if str(val).lower() == lookup_str:
                    return table_array[row_idx][c] if row_idx < len(table_array) else "#REF!"
            return "#N/A"
        return "#N/A"

    def _substitute(self, text, old, new, instance=None):
        text, old, new = str(text), str(old), str(new)
        if instance:
            count = int(instance)
            parts = text.split(old)
            if len(parts) <= count: return text
            return old.join(parts[:count]) + new + old.join(parts[count:])
        return text.replace(old, new)