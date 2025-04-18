# scanner_gui.py
import difflib
from scanner import TOKEN_TYPES
import customtkinter as ctk
from tkinter import messagebox
from scanner import analyze_code, write_tokens_to_file

saved_file_label = None  # دا هنستخدمه تحت عشان نحدث الرسالة

def get_color_for_token_type(token_type):
    appearance = ctk.get_appearance_mode()
    is_dark = appearance == "Dark"

    colors = {
        "Keyword": "#0066cc" if not is_dark else "#66b3ff",
        "Identifier": "#000000" if not is_dark else "#ffffff",
        "Number": "#228B22" if not is_dark else "#7CFC00",
        "DataType": "#8A2BE2" if not is_dark else "#D8BFD8",
        "Operator": "#ff8c00" if not is_dark else "#ffd280",
        "Assignment": "#ff8c00" if not is_dark else "#ffd280",
        "Equality": "#ff8c00" if not is_dark else "#ffd280",
        "Semicolon": "#999999",
        "Unknown": "#ff0000"
    }

    return colors.get(token_type, "#000000")


# إعداد الواجهة
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title("Python Scanner - GUI")
app.geometry("900x700")



# Frame لإدخال الكود
input_frame = ctk.CTkFrame(app, width=850)
input_frame.pack(pady=(20, 10))

# Frame للأزرار
buttons_frame = ctk.CTkFrame(app, width=850)
buttons_frame.pack(pady=(5, 10))

# Frame لعرض النتائج
output_frame = ctk.CTkFrame(app, width=850)
output_frame.pack(pady=(10, 5))
 

# صندوق إدخال الكود

input_box = ctk.CTkTextbox(input_frame, width=800, height=200, corner_radius=12, font=("Consolas", 14))
input_box.pack(padx=10, pady=10)

# صندوق عرض النتائج
output_box = ctk.CTkTextbox(output_frame, width=800, height=250, corner_radius=12, font=("Consolas", 13), state="disabled")
output_box.pack(padx=10, pady=(10, 5))


# تحليل الكود
def analyze():
    code = input_box.get("1.0", "end-1c")
    if not code.strip():
        messagebox.showwarning("تحذير", "من فضلك أدخل الكود أولاً")
        return

    tokens = analyze_code(code)

    # تهيئة الصندوق
    output_box.configure(state="normal")
    output_box.delete("1.0", "end")
    

    
    for i, token in enumerate(tokens):
        tag_name = f"tag{i}"
        token_text = str(token) + "\n"
        output_box.insert("end", token_text, tag_name)
        output_box.tag_config(tag_name, foreground=get_color_for_token_type(token.type))
        
        saved_file_label = ctk.CTkLabel(app, text="", font=("Arial", 12), text_color="green")
        saved_file_label.pack(pady=(0, 10))


    output_box.configure(state="disabled")

    # حفظ التوكنز في ملف تلقائي
    first_word = code.strip().split()[0] if code.strip() else "output"
    file_name = write_tokens_to_file(tokens, base_name=first_word)
    messagebox.showinfo("تم الحفظ", f"تم حفظ التوكنز في:\n{file_name}")


# زر التحليل
analyze_button = ctk.CTkButton(buttons_frame, text="🔍 تحليل الكود", command=analyze, corner_radius=10, width=180)
analyze_button.pack(side="left", padx=10)

# زر المسح
def clear():
    input_box.delete("1.0", "end")
    output_box.configure(state="normal")
    output_box.delete("1.0", "end")
    output_box.configure(state="disabled")

clear_button = ctk.CTkButton(buttons_frame, text="🗑️ مسح الكل", command=clear, corner_radius=10, width=180)
clear_button.pack(side="left", padx=10)

# تبديل الوضع
def toggle_mode():
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("Dark" if current == "Light" else "Light")

mode_button = ctk.CTkButton(buttons_frame, text="🌓 الوضع", command=toggle_mode, corner_radius=10, width=180)
mode_button.pack(side="left", padx=10)


def show_errors():
    code = input_box.get("1.0", "end-1c")
    tokens = analyze_code(code)

    error_lines = []
    for token in tokens:
        if token.type == "Unknown":
            suggestion = difflib.get_close_matches(token.value, TOKEN_TYPES.keys(), n=1)
            suggested_word = suggestion[0] if suggestion else "لا يوجد اقتراح"
            error_lines.append(f"السطر {token.line}:\n- ❌ '{token.value}' → هل تقصد: '{suggested_word}'؟")

    if not error_lines:
        messagebox.showinfo("لا يوجد أخطاء", "✅ الكود لا يحتوي على أخطاء معروفة.")
        return
  
   

    # إنشاء popup جديدة
    popup = ctk.CTkToplevel(app)
    popup.title("الأخطاء والاقتراحات")
    popup.geometry("500x400")

    label = ctk.CTkLabel(popup, text="🧠 الأخطاء التي تم العثور عليها:", font=("Arial", 16))
    label.pack(pady=10)

    error_textbox = ctk.CTkTextbox(popup, width=460, height=300, corner_radius=10, font=("Consolas", 13))
    error_textbox.pack(padx=10, pady=10)
    error_textbox.insert("end", "\n\n".join(error_lines))
    error_textbox.configure(state="disabled")
    
    


error_button = ctk.CTkButton(buttons_frame, text="❗ عرض الأخطاء", command=show_errors, corner_radius=10, width=180)
error_button.pack(side="left", padx=10)






# تشغيل التطبيق
app.mainloop()
