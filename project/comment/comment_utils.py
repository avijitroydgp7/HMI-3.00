# project/comment/comment_utils.py
import re
import statistics
import operator

FUNCTION_HINTS = {
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
    "CHAR": "CHAR(number)",
    "VLOOKUP": "VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])",
    "HLOOKUP": "HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup])",
    "TRIM": "TRIM(text)",
    "REPLACE": "REPLACE(old_text, start_num, num_chars, new_text)",
    "SUBSTITUTE": "SUBSTITUTE(text, old_text, new_text, [instance_num])",
    "IFERROR": "IFERROR(value, value_if_error)",
    "IFNA": "IFNA(value, value_if_na)",
}


class FormulaParser:
    def __init__(self, table, cell):
        self.table = table
        self.cell = cell
        self.ops = {
            '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv,
            '^': operator.pow,
            '=': operator.eq, '==': operator.eq,
            '<': operator.lt, '>': operator.gt,
            '<=': operator.le, '>=': operator.ge,
            '!=': operator.ne, '<>': operator.ne,
        }
        self.precedence = {
            '+': 1, '-': 1, '*': 2, '/': 2, '^': 3,
            '=': 0, '==': 0, '<': 0, '>': 0, '<=': 0, '>=': 0, '!=': 0, '<>': 0
        }
        self.functions = {
            'SUM': lambda *args: sum(args),
            'AVERAGE': lambda *args: statistics.mean(args) if args else 0,
            'MAX': max,
            'MIN': min,
            'COUNT': lambda *args: len(args),
            'IF': lambda *args: args[1] if args[0] else (args[2] if len(args) > 2 else False),
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
            'DEC2HEX': hex,
            'DEC2BIN': bin,
            'DEC2OCT': oct,
            'HEX2DEC': lambda h: int(h, 16),
            'HEX2BIN': lambda h: bin(int(h, 16)),
            'HEX2OCT': lambda h: oct(int(h, 16)),
            'BIN2DEC': lambda b: int(b, 2),
            'BIN2HEX': lambda b: hex(int(b, 2)),
            'BIN2OCT': lambda b: oct(int(b, 2)),
            'OCT2DEC': lambda o: int(o, 8),
            'OCT2BIN': lambda o: bin(int(o, 8)),
            'OCT2HEX': lambda o: hex(int(o, 8)),
            'CHAR': chr,
            'VLOOKUP': self._vlookup,
            'HLOOKUP': self._hlookup,
            'TRIM': lambda s: str(s).strip(),
            'REPLACE': lambda old_text, start_num, num_chars, new_text: self._replace(old_text, start_num, num_chars, new_text),
            'SUBSTITUTE': lambda text, old_text, new_text, instance_num=None: self._substitute(text, old_text, new_text, instance_num),
            'IFERROR': self._iferror,
            'IFNA': self._ifna,
        }

    def evaluate(self, expression):
        try:
            tokens = self._tokenize(expression)
            rpn = self._shunting_yard(tokens)
            return self._evaluate_rpn(rpn)
        except Exception as e:
            # Check for IFERROR/IFNA at the top level
            match = re.match(r"^\s*IF(ERROR|NA)\((.*)\)\s*$", expression, re.IGNORECASE)
            if match:
                func_type = match.group(1).upper()
                inner_expr = match.group(2)
                # This is a simplified fallback for top-level IFERROR/IFNA
                # The robust solution is within _evaluate_rpn
                try:
                    # Attempt to evaluate the value part
                    value_expr, value_if_error_expr = self._split_if_args(inner_expr)
                    self.evaluate(value_expr) # This will raise an error if it fails
                except Exception:
                    _, value_if_error_expr = self._split_if_args(inner_expr)
                    return self.evaluate(value_if_error_expr)

            raise e # Re-raise if not a top-level IFERROR/IFNA

    def _split_if_args(self, args_str):
        paren_level = 0
        split_index = -1
        for i, char in enumerate(args_str):
            if char == '(':
                paren_level += 1
            elif char == ')':
                paren_level -= 1
            elif char == ',' and paren_level == 0:
                split_index = i
                break
        if split_index == -1:
            raise ValueError("Invalid IFERROR/IFNA arguments")
        return args_str[:split_index], args_str[split_index+1:]

    def _tokenize(self, expression):
        token_specification = [
            ('FUNCTION',  r'[A-Z][A-Z0-9_]*\('),
            ('CELLRANGE', r'[A-Z]+[0-9]+:[A-Z]+[0-9]+'),
            ('CELL',      r'[A-Z]+[0-9]+'),
            ('NUMBER',    r'[0-9]+(\.[0-9]*)?'),
            ('BOOLEAN',   r'TRUE|FALSE'),
            ('OP',        r'<=|>=|<>|!=|==|<|>|[\+\-\*/\^]'),
            ('LPAREN',    r'\('),
            ('RPAREN',    r'\)'),
            ('COMMA',     r','),
            ('STRING',    r'"[^"]*"'),
            ('MISMATCH',  r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        tokens = []
        for mo in re.finditer(tok_regex, expression, re.IGNORECASE):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'FUNCTION':
                tokens.append((kind, value[:-1].upper()))
                tokens.append(('LPAREN', '('))
            elif kind not in ['MISMATCH']:
                tokens.append((kind, value))
        return tokens

    def _shunting_yard(self, tokens):
        output = []
        operators = []
        arg_counts = []

        for i, (kind, value) in enumerate(tokens):
            if kind in ('NUMBER', 'CELL', 'CELLRANGE', 'STRING', 'BOOLEAN'):
                output.append((kind, value))
            elif kind == 'FUNCTION':
                operators.append((kind, value))
                if i + 1 < len(tokens) and tokens[i+1][0] == 'RPAREN':
                    arg_counts.append(0)
                else:
                    arg_counts.append(1)
            elif kind == 'COMMA':
                if not arg_counts: raise ValueError("Comma outside of function arguments")
                arg_counts[-1] += 1
                while operators and operators[-1][0] != 'LPAREN':
                    output.append(operators.pop())
            elif kind == 'OP':
                while (operators and operators[-1][0] == 'OP' and
                       self.precedence.get(operators[-1][1], 0) >= self.precedence.get(value, 0)):
                    output.append(operators.pop())
                operators.append((kind, value))
            elif kind == 'LPAREN':
                operators.append((kind, value))
            elif kind == 'RPAREN':
                while operators and operators[-1][0] != 'LPAREN':
                    output.append(operators.pop())
                if not operators or operators.pop()[0] != 'LPAREN':
                    raise ValueError("Mismatched parentheses")

                if operators and operators[-1][0] == 'FUNCTION':
                    func_token = operators.pop()
                    arg_count = arg_counts.pop() if arg_counts else 0
                    output.append(('FUNCTION_EXEC', (func_token[1], arg_count)))


        while operators:
            op_kind, op_val = operators.pop()
            if op_kind in ('LPAREN', 'RPAREN'):
                raise ValueError("Mismatched parentheses in operator stack")
            output.append((op_kind, op_val))
        return output

    def _evaluate_rpn(self, rpn_tokens):
        stack = []
        for kind, value in rpn_tokens:
            if kind == 'NUMBER':
                stack.append(float(value))
            elif kind == 'BOOLEAN':
                stack.append(value.upper() == 'TRUE')
            elif kind == 'STRING':
                stack.append(value[1:-1])
            elif kind == 'CELL':
                row, col = self.table.cell_ref_to_indices(value)
                stack.append(self.table.get_cell_value(row, col, dependent_cell=self.cell))
            elif kind == 'CELLRANGE':
                stack.append(self._get_range_values(value))
            elif kind == 'OP':
                if len(stack) < 2: raise ValueError(f"Syntax Error: Not enough operands for '{value}'")
                right, left = stack.pop(), stack.pop()
                stack.append(self.ops[value](left, right))
            elif kind == 'FUNCTION_EXEC':
                func_name, arg_count = value
                if len(stack) < arg_count: raise ValueError(f"Not enough arguments for {func_name}")

                args = [stack.pop() for _ in range(arg_count)]
                args.reverse()

                flat_args = []
                for arg in args:
                    if isinstance(arg, list) and func_name not in ('VLOOKUP', 'HLOOKUP'):
                        for row_list in arg:
                            flat_args.extend(row_list)
                    else:
                        flat_args.append(arg)

                result = self.functions[func_name](*flat_args)
                stack.append(result)

        return stack[0] if stack else 0

    def _get_range_values(self, range_str, as_string=False):
        values = []
        start_ref, end_ref = range_str.split(':')
        start_row, start_col = self.table.cell_ref_to_indices(start_ref)
        end_row, end_col = self.table.cell_ref_to_indices(end_ref)

        if start_row > end_row: start_row, end_row = end_row, start_row
        if start_col > end_col: start_col, end_col = end_col, start_col

        for r in range(start_row, end_row + 1):
            row_values = []
            for c in range(start_col, end_col + 1):
                 row_values.append(self.table.get_cell_value(r, c, as_string=as_string, dependent_cell=self.cell))
            values.append(row_values)
        return values

    def _vlookup(self, lookup_value, table_array, col_index_num, range_lookup=True):
        col_index_num = int(col_index_num) - 1

        for row in table_array:
            if (range_lookup and str(lookup_value).lower() in str(row[0]).lower()) or \
               (not range_lookup and str(lookup_value) == str(row[0])):
                return row[col_index_num]
        return "#N/A"

    def _hlookup(self, lookup_value, table_array, row_index_num, range_lookup=True):
        row_index_num = int(row_index_num) - 1

        num_cols = len(table_array[0])
        for c in range(num_cols):
            if (range_lookup and str(lookup_value).lower() in str(table_array[0][c]).lower()) or \
               (not range_lookup and str(lookup_value) == str(table_array[0][c])):
                return table_array[row_index_num][c]
        return "#N/A"

    def _replace(self, old_text, start_num, num_chars, new_text):
        old_text = str(old_text)
        start_num = int(start_num) - 1
        num_chars = int(num_chars)
        return old_text[:start_num] + str(new_text) + old_text[start_num + num_chars:]

    def _substitute(self, text, old_text, new_text, instance_num=None):
        text = str(text)
        old_text = str(old_text)
        new_text = str(new_text)
        if instance_num:
            return text.replace(old_text, new_text, int(instance_num))
        return text.replace(old_text, new_text)

    def _iferror(self, value, value_if_error):
        # This will be called by the evaluation logic.
        # The value is already evaluated at this point.
        # We need a way to check if it was an error.
        # A simple check for string error codes can work here.
        if isinstance(value, str) and value.startswith('#'):
            return value_if_error
        return value

    def _ifna(self, value, value_if_na):
        if value == "#N/A":
            return value_if_na
        return value