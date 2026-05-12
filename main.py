import sys

# --- تعريف الرموز (Tokens) ---
# أضفنا LOOP و TO بناءً على الكويز
NUM, ID, IF, THEN, WHILE, DO, BEGIN, END, VOID, MAIN, LOOP, TO, EOF = range(256, 269)

# --- المتغيرات العالمية ---
input_text = "void main() begin loop x = x - y; to (x) end" # مثال الكويز
input_index = 0
lookahead = None
tokenval = None
lineno = 1

# --- المحلل اللغوي (Lexical Analyzer) ---
def lexan():
    global input_index, tokenval, lineno
    while True:
        if input_index >= len(input_text): return EOF
        t = input_text[input_index]
        input_index += 1
        if t in ' \t': continue
        if t == '\n':
            lineno += 1
            continue
        if t.isdigit():
            num_str = t
            while input_index < len(input_text) and input_text[input_index].isdigit():
                num_str += input_text[input_index]; input_index += 1
            tokenval = int(num_str)
            return NUM
        if t.isalpha():
            id_str = t
            while input_index < len(input_text) and input_text[input_index].isalnum():
                id_str += input_text[input_index]; input_index += 1
            # الكلمات المحجوزة شاملة المراحل 6 و 7 والكويز
            keywords = {
                "if": IF, "then": THEN, "while": WHILE, "do": DO, 
                "begin": BEGIN, "end": END, "void": VOID, "main": MAIN,
                "loop": LOOP, "to": TO
            }
            tokenval = id_str
            return keywords.get(id_str, ID)
        return t

# --- دوال المساعدة ---
def match(token):
    global lookahead
    if lookahead == token: lookahead = lexan()
    else: error()

def error():
    print(f"\nSyntax error at line {lineno}")
    sys.exit(1)

# --- المحلل النحوي وتوليد الكود (Emitter) ---

def factor():
    global tokenval
    if lookahead == '(':
        match('('); expr(); match(')')
    elif lookahead == NUM:
        print(f"Push {tokenval}")
        match(NUM)
    elif lookahead == ID:
        print(f"Push {tokenval}")
        match(ID)

def term():
    factor()
    while lookahead in ['*', '/']:
        op = lookahead; match(op)
        factor()
        print(f"Pop r1\nPop r2\n{'Mult' if op=='*' else 'Div'} r2, r1\nPush r2")

def expr():
    term()
    while lookahead in ['+', '-']:
        op = lookahead; match(op)
        term()
        print(f"Pop r1\nPop r2\n{'Add' if op=='+' else 'Sub'} r2, r1\nPush r2")

def stmt():
    global tokenval
    if lookahead == ID:
        id_name = tokenval; match(ID)
        if lookahead == '=':
            match('='); expr(); print(f"Pop {id_name}")
        elif lookahead == '(':
            match('('); match(')'); print(f"Call {id_name}")
    
    elif lookahead == IF:
        match(IF); match('('); expr(); match(')')
        print("Pop r2\nCmp r2, 0\nBe else_label")
        match(THEN); stmt()
        print("else_label:")
        
    elif lookahead == WHILE:
        print("while_label:")
        match(WHILE); match('('); expr(); match(')')
        print("Pop r2\nCmp r2, 0\nBe endwhile_label")
        match(DO); stmt()
        print("B while_label\nendwhile_label:")

    # --- منطق الكويز: LOOP .. TO ---
    elif lookahead == LOOP:
        print("loop_label:") # الأكشن loop1()
        match(LOOP)
        cs() 
        match(TO)
        match('('); expr(); match(')')
        # الأكشن loop2()
        print("Pop r2\nCmp r2, 0\nBne loop_label") 

    elif lookahead == BEGIN:
        match(BEGIN); cs(); match(END)

def cs():
    while lookahead not in [END, TO, EOF, VOID]:
        stmt()
        if lookahead == ';': match(';')
        else: break

def prog():
    while lookahead == VOID:
        match(VOID)
        if lookahead == MAIN:
            match(MAIN); print("main:"); match('('); match(')'); 
            match(BEGIN); cs(); match(END); print("Exit")
        else:
            func_name = tokenval; match(ID); print(f"{func_name}:")
            match('('); match(')'); match(BEGIN); cs(); match(END); print("Ret")

# --- التشغيل واختبار الكود ---
if __name__ == "__main__":
    print("--- Intermediate Code Output ---")
    lookahead = lexan()
    prog()