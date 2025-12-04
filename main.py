import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from collections import deque

# MODUL 5 & 6: OOP - Class dengan Encapsulation
class Transaksi:
    def __init__(self, jenis, kategori, nominal, tanggal, catatan):
        self.__jenis = jenis
        self.__kategori = kategori
        self.__nominal = nominal
        self.__tanggal = tanggal
        self.__catatan = catatan
    
    def getJenis(self): return self.__jenis
    def getKategori(self): return self.__kategori
    def getNominal(self): return self.__nominal
    def getTanggal(self): return self.__tanggal
    def getCatatan(self): return self.__catatan

class Budget:
    def __init__(self, kategori, limit):
        self.__kategori = kategori
        self.__limit = limit
        self.__terpakai = 0
    
    def tambahPengeluaran(self, nominal):
        self.__terpakai += nominal
    
    def getKategori(self): return self.__kategori
    def getLimit(self): return self.__limit
    def getTerpakai(self): return self.__terpakai
    
    def getStatus(self):
        persentase = (self.__terpakai / self.__limit) * 100
        if persentase < 70: return "Aman"
        elif persentase < 100: return "Warning"
        else: return "Over-limit"

# MODUL 8: GUI Programming dengan Tkinter
class BudgetPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Planner Mahasiswa")
        self.root.geometry("850x650")
        self.root.configure(bg="#f0f0f0")
        
        # MODUL 1: Variabel & Tipe Data
        self.transaksi_list = []
        self.budget_dict = {}
        self.kategori_options = ["Makan", "Kos", "Transport", "Hiburan", "Lainnya"]
        
        # MODUL 7: Queue untuk riwayat transaksi terbaru
        self.riwayat_queue = deque(maxlen=5)
        
        self.current_page = "dashboard"
        self.setupUI()
    
    def setupUI(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(main_frame, text="Budget Planner Mahasiswa", 
                        font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=(0, 5))
        
        credit = tk.Label(main_frame, text="Made by: Devin Raihan Ferynaldo | NIM: 21120125140199", 
                         font=("Arial", 10), bg="#f0f0f0", fg="#666")
        credit.pack(pady=(0, 10))
        
        # Menu Navigation
        menu_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, borderwidth=2)
        menu_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_style = {"font": ("Arial", 10, "bold"), "width": 15, "cursor": "hand2", "relief": tk.FLAT}
        tk.Button(menu_frame, text="Dashboard", command=lambda: self.changePage("dashboard"), 
                 bg="#2196F3", fg="white", **btn_style).pack(side=tk.LEFT, padx=5, pady=8)
        tk.Button(menu_frame, text="Transaksi", command=lambda: self.changePage("transaksi"), 
                 bg="#4CAF50", fg="white", **btn_style).pack(side=tk.LEFT, padx=5, pady=8)
        tk.Button(menu_frame, text="Budget", command=lambda: self.changePage("budget"), 
                 bg="#FF9800", fg="white", **btn_style).pack(side=tk.LEFT, padx=5, pady=8)
        tk.Button(menu_frame, text="Laporan", command=lambda: self.changePage("laporan"), 
                 bg="#607D8B", fg="white", **btn_style).pack(side=tk.LEFT, padx=5, pady=8)
        
        # Content Frame
        self.content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.showDashboard()
    
    def clearContent(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def changePage(self, page):
        self.current_page = page
        self.clearContent()
        
        # MODUL 2: Pengkondisian untuk routing halaman
        if page == "dashboard":
            self.showDashboard()
        elif page == "transaksi":
            self.showTransaksi()
        elif page == "budget":
            self.showBudget()
        elif page == "laporan":
            self.showLaporan()
    
    def showDashboard(self):
        # Summary Frame
        summary_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, borderwidth=2)
        summary_frame.pack(fill=tk.X, pady=(0, 15))
        
        total_income = sum([t.getNominal() for t in self.transaksi_list if t.getJenis() == "Pemasukan"])
        total_expense = sum([t.getNominal() for t in self.transaksi_list if t.getJenis() == "Pengeluaran"])
        saldo = total_income - total_expense
        
        saldo_color = "blue" if saldo >= 0 else "red"
        saldo_label = tk.Label(summary_frame, text=f"Saldo: Rp {saldo:,.0f}", 
                               font=("Arial", 16, "bold"), bg="white", fg=saldo_color)
        saldo_label.grid(row=0, column=0, padx=25, pady=20)
        
        pemasukan_label = tk.Label(summary_frame, text=f"Pemasukan: Rp {total_income:,.0f}", 
                                   font=("Arial", 14), bg="white", fg="green")
        pemasukan_label.grid(row=0, column=1, padx=25, pady=20)
        
        pengeluaran_label = tk.Label(summary_frame, text=f"Pengeluaran: Rp {total_expense:,.0f}", 
                                     font=("Arial", 14), bg="white", fg="red")
        pengeluaran_label.grid(row=0, column=2, padx=25, pady=20)
        
        # Riwayat Frame
        riwayat_frame = tk.LabelFrame(self.content_frame, text="Transaksi Terbaru", 
                                     font=("Arial", 12, "bold"), bg="white", padx=15, pady=10)
        riwayat_frame.pack(fill=tk.BOTH, expand=True)
        
        # MODUL 3: Perulangan untuk menampilkan riwayat
        if len(self.riwayat_queue) == 0:
            tk.Label(riwayat_frame, text="Belum ada transaksi", 
                    font=("Arial", 10, "italic"), bg="white", fg="gray").pack(pady=20)
        else:
            for item in self.riwayat_queue:
                tk.Label(riwayat_frame, text=item, font=("Arial", 10), 
                        bg="white", anchor="w").pack(fill=tk.X, pady=3)
    
    def showTransaksi(self):
        input_frame = tk.LabelFrame(self.content_frame, text="Tambah Transaksi", 
                                   font=("Arial", 12, "bold"), bg="white", padx=20, pady=15)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(input_frame, text="Tipe:", bg="white", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        tipe_var = tk.StringVar(value="Pengeluaran")
        tipe_frame = tk.Frame(input_frame, bg="white")
        tipe_frame.grid(row=0, column=1, sticky="w", pady=5)
        tk.Radiobutton(tipe_frame, text="Pemasukan", variable=tipe_var, 
                      value="Pemasukan", bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        tk.Radiobutton(tipe_frame, text="Pengeluaran", variable=tipe_var, 
                      value="Pengeluaran", bg="white", font=("Arial", 10)).pack(side=tk.LEFT)
        
        tk.Label(input_frame, text="Jumlah (Rp):", bg="white", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        jumlah_entry = tk.Entry(input_frame, font=("Arial", 10), width=35)
        jumlah_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        tk.Label(input_frame, text="Kategori:", bg="white", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        kategori_var = tk.StringVar(value=self.kategori_options[0])
        ttk.Combobox(input_frame, textvariable=kategori_var, values=self.kategori_options, 
                    font=("Arial", 10), width=33, state="readonly").grid(row=2, column=1, sticky="w", pady=5)
        
        tk.Label(input_frame, text="Keterangan:", bg="white", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        ket_entry = tk.Entry(input_frame, font=("Arial", 10), width=35)
        ket_entry.grid(row=3, column=1, sticky="w", pady=5)
        
        def tambahTransaksi():
            # MODUL 2: Pengkondisian validasi input
            if not jumlah_entry.get():
                messagebox.showerror("Error", "Jumlah harus diisi!")
                return
            
            try:
                nominal = float(jumlah_entry.get())
                if nominal <= 0:
                    messagebox.showerror("Error", "Jumlah harus lebih dari 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "Jumlah harus berupa angka")
                return
            
            # Cek saldo jika pengeluaran
            if tipe_var.get() == "Pengeluaran":
                total_income = sum([t.getNominal() for t in self.transaksi_list if t.getJenis() == "Pemasukan"])
                total_expense = sum([t.getNominal() for t in self.transaksi_list if t.getJenis() == "Pengeluaran"])
                saldo_sekarang = total_income - total_expense
                
                if nominal > saldo_sekarang:
                    messagebox.showerror("Error", f"Saldo tidak cukup!\nSaldo saat ini: Rp {saldo_sekarang:,.0f}\nPengeluaran: Rp {nominal:,.0f}")
                    return
            
            tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")
            trans = Transaksi(tipe_var.get(), kategori_var.get(), nominal, tanggal, ket_entry.get())
            self.transaksi_list.append(trans)
            
            # Cek dan update budget jika pengeluaran
            pesan_budget = ""
            if tipe_var.get() == "Pengeluaran" and kategori_var.get() in self.budget_dict:
                budget = self.budget_dict[kategori_var.get()]
                budget.tambahPengeluaran(nominal)
                
                # Cek status budget setelah pengeluaran
                if budget.getStatus() == "Over-limit":
                    pesan_budget = f"\n\n⚠️ PERINGATAN: Budget {kategori_var.get()} melebihi batas!\nTerpakai: Rp {budget.getTerpakai():,.0f}\nLimit: Rp {budget.getLimit():,.0f}"
                elif budget.getStatus() == "Warning":
                    pesan_budget = f"\n\n⚠️ Budget {kategori_var.get()} hampir habis!\nTerpakai: Rp {budget.getTerpakai():,.0f}\nLimit: Rp {budget.getLimit():,.0f}"
            
            self.riwayat_queue.append(f"{tanggal} | {tipe_var.get()} | {kategori_var.get()} | Rp {nominal:,.0f}")
            
            messagebox.showinfo("Sukses", f"Transaksi berhasil ditambahkan!{pesan_budget}")
            jumlah_entry.delete(0, tk.END)
            ket_entry.delete(0, tk.END)
            updateTable()
        
        btn_frame = tk.Frame(input_frame, bg="white")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Tambah", command=tambahTransaksi, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                 width=15, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # Tabel Frame
        table_frame = tk.LabelFrame(self.content_frame, text="Riwayat Transaksi", 
                                   font=("Arial", 12, "bold"), bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Tanggal", "Tipe", "Jumlah", "Kategori", "Keterangan")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        def updateTable():
            for item in tree.get_children():
                tree.delete(item)
            for t in self.transaksi_list:
                tree.insert("", tk.END, values=(t.getTanggal(), t.getJenis(), 
                           f"Rp {t.getNominal():,.0f}", t.getKategori(), t.getCatatan()))
        
        def hapusTransaksi():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Peringatan", "Pilih transaksi yang ingin dihapus")
                return
            if messagebox.askyesno("Konfirmasi", "Hapus transaksi yang dipilih?"):
                index = tree.index(selected[0])
                del self.transaksi_list[index]
                updateTable()
                messagebox.showinfo("Sukses", "Transaksi berhasil dihapus")
        
        tk.Button(table_frame, text="Hapus Transaksi", command=hapusTransaksi,
                 bg="#ff9800", fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2").pack(pady=5)
        
        updateTable()
    
    def showBudget(self):
        input_frame = tk.LabelFrame(self.content_frame, text="Set Budget Kategori", 
                                   font=("Arial", 12, "bold"), bg="white", padx=20, pady=15)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(input_frame, text="Kategori:", bg="white", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        kategori_var = tk.StringVar(value=self.kategori_options[0])
        ttk.Combobox(input_frame, textvariable=kategori_var, values=self.kategori_options, 
                    font=("Arial", 10), width=33, state="readonly").grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(input_frame, text="Limit Budget (Rp):", bg="white", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        limit_entry = tk.Entry(input_frame, font=("Arial", 10), width=35)
        limit_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        list_frame = tk.LabelFrame(self.content_frame, text="Daftar Budget", 
                                  font=("Arial", 12, "bold"), bg="white", padx=15, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        def setBudget():
            if not limit_entry.get():
                messagebox.showwarning("Peringatan", "Limit budget wajib diisi!")
                return
            try:
                limit = float(limit_entry.get())
                if limit <= 0:
                    messagebox.showerror("Error", "Limit harus lebih dari 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "Limit harus berupa angka")
                return
            
            # Hitung pengeluaran yang sudah ada untuk kategori ini
            total_pengeluaran = sum([t.getNominal() for t in self.transaksi_list 
                                    if t.getJenis() == "Pengeluaran" and t.getKategori() == kategori_var.get()])
            
            new_budget = Budget(kategori_var.get(), limit)
            if total_pengeluaran > 0:
                new_budget.tambahPengeluaran(total_pengeluaran)
            
            self.budget_dict[kategori_var.get()] = new_budget
            messagebox.showinfo("Sukses", f"Budget {kategori_var.get()} berhasil dibuat!")
            limit_entry.delete(0, tk.END)
            tampilListBudget()
        
        tk.Button(input_frame, text="Set Budget", command=setBudget, 
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"), 
                 width=15, cursor="hand2").grid(row=2, column=0, columnspan=2, pady=10)
        
        def tampilListBudget():
            for widget in list_frame.winfo_children():
                widget.destroy()
            
            if len(self.budget_dict) == 0:
                tk.Label(list_frame, text="Belum ada budget", 
                        font=("Arial", 10, "italic"), bg="white", fg="gray").pack(pady=20)
            else:
                for kategori, budget in self.budget_dict.items():
                    status = budget.getStatus()
                    color = "green" if status == "Aman" else "orange" if status == "Warning" else "red"
                    
                    budget_frame = tk.Frame(list_frame, bg="white")
                    budget_frame.pack(fill=tk.X, pady=5)
                    
                    tk.Label(budget_frame, 
                            text=f"{kategori}: Rp {budget.getTerpakai():,.0f} / Rp {budget.getLimit():,.0f} [{status}]", 
                            fg=color, font=("Arial", 11), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
                    
                    def hapusBudget(kat=kategori):
                        if messagebox.askyesno("Konfirmasi", f"Hapus budget {kat}?"):
                            del self.budget_dict[kat]
                            tampilListBudget()
                            messagebox.showinfo("Sukses", f"Budget {kat} berhasil dihapus!")
                    
                    tk.Button(budget_frame, text="Hapus", command=hapusBudget, 
                             bg="#f44336", fg="white", font=("Arial", 9), width=8).pack(side=tk.RIGHT, padx=5)
        
        tampilListBudget()
    
    def showLaporan(self):
        laporan_frame = tk.LabelFrame(self.content_frame, text="Laporan Keuangan", 
                                     font=("Arial", 12, "bold"), bg="white", padx=20, pady=15)
        laporan_frame.pack(fill=tk.BOTH, expand=True)
        
        expense_per_kategori = {}
        for t in self.transaksi_list:
            if t.getJenis() == "Pengeluaran":
                kategori = t.getKategori()
                if kategori in expense_per_kategori:
                    expense_per_kategori[kategori] += t.getNominal()
                else:
                    expense_per_kategori[kategori] = t.getNominal()
        
        tk.Label(laporan_frame, text="Pengeluaran per Kategori:", 
                font=("Arial", 12, "bold"), bg="white").pack(pady=10, anchor="w")
        
        if len(expense_per_kategori) == 0:
            tk.Label(laporan_frame, text="Belum ada data pengeluaran", 
                    font=("Arial", 10, "italic"), bg="white", fg="gray").pack(pady=20)
        else:
            for kategori, total in expense_per_kategori.items():
                tk.Label(laporan_frame, text=f"{kategori}: Rp {total:,.0f}", 
                        font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetPlannerApp(root)
    root.mainloop()