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
        
        self.recent_tree = ttk.Treeview(self.recent_frame, columns=("rank", "name", "time"), show="headings", height=5)
        self.recent_tree.heading("rank", text="Rank")
        self.recent_tree.heading("name", text="Name")
        self.recent_tree.heading("time", text="Time")
        
        self.recent_tree.column("rank", width=50, anchor="center")
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
            
        # Sort by finish time (assuming totaltime is available and valid)
        # Filter only finished competitors
        finished = [c for c in competitors if c.totaltime != 9999999999 and not c.dnf and not c.dns and not c.dsq]
        # Sort by totaltime descending (most recent finishes might be what we want, but usually "recent" means last added)
        # Actually, for a "Recent Finishers" list, we probably want the ones who *just* finished.
        # But without a timestamp of *when* they finished, we can't easily sort by "finish time absolute".
        # However, the `competitors` list order might not be guaranteed.
        # Let's try to show the top 5 fastest for now, or if we can, the last ones processed.
        # Given the current app structure, let's just show the top 5 fastest (Leaderboard style) 
        # OR we can try to infer "recent" if the app tracks it. 
        # The app doesn't seem to track "finish timestamp" explicitly other than `totaltime` (race duration).
        # So "Recent" in a race context usually means "Leaderboard" or "Last on track".
        # Let's do Leaderboard (Fastest) for now as it's most common for simple displays.
        
        finished.sort(key=lambda x: x.totaltime)
        
        # Show top 10
        for i, comp in enumerate(finished[:10]):
            time_str = self._format_time(comp.totaltime)
            self.recent_tree.insert("", "end", values=(i+1, f"{comp.etunimi} {comp.sukunimi}", time_str))

    def _format_time(self, seconds):
        import time
        return time.strftime("%H:%M:%S", time.gmtime(seconds)) + (",%02d" % int(((seconds - int(seconds)) * 100)))
