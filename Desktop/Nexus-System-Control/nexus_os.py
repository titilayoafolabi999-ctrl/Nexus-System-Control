import customtkinter as ctk
from tkinter import filedialog, messagebox
import os, shutil, psutil, requests
from datetime import datetime

# Global UI Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NexusOS(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nexus OS - System Toolkit")
        self.geometry("950x600")
        
        # Main Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.sidebar, text="NEXUS COMMAND", font=("Roboto", 22, "bold")).pack(pady=30)

        # Navigation
        self.setup_nav_button("📊 System Monitor", self.show_sys_monitor)
        self.setup_nav_button("🧹 File Janitor", self.show_janitor)
        self.setup_nav_button("🌤️ Weather Station", self.show_weather)

        # Tool Description Box
        self.desc_box = ctk.CTkFrame(self.sidebar, fg_color="#2b2b2b", corner_radius=10)
        self.desc_box.pack(side="bottom", fill="x", padx=15, pady=20)
        self.desc_label = ctk.CTkLabel(self.desc_box, text="System initialized. Select a tool.", 
                                      wraplength=180, font=("Roboto", 11), text_color="#aaaaaa")
        self.desc_label.pack(pady=10, padx=10)

        # --- MAIN DISPLAY ---
        self.main_area = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e1e1e")
        self.main_area.grid(row=0, column=1, padx=20, pady=(20, 50), sticky="nsew")

        # --- STATUS BAR ---
        self.status_bar = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_bar.place(relx=0, rely=1, relwidth=1, anchor="sw")
        self.time_lbl = ctk.CTkLabel(self.status_bar, text="", font=("Roboto", 11))
        self.time_lbl.pack(side="right", padx=20)
        self.status_msg = ctk.CTkLabel(self.status_bar, text="Nexus OS v1.0 | Status: Online", font=("Roboto", 11))
        self.status_msg.pack(side="left", padx=20)

        self.update_clock()
        self.show_welcome()

    def setup_nav_button(self, name, cmd):
        ctk.CTkButton(self.sidebar, text=name, command=cmd, height=45).pack(pady=10, padx=20, fill="x")

    def clear_main(self):
        for widget in self.main_area.winfo_children(): widget.destroy()

    def update_clock(self):
        self.time_lbl.configure(text=datetime.now().strftime("%Y-%m-%d | %H:%M:%S"))
        self.after(1000, self.update_clock)

    def show_welcome(self):
        self.clear_main()
        ctk.CTkLabel(self.main_area, text="WELCOME TO NEXUS OS", font=("Roboto", 32, "bold")).pack(expand=True)

    # MODULE 1: SYSTEM MONITOR
    def show_sys_monitor(self):
        self.desc_label.configure(text="Live diagnostics: Tracking CPU and RAM utilization percentages.")
        self.clear_main()
        ctk.CTkLabel(self.main_area, text="Hardware Diagnostics", font=("Roboto", 22, "bold")).pack(pady=30)
        self.cpu_bar = ctk.CTkProgressBar(self.main_area, width=500); self.cpu_bar.pack(pady=10)
        self.cpu_lbl = ctk.CTkLabel(self.main_area, text="CPU: 0%"); self.cpu_lbl.pack()
        self.ram_bar = ctk.CTkProgressBar(self.main_area, width=500); self.ram_bar.pack(pady=20)
        self.ram_lbl = ctk.CTkLabel(self.main_area, text="RAM: 0%"); self.ram_lbl.pack()
        self.refresh_sys()

    def refresh_sys(self):
        if hasattr(self, 'cpu_bar'):
            c, r = psutil.cpu_percent(), psutil.virtual_memory().percent
            self.cpu_bar.set(c/100); self.ram_bar.set(r/100)
            self.cpu_lbl.configure(text=f"CPU Load: {c}%"); self.ram_lbl.configure(text=f"RAM Load: {r}%")
            self.after(1000, self.refresh_sys)

    # MODULE 2: FILE JANITOR
    def show_janitor(self):
        self.desc_label.configure(text="Storage Cleanup: Automatically sorts files into Images, Docs, Media, and Apps.")
        self.clear_main()
        ctk.CTkLabel(self.main_area, text="Storage Janitor", font=("Roboto", 22, "bold")).pack(pady=30)
        self.p_str = ctk.StringVar(value="No path selected...")
        ctk.CTkLabel(self.main_area, textvariable=self.p_str, text_color="gray").pack()
        ctk.CTkButton(self.main_area, text="Select Target Folder", command=self.pick_p).pack(pady=10)
        ctk.CTkButton(self.main_area, text="Execute Cleanup", fg_color="green", command=self.run_c).pack(pady=10)

    def pick_p(self):
        path = filedialog.askdirectory()
        if path: self.p_str.set(path)

    def run_c(self):
        p = self.p_str.get()
        if not os.path.exists(p) or p == "No path selected...": return
        cats = {"Images":['.jpg','.png','.jpeg'], "Docs":['.pdf','.txt','.docx'], "Media":['.mp4','.mp3'], "Apps":['.exe','.msi']}
        cnt = 0
        for f in os.listdir(p):
            ext = os.path.splitext(f)[1].lower()
            for cat, exts in cats.items():
                if ext in exts:
                    d = os.path.join(p, cat); os.makedirs(d, exist_ok=True)
                    shutil.move(os.path.join(p, f), os.path.join(d, f)); cnt += 1
        messagebox.showinfo("Nexus Janitor", f"Process complete. {cnt} files organized.")

    # MODULE 3: WEATHER STATION
    def show_weather(self):
        self.desc_label.configure(text="Satellite Data: Fetching real-time global weather conditions via API.")
        self.clear_main()
        ctk.CTkLabel(self.main_area, text="Weather Station", font=("Roboto", 22, "bold")).pack(pady=30)
        self.entry = ctk.CTkEntry(self.main_area, placeholder_text="Enter City Name", width=300); self.entry.pack(pady=10)
        ctk.CTkButton(self.main_area, text="Retrieve Data", command=self.get_w).pack(pady=10)
        self.w_info = ctk.CTkLabel(self.main_area, text="", font=("Roboto", 16, "italic"), justify="left")
        self.w_info.pack(pady=30)

    def get_w(self):
        city = self.entry.get()
        if not city: return
        try:
            r = requests.get(f"https://wttr.in/{city}?format=%C+%t+%h+%w+%f").text.split()
            if len(r) >= 5:
                txt = f"📍 {city.capitalize()}\n\n☁️ Condition: {r[0]}\n🌡️ Temp: {r[1]}\n💧 Humidity: {r[2]}\n🌬️ Wind: {r[3]}\n🧥 Feels Like: {r[4]}"
                self.w_info.configure(text=txt)
            else: self.w_info.configure(text="Data unavailable for this location.")
        except: self.w_info.configure(text="Connection Error: Check internet.")

if __name__ == "__main__":
    app = NexusOS(); app.mainloop()