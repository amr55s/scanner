# scanner_core.py

TOKEN_TYPES = {
    "int": "DataType",
    "float": "DataType",
    "char": "DataType",
    "if": "Keyword",
    "while": "Keyword",
    "for": "Keyword",
    "=": "Assignment",
    "==": "Equality",
    "+": "Operator",
    "-": "Operator",
    "*": "Operator",
    "/": "Operator",
    ";": "Semicolon"
}

class Token:
    def __init__(self, value, type_, line):
        self.value = value
        self.type = type_
        self.line = line

    def __str__(self):
        return f"{self.value}\t{self.type}\tLine {self.line}"

def is_number(token):
    return token.isdigit()

def is_identifier(token):
    return token.isidentifier()

def tokenize_line(line_text, line_number):
    tokens = []
    symbols = ["==", "=", ";", "+", "-", "*", "/"]
    for sym in symbols:
        line_text = line_text.replace(sym, f" {sym} ")
    parts = line_text.split()

    for part in parts:
        if part in TOKEN_TYPES:
            token_type = TOKEN_TYPES[part]
        elif is_number(part):
            token_type = "Number"
        elif is_identifier(part):
            token_type = "Identifier"
        else:
            token_type = "Unknown"
        tokens.append(Token(part, token_type, line_number))
    return tokens

def analyze_code(code):
    all_tokens = []
    lines = code.strip().split("\n")
    for i, line in enumerate(lines, start=1):
        line_tokens = tokenize_line(line, i)
        all_tokens.extend(line_tokens)
    return all_tokens

def write_tokens_to_file(tokens, base_name="output"):
    file_name = f"tokens_{base_name}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        for token in tokens:
            f.write(str(token) + "\n")
    return file_name  # عشان نعرض اسم الملف بعدين في الواجهة
