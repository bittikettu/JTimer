import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ckilpailija import kilpailija

class ParticipantEditor(tk.Toplevel):
    def __init__(self, parent, competitors, update_callback):
        super().__init__(parent)
        self.title("Participant Editor")
        self.geometry("800x600")
        self.competitors = competitors
        self.update_callback = update_callback

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Main container
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Treeview for participants
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        columns = ("bib", "firstname", "lastname", "club", "series")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        self.tree.heading("bib", text="Bib #")
        self.tree.heading("firstname", text="First Name")
        self.tree.heading("lastname", text="Last Name")
        self.tree.heading("club", text="Club")
        self.tree.heading("series", text="Series")
        
        self.tree.column("bib", width=50)
        self.tree.column("firstname", width=100)
        self.tree.column("lastname", width=100)
        self.tree.column("club", width=100)
        self.tree.column("series", width=50)

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Input fields
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Participant Details", padding="10")
        self.input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        ttk.Label(self.input_frame, text="Bib #:").grid(row=0, column=0, padx=5, pady=5)
        self.bib_var = tk.StringVar()
        self.bib_entry = ttk.Entry(self.input_frame, textvariable=self.bib_var)
        self.bib_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="First Name:").grid(row=0, column=2, padx=5, pady=5)
        self.fname_var = tk.StringVar()
        self.fname_entry = ttk.Entry(self.input_frame, textvariable=self.fname_var)
        self.fname_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Last Name:").grid(row=0, column=4, padx=5, pady=5)
        self.lname_var = tk.StringVar()
        self.lname_entry = ttk.Entry(self.input_frame, textvariable=self.lname_var)
        self.lname_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Club:").grid(row=1, column=0, padx=5, pady=5)
        self.club_var = tk.StringVar()
        self.club_entry = ttk.Entry(self.input_frame, textvariable=self.club_var)
        self.club_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Series:").grid(row=1, column=2, padx=5, pady=5)
        self.series_var = tk.StringVar()
        self.series_entry = ttk.Entry(self.input_frame, textvariable=self.series_var)
        self.series_entry.grid(row=1, column=3, padx=5, pady=5)

        # Buttons
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(self.btn_frame, text="New", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Save/Update", command=self.save_participant).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Delete", command=self.delete_participant).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Close", command=self.destroy).pack(side=tk.LEFT, padx=5)

        self.refresh_list()

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for comp in self.competitors:
            self.tree.insert("", tk.END, values=(comp.bibnumber, comp.etunimi, comp.sukunimi, comp.seura, comp.kilpasarja))

    def on_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        item = self.tree.item(selected_items[0])
        values = item['values']
        
        if values:
            self.bib_var.set(values[0])
            self.fname_var.set(values[1])
            self.lname_var.set(values[2])
            self.club_var.set(values[3])
            self.series_var.set(values[4])

    def clear_form(self):
        self.bib_var.set("")
        self.fname_var.set("")
        self.lname_var.set("")
        self.club_var.set("")
        self.series_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def save_participant(self):
        bib = self.bib_var.get()
        if not bib:
            messagebox.showerror("Error", "Bib number is required")
            return

        # Check if updating existing
        existing = None
        for comp in self.competitors:
            if str(comp.bibnumber) == str(bib):
                existing = comp
                break
        
        if existing:
            existing.etunimi = self.fname_var.get()
            existing.sukunimi = self.lname_var.get()
            existing.seura = self.club_var.get()
            existing.kilpasarja = self.series_var.get()
            messagebox.showinfo("Success", "Participant updated")
        else:
            new_comp = kilpailija(
                self.fname_var.get(),
                self.lname_var.get(),
                "", # Phone
                self.club_var.get(),
                self.series_var.get(),
                bib
            )
            self.competitors.append(new_comp)
            messagebox.showinfo("Success", "Participant added")
        
        self.refresh_list()
        if self.update_callback:
            self.update_callback()

    def delete_participant(self):
        bib = self.bib_var.get()
        if not bib:
            return

        for i, comp in enumerate(self.competitors):
            if str(comp.bibnumber) == str(bib):
                del self.competitors[i]
                self.clear_form()
                self.refresh_list()
                if self.update_callback:
                    self.update_callback()
                messagebox.showinfo("Success", "Participant deleted")
                return
        
        messagebox.showerror("Error", "Participant not found")
