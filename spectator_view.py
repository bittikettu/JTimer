import tkinter as tk
from tkinter import ttk

class SpectatorView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("JTimer - Spectator View")
        self.geometry("800x600")
        
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Header
        self.header = ttk.Label(self, text="JTimer Live", font=("Helvetica", 24, "bold"))
        self.header.grid(row=0, column=0, pady=10)
        
        # Timer
        self.time_var = tk.StringVar(value="00:00:00")
        self.timer_label = ttk.Label(self, textvariable=self.time_var, font=("Courier", 80, "bold"), foreground="#00ff00")
        self.timer_label.grid(row=1, column=0, pady=20)
        
        # Recent Finishers
        self.recent_frame = ttk.LabelFrame(self, text="Recent Finishers", padding="10")
        self.recent_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        self.recent_frame.columnconfigure(0, weight=1)
        
        self.recent_tree = ttk.Treeview(self.recent_frame, columns=("rank", "class", "name", "time"), show="headings", height=5)
        self.recent_tree.heading("rank", text="Rank")
        self.recent_tree.heading("class", text="Class")
        self.recent_tree.heading("name", text="Name")
        self.recent_tree.heading("time", text="Time")
        
        self.recent_tree.column("rank", width=50, anchor="center")
        self.recent_tree.column("class", width=100, anchor="center")
        self.recent_tree.column("name", width=300)
        self.recent_tree.column("time", width=150, anchor="e")
        
        # Style configuration for larger text in treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 14), rowheight=30)
        style.configure("Treeview.Heading", font=("Helvetica", 16, "bold"))
        
        self.recent_tree.pack(fill=tk.BOTH, expand=True)

    def update_time(self, time_str):
        self.time_var.set(time_str)

    def update_recent(self, competitors):
        # Clear current list
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
            
        # Filter only finished competitors
        finished = [c for c in competitors if c.totaltime != 9999999999 and not c.dnf and not c.dns and not c.dsq]
        
        # Calculate class ranks
        class_results = {}
        for comp in finished:
            if comp.kilpasarja not in class_results:
                class_results[comp.kilpasarja] = []
            class_results[comp.kilpasarja].append(comp)
            
        for cls in class_results:
            class_results[cls].sort(key=lambda x: x.totaltime)

        # Sort by finish timestamp descending (latest finisher first)
        # Fallback to totaltime if timestamp is 0 (e.g. old data)
        finished.sort(key=lambda x: x.finish_timestamp if hasattr(x, 'finish_timestamp') and x.finish_timestamp > 0 else x.totaltime, reverse=True)
        
        # Show top 20
        for i, comp in enumerate(finished[:20]):
            time_str = self._format_time(comp.totaltime)
            
            # Determine medal
            medal = ""
            if comp.kilpasarja in class_results:
                class_rank = class_results[comp.kilpasarja].index(comp)
                if class_rank == 0:
                    medal = "🥇 "
                elif class_rank == 1:
                    medal = "🥈 "
                elif class_rank == 2:
                    medal = "🥉 "
            
            display_name = f"{medal}{comp.etunimi} {comp.sukunimi}"
            
            self.recent_tree.insert("", "end", values=(i+1, comp.kilpasarja, display_name, time_str))

    def _format_time(self, seconds):
        import time
        return time.strftime("%H:%M:%S", time.gmtime(seconds)) + (",%02d" % int(((seconds - int(seconds)) * 100)))
