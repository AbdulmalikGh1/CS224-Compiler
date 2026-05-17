# parser.py
import sys
import lexer
import symbol
import emitter

lookahead = None

def error():
    print(f"Syntax error at line {lexer.lineno}")
    # كتابة الخطأ في ملف الأخطاء المخصص (Phase 3)
    with open("file.err", "w") as err_file:
        err_file.write(f"Syntax error at line {lexer.lineno}\n")
    sys.exit(1)

def match(token):
    global lookahead
    if lookahead == token:
        lookahead = lexer.lexan()
    else:
        error()

# --- مستويات الأولويات الحسابية (Phase 5) ---
def factor():
    global lookahead
    if lookahead == '(':
        match('('); expr(); match(')')
    elif lookahead == 'NUM':
        emitter.emit('NUM', lexer.tokenval)
        match('NUM')
    elif lookahead == 'ID':
        emitter.emit('ID', lexer.tokenval)
        match('ID')
    else:
        error()

def term():
    factor()
    while lookahead in ['*', '/']:
        op = lookahead; match(op)
        factor()
        emitter.emit(op)

def expr():
    term()
    while lookahead in ['+', '-']:
        op = lookahead; match(op)
        term()
        emitter.emit(op)

# --- قواعد التحكم والمنطق (Phase 6 & 7 & الكويزات) ---

def stmt():
    global lookahead
    
    # 1. إذا بدأت الجملة بمعرّف (تطبيق الـ Left Factoring بناءً على الفاينل لاب)
    if lookahead == 'ID':
        tok = lexer.tokenval # حفظ الأندكس الخاص بالمتغير الحالي قبل عمل match
        match('ID')
        rest(tok) # نمرر الأندكس لدالة rest لتحدد هل هو تخصيص أم استدعاء
        
    elif lookahead == 'IF':
        match('IF'); match('('); expr(); match(')')
        print("Pop r2\nCmp r2, 0\nBe else_label") # محاكاة القفز في الـ IF
        match('THEN'); stmt()
        
    elif lookahead == 'WHILE':
        print("while_label:")
        match('WHILE'); match('('); expr(); match(')')
        print("Pop r2\nCmp r2, 0\nBe endwhile_label")
        match('DO'); stmt()
        print("B while_label\nendwhile_label:")

    # ⚠️ [مكان إضافة أسئلة الكويزات الفجائية مثل REPEAT أو LOOP]
    # مثال لو أضاف REPEAT:
    # elif lookahead == 'REPEAT':
    #     print("repeat_label:")
    #     match('REPEAT'); cs(); match('UNTIL')
    #     match('('); expr(); match(')'); print("Pop r2\nCmp r2,0\nBne repeat_label")
    elif lookahead == 'REPEAT':
        match("REPEAT")
        emitter.rep1()
        stmt()
        match("UNTIL")
        match('(')
        expr()
        match(')')
        emitter.rep2()
    
    elif lookahead == 'DO':
        match('DO')
        emitter.do1()
        cs()
        match('UNTIL')
        match('(')
        expr()
        match(')')
        emitter.do2()
    elif lookahead == 'BEGIN':
        match('BEGIN'); cs(); match('END')
    else:
        error()

def rest(tok):
    # دالة مساعدة لحل مشكلة البداية بـ ID (تخصيص متغير = أم استدعاء دالة ())
    if lookahead == '=':
        match('='); expr()
        emitter.emit('ASSIGN', tok) # توليد أمر Pop لاسم المتغير
    elif lookahead == '(':
        match('('); match(')')
        emitter.emit('FUNCALL', tok) # توليد أمر call لاسم الدالة
    else:
        error()

def cs():
    # قائمة الجمل البرمجية المفصولة بفاصلة منقوطة
    while lookahead not in ['END', 'UNTIL', 'TO', 'EOF']:
        stmt()
        if lookahead == ';':
            match(';')
        else:
            break

# ⚠️ [دالة التعامل مع الفاينل لاب وجزء الدالات - Phase 7]
def Function():
    if lookahead == 'VOID':
        match('VOID')
        func_tok = lexer.tokenval # حفظ أندكس اسم الدالة
        match('ID')
        emitter.emit('FUNDEC', func_tok) # طباعة اسم الدالة كعنوان F1:
        match('(')
        match(')')
        match('BEGIN')
        cs()
        match('END')
        emitter.emit('FUNRET') # طباعة أمر العودة ret

def parse():
    global lookahead
    symbol.initialize()
    lookahead = lexer.lexan()
    
    # حلقة قراءة البرنامج بالكامل حتى نهاية الملف (Final Lab الهيكل الجديد)
    while lookahead != 'EOF':
        if lookahead == 'VOID':
            Function()
        else:
            stmt()

