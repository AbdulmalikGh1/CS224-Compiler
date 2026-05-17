# lexer.py
import symbol

input_text = ""
input_index = 0
tokenval = None  # يحتوي على القيمة العددية أو أندكس المتغير في جدول الرموز
lineno = 1

def lexan():
    global input_index, tokenval, lineno
    
    while True:
        if input_index >= len(input_text):
            return 'EOF'
            
        t = input_text[input_index]
        input_index += 1
        
        if t == ' ' or t == '\t':
            continue
            
        elif t == '\n':
            lineno += 1
            continue
            
        elif t.isdigit():
            num_str = t
            while input_index < len(input_text) and input_text[input_index].isdigit():
                num_str += input_text[input_index]
                input_index += 1
            tokenval = int(num_str)
            return 'NUM'
            
        elif t.isalpha():
            id_str = t
            while input_index < len(input_text) and input_text[input_index].isalnum():
                id_str += input_text[input_index]
                input_index += 1
                
            # البحث في جدول الرموز (هل هي كلمة محجوزة أم متغير جديد؟)
            p = symbol.lookup(id_str)
            if p is None:
                p = symbol.insert(id_str, 'ID')
                
            tokenval = p  # تخزين أندكس الرمز في الـ tokenval
            return symbol.symbol_table[p].token
            
        else:
            return t