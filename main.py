import sys

# تعريف الرموز (Tokens)
NUM = 256 # تعريف NUM خارج نطاق ASCII [cite: 733]

# المتغيرات العامة
input_text = "150 + 20 - 5" # مثال لمدخل يحتوي مسافات وأرقام متعددة الخانات [cite: 656]
input_index = 0
lookahead = None
tokenval = None # يحتوي على قيمة الرقم الفعلي [cite: 735]
lineno = 1      # تتبع رقم السطر للأخطاء [cite: 686]

def lexan():
    global input_text, input_index, tokenval, lineno
    
    while True:
        # التحقق من نهاية النص
        if input_index >= len(input_text):
            return 'EOF'
        
        t = input_text[input_index]
        input_index += 1

        # 1. تجاهل المسافات والتبويب [cite: 696, 745]
        if t == ' ' or t == '\t':
            continue
        
        # 2. تتبع رقم السطر عند وجود سطر جديد [cite: 697, 746]
        elif t == '\n':
            lineno += 1
            continue
        
        # 3. معالجة الأرقام (خانات متعددة) [cite: 748]
        elif t.isdigit():
            number_str = t
            # الاستمرار في القراءة طالما الرمز التالي رقم
            while input_index < len(input_text) and input_text[input_index].isdigit():
                number_str += input_text[input_index]
                input_index += 1
            
            tokenval = int(number_str) # تخزين قيمة الرقم [cite: 751]
            return NUM # إرجاع الرمز NUM [cite: 752]
        
        # 4. إرجاع الرموز الأخرى (+, -)
        else:
            return t

def error():
    print(f"\nsyntax error at line {lineno}") # استخدام رقم السطر في رسالة الخطأ [cite: 564]
    sys.exit(1)

def match(token):
    global lookahead
    if lookahead == token:
        lookahead = lexan()
    else:
        error()

def term():
    global lookahead, tokenval
    # تحديث قاعدة term لتقبل NUM [cite: 723, 760]
    if lookahead == NUM:
        print(tokenval, end=' ') # طباعة قيمة الرقم الفعلي [cite: 764]
        match(NUM)
    else:
        error()

def rest():
    global lookahead
    while True:
        if lookahead == '+':
            match('+')
            term()
            print('+', end=' ')
        elif lookahead == '-':
            match('-')
            term()
            print('-', end=' ')
        else:
            break

def expr():
    term()
    rest()

def main():
    global lookahead
    lookahead = lexan()
    expr()
    print(f"\nParsing completed successfully (Lines processed: {lineno})")

if __name__ == "__main__":
    main()