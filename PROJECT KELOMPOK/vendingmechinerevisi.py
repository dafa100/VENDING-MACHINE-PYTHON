import tkinter as tk
import time, os

MULTITAP = {
    "1": ["1", "a", "b", "c"],
    "2": ["2", "d", "e", "f"],
    "3": ["3", "g", "h", "i"],
    "4": ["4", "j", "k", "l"],
    "5": ["5", "m", "n", "o"],
    "6": ["6", "p", "q", "r"],
    "7": ["7", "s", "t", "u"],
    "8": ["8", "v", "w", "x"],
    "9": ["9", "x", "y", "z"],
    "0": ["0"],
}

PRODUCTS = [
    ("01", "Air mineral", 3000,  "01.png"),
    ("02", "Orange Juice", 6000, "02.png"),
    ("03", "Yoghurt", 5000,      "03.png"),
    ("04", "Chiki Balls", 10000, "04.png"),
    ("05", "Doritos", 12000,     "05.png"),
    ("06", "Chocopie", 5000,     "06.png"),
    ("07", "Oreo", 8000,         "07.png"),
    ("08", "Crackers", 12000,    "08.png"),
    ("09", "Popcorn", 14000,     "09.png"),
    ("10", "Coffee", 4000,       "10.png"),
    ("11", "Pepsi", 25000,       "11.png"),
    ("12", "Milk", 15000,        "12.png"),
]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine")

        self.text = tk.StringVar()
        self.msg = tk.StringVar()
        self.last_key = None
        self.last_time = 0
        self.tap = 0
        self.timeout = 0.8

        self.items = {}
        self.images = []

        main = tk.Frame(root, bg="#0b2b3f")
        main.pack(fill="both", expand=True)

        left = tk.Frame(main, bg="#123953", padx=20, pady=20)
        left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(main, bg="#0b2b3f", padx=40, pady=40)
        right.pack(side="right", fill="y")

        self.build_products(left)
        self.build_panel(right)

    def build_products(self, parent):
        for i, (code, name, price, imgfile) in enumerate(PRODUCTS):
            r, c = divmod(i, 3)
            card = tk.Frame(parent, bg="#f0f0f0", bd=2, relief="ridge", padx=8, pady=8)
            card.grid(row=r, column=c, padx=10, pady=10)

            img = None
            if os.path.exists(imgfile):
                try:
                    img = tk.PhotoImage(file=imgfile)
                except:  # file rusak dll
                    img = None
            if img:
                self.images.append(img)
                tk.Label(card, image=img, bg="#f0f0f0").pack()
            else:
                tk.Label(card, text="No Image", width=12, height=6, bg="#ccc").pack()

            tk.Label(card, text=code, font=("Arial", 9, "bold"), bg="#f0f0f0").pack()
            tk.Label(card, text=name, font=("Arial", 9), bg="#f0f0f0").pack()
            tk.Label(card, text=f"Rp {price:,}".replace(",", "."),
                     font=("Arial", 9), bg="#f0f0f0").pack()

            stok_var = tk.StringVar(value="99")
            tk.Label(card, textvariable=stok_var, font=("Arial", 9), bg="#f0f0f0").pack()

            self.items[code] = {"name": name, "price": price, "stock": 99, "stok_var": stok_var}

    def build_panel(self, parent):
        monitor = tk.Frame(parent, bg="black", padx=20, pady=20)
        monitor.pack(fill="x", pady=(0, 30))

        for t in ["SELAMAT DATANG", "1. ADMIN", "2. BELANJA"]:
            tk.Label(monitor, text=t, fg="white", bg="black",
                     font=("Arial", 12 if "SELAMAT" in t else 10, "bold" if "SELAMAT" in t else "normal")
                     ).pack(anchor="w")

        tk.Label(monitor, text=" ", bg="black").pack()
        tk.Label(monitor, text="INPUT:", fg="white", bg="black",
                 font=("Arial", 10)).pack(anchor="w")
        tk.Label(monitor, textvariable=self.text, fg="white", bg="black",
                 font=("Consolas", 13)).pack(anchor="w")
        tk.Label(monitor, textvariable=self.msg, fg="white", bg="black",
                 font=("Arial", 9), wraplength=220, justify="left").pack(anchor="w", pady=(5, 0))

        outer = tk.Frame(parent, bg="#d9d9d9", padx=10, pady=10)
        outer.pack()
        pad = tk.Frame(outer, bg="#d9d9d9")
        pad.pack()

        keys = [
            ("1", "abc"), ("2", "def"), ("3", "ghi"),
            ("4", "jkl"), ("5", "mno"), ("6", "pqr"),
            ("7", "stu"), ("8", "vwx"), ("9", "xyz"),
            ("X", ""),    ("0", ""),    ("OK", "")
        ]

        r = c = 0
        for key, letters in keys:
            if key in MULTITAP:
                text = f"{key}\n{letters}"
                bg, fg = "#222", "white"
            elif key == "X":
                text, bg, fg = "X", "#f33", "white"
            else:
                text, bg, fg = "OK", "#f8a52b", "white"

            tk.Button(
                pad, text=text, width=4, height=2, bg=bg, fg=fg,
                font=("Arial", 10, "bold"), relief="flat",
                command=lambda k=key: self.handle_key(k)
            ).grid(row=r, column=c, padx=4, pady=4)

            c += 1
            if c > 2:
                c = 0
                r += 1

    def handle_key(self, key):
        self.msg.set("")
        if key == "OK":
            self.buy()
            return
        if key == "X":
            cur = self.text.get()
            if cur:
                self.text.set(cur[:-1])  # hapus 1 karakter terakhir
            self.last_key = None
            self.tap = 0
            return
        if key not in MULTITAP:
            self.text.set(self.text.get() + key)
            return

        now = time.time()
        same = (key == self.last_key and now - self.last_time < self.timeout)
        self.tap = self.tap + 1 if same else 0
        self.last_key, self.last_time = key, now

        chars = MULTITAP[key]
        ch = chars[self.tap % len(chars)]
        cur = self.text.get()
        if same and cur:
            cur = cur[:-1]
        self.text.set(cur + ch)

    def buy(self):
        code = self.text.get().strip()
        if code not in self.items:
            self.msg.set("Kode tidak valid.")
            return
        item = self.items[code]
        if item["stock"] <= 0:
            self.msg.set("Stok habis.")
            return
        item["stock"] -= 1
        item["stok_var"].set(f"Stok : {item['stock']}")
        self.msg.set(f"Anda membeli {item['name']} (Rp {item['price']:,})".replace(",", "."))
        self.text.set("")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()