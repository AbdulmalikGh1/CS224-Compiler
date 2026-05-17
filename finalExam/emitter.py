# emitter.py
import symbol

# إنشاء ملفات المخرجات كما هو مطلوب في Phase 3 و Phase 5
output_postfix = open("file.obj", "w")
output_inter = open("file.il", "w")

def emit(token, attribute=None):
    # 🌟 [قسم التحسين - OPTIMIZATION] 🌟
    # إذا طلب الدكتور كود محسن بدلاً من المعتاد، يمكنك تغيير نصوص الـ write هنا مباشرة
    
    if token == '+':
        output_postfix.write('+ ')
        output_inter.write("Pop r1\nPop r2\nAdd r2, r1\nPush r2\n")
        
    elif token == '-':
        output_postfix.write('- ')
        output_inter.write("Pop r1\nPop r2\nSub r2, r1\nPush r2\n")
        
    elif token == '*':
        output_postfix.write('* ')
        output_inter.write("Pop r1\nPop r2\nMult r2, r1\nPush r2\n")
        
    elif token == '/':
        output_postfix.write('/ ')
        output_inter.write("Pop r1\nPop r2\nDiv r2, r1\nPush r2\n")
        
    elif token == 'NUM':
        output_postfix.write(f"{attribute} ")
        output_inter.write(f"Push {attribute}\n")
        
    elif token == 'ID':
        # جلب اسم المتغير الفعلي من جدول الرموز باستخدام الأندكس
        lexeme = symbol.symbol_table[attribute].string
        output_postfix.write(f"{lexeme} ")
        output_inter.write(f"Push {lexeme}\n")
        
    elif token == 'ASSIGN':
        lexeme = symbol.symbol_table[attribute].string
        output_inter.write(f"Pop {lexeme}\n")

    # ⚠️ [مكان إضافة الأفعال الدلالية للدالات أو الأدوات الجديدة]
    elif token == 'FUNDEC': # تعريف دالة
        lexeme = symbol.symbol_table[attribute].string
        output_inter.write(f"{lexeme}:\n")
        
    elif token == 'FUNRET': # عودة من دالة
        output_inter.write("ret\n")
        
    elif token == 'FUNCALL': # استدعاء دالة
        lexeme = symbol.symbol_table[attribute].string
        output_inter.write(f"call {lexeme}\n")

def close_files():
    output_postfix.close()
    output_inter.close()

def rep1():
    output_inter.write("repeat:\n")
def rep2():
    output_inter.write("pop r2\ncmp r2,0\nbne repeat\n")

def do1():
    output_inter.write("do:\n")

def do2():
    output_inter.write("pop r2\ncmp r2,0\nbne do\n") 