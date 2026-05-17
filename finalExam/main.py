# main.py
import lexer
import parser
import emitter

def main():
    # 1. قراءة التعبير البرمجي من ملف المدخلات الخارجي المخصص .exp
    try:
        with open("file.exp", "r") as f:
            lexer.input_text = f.read()
    except FileNotFoundError:
        print("Error: Please create a 'file.exp' in the same folder and write your expressions.")
        return

    # 2. تشغيل المحلل والـ Parser
    print("Compilation started...")
    parser.parse()
    
    # 3. إغلاق وحفظ ملفات المخرجات .obj و .il
    emitter.close_files()
    print("Compilation successful! Check 'file.obj' and 'file.il' for outputs.")

if __name__ == "__main__":
    main()