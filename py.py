import tkinter as tk
import math

class Calculator:
    def __init__(self, master):
        self.master = master
    
    

        master.title("ماشین حساب")
        master.geometry("500x600") # اندازه تقریبی پنجره
        master.resizable(False, False) # غیرفعال کردن تغییر اندازه پنجره
        master.configure(bg="#2196F3") # رنگ پس‌زمینه آبی برای قسمت بالای ماشین حساب

        self.current_expression = "" # برای ذخیره عبارت فعلی
        self.result_displayed = False # برای بررسی اینکه آیا نتیجه ای نمایش داده شده است یا خیر

        # کادر نمایش
        self.display_frame = tk.Frame(master, bg="#2196F3")
        self.display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", ipady=20)
        master.grid_rowconfigure(0, weight=1) # برای اینکه کادر نمایش فضای بیشتری بگیرد

        self.display = tk.Entry(self.display_frame, width=20, borderwidth=0, font=('Arial', 32),
                                bg="#2196F3", fg="white", justify='right')
        self.display.pack(expand=True, fill="both", padx=10, pady=10) # استفاده از pack برای مرکزی کردن و گسترش

        # فریم دکمه ها
        self.button_frame = tk.Frame(master, bg="lightgray")
        self.button_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")
        for i in range(6): # 6 سطر دکمه داریم
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4): # 4 ستون دکمه داریم
            self.button_frame.grid_columnconfigure(i, weight=1)

        # تعریف سبک دکمه ها
        button_font = ('Arial', 18, 'bold')
        button_padx = 15
        button_pady = 15

        # دکمه های علمی (سبز)
        self.create_button("π", 0, 0, command=self.add_pi, bg="#4CAF50", fg="white", font=button_font, padx=button_padx, pady=button_pady)
        self.create_button("x²", 0, 1, command=self.power_of_2, bg="#4CAF50", fg="white", font=button_font, padx=button_padx, pady=button_pady)
        self.create_button("√", 0, 2, command=self.square_root, bg="#4CAF50", fg="white", font=button_font, padx=button_padx, pady=button_pady)
        self.create_button("1/x", 0, 3, command=self.inverse, bg="#4CAF50", fg="white", font=button_font, padx=button_padx, pady=button_pady)

        # ردیف C و عملگرها
        self.create_button("C", 1, 0, command=self.clear, bg="#F44336", fg="white", font=button_font, padx=button_padx, pady=button_pady)
        self.create_button("%", 1, 1, command=lambda: self.add_to_expression("%"), bg="#9E9E9E", fg="black", font=button_font, padx=button_padx, pady=button_pady)
        self.create_button("+/-", 1, 2, command=self.toggle_sign, bg="#9E9E9E", fg="black", font=button_font, padx=button_padx, pady=button_pady)
        self.create_button("÷", 1, 3, command=lambda: self.add_to_expression("/"), bg="#9E9E9E", fg="black", font=button_font, padx=button_padx, pady=button_pady)

        # دکمه های اعداد 7، 8، 9 و ضرب
        self.create_button("7", 2, 0)
        self.create_button("8", 2, 1)
        self.create_button("9", 2, 2)
        self.create_button("×", 2, 3, command=lambda: self.add_to_expression("*"), bg="#9E9E9E", fg="black", font=button_font, padx=button_padx, pady=button_pady)

        # دکمه های اعداد 4، 5، 6 و منها
        self.create_button("4", 3, 0)
        self.create_button("5", 3, 1)
        self.create_button("6", 3, 2)
        self.create_button("-", 3, 3, command=lambda: self.add_to_expression("-"), bg="#9E9E9E", fg="black", font=button_font, padx=button_padx, pady=button_pady)

        # دکمه های اعداد 1، 2، 3 و جمع
        self.create_button("1", 4, 0)
        self.create_button("2", 4, 1)
        self.create_button("3", 4, 2)
        self.create_button("+", 4, 3, command=lambda: self.add_to_expression("+"), bg="#9E9E9E", fg="black", font=button_font, padx=button_padx, pady=button_pady)

        # دکمه های 0، اعشار، بک اسپیس و مساوی
        self.create_button("0", 5, 0)
        self.create_button(".", 5, 1)
        self.create_button("⌫", 5, 2, command=self.backspace, bg="#9E9E9E", fg="black", font=button_font, padx=button_padx, pady=button_pady)
        self.create_button("=", 5, 3, command=self.calculate, bg="#FFC107", fg="black", font=button_font, padx=button_padx, pady=button_pady)

    def create_button(self, text, row, column, columnspan=1, command=None, bg="white", fg="black", font=('Arial', 18, 'bold'), padx=15, pady=15):
        # اگر command تعریف نشده بود، به صورت پیش‌فرض اعداد و نقطه رو به current_expression اضافه کنه
        if command is None:
            command = lambda: self.add_to_expression(text)

        button = tk.Button(self.button_frame, text=text, font=font, bg=bg, fg=fg,
                           command=command, relief="flat", bd=1, highlightbackground="lightgray")
        button.grid(row=row, column=column, columnspan=columnspan, sticky="nsew", padx=2, pady=2)

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_expression)

    def add_to_expression(self, char):
        if self.result_displayed: # اگر یک نتیجه نمایش داده شده، با شروع ورودی جدید پاکش کن
            self.current_expression = ""
            self.result_displayed = False
        
        # جلوگیری از وارد کردن چند نقطه اعشار متوالی در یک عدد
        if char == '.' and '.' in self.current_expression.split(" ")[-1]:
            return
            
        self.current_expression += str(char)
        self.update_display()

    def clear(self):
        self.current_expression = ""
        self.update_display()
        self.result_displayed = False

    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_display()
        self.result_displayed = False

    def calculate(self):
        try:
            # جایگزینی عملگرهای خاص با عملگرهای پایتون
            expression = self.current_expression.replace("÷", "/").replace("×", "*").replace("%", "/100*")
            result = eval(expression)
            self.current_expression = str(result)
            self.update_display()
            self.result_displayed = True
        except Exception:
            self.current_expression = "Error"
            self.update_display()
            self.result_displayed = True

    def add_pi(self):
        if self.result_displayed:
            self.current_expression = ""
            self.result_displayed = False
        self.current_expression += str(math.pi)
        self.update_display()

    def power_of_2(self):
        try:
            num = float(self.current_expression)
            self.current_expression = str(num ** 2)
            self.update_display()
            self.result_displayed = True
        except ValueError:
            self.current_expression = "Error"
            self.update_display()
            self.result_displayed = True

    def square_root(self):
        try:
            num = float(self.current_expression)
            if num < 0:
                self.current_expression = "Error"
            else:
                self.current_expression = str(math.sqrt(num))
            self.update_display()
            self.result_displayed = True
        except ValueError:
            self.current_expression = "Error"
            self.update_display()
            self.result_displayed = True

    def inverse(self):
        try:
            num = float(self.current_expression)
            if num == 0:
                self.current_expression = "Error"
            else:
                self.current_expression = str(1 / num)
            self.update_display()
            self.result_displayed = True
        except ValueError:
            self.current_expression = "Error"
            self.update_display()
            self.result_displayed = True
            
    def toggle_sign(self):
        try:
            # ابتدا بررسی میکنیم آیا آخرین ورودی یک عدد هست یا نه
            parts = self.current_expression.split()
            if parts:
                last_part = parts[-1]
                if last_part.replace('.', '', 1).isdigit() or (last_part.startswith('-') and last_part[1:].replace('.', '', 1).isdigit()):
                    num = float(last_part)
                    new_num = -num
                    self.current_expression = self.current_expression.rsplit(last_part, 1)[0] + str(new_num)
                    self.update_display()
                    self.result_displayed = False # علامت عوض شد، هنوز محاسبه نهایی نیست
        except ValueError:
            self.current_expression = "Error"
            self.update_display()
            self.result_displayed = True


root = tk.Tk()
my_calculator = Calculator(root)
root.mainloop()