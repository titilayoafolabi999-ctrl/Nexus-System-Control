import customtkinter as ctk
from tkinter import filedialog, messagebox
import os, shutil, psutil, requests
from datetime import datetime

# Configure the look of the app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NexusOS(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nexus OS - System Toolkit")
        self.geometry("950x600")

        # Configure Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR FRAME ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="NEXUS COMMAND", font=("Roboto", 22, "bold")).pack(pady=30)

        # Navigation Buttons
        self.setup_nav_button("📊 System Monitor", self.show_sys_monitor)
        self.setup_nav_button("🧹 File Janitor", self.show_janitor)
        self.setup_nav_button("🌤️ Weather Station", self.show_weather)

        # Tool Description Panel
        self.desc_box = ctk.CTkFrame(self.sidebar, fg_color="#2b2b2b", corner_radius=10)
        self.desc_box.pack(side="bottom", fill="x", padx=15, pady=20)
        
        self.desc_label = ctk.CTkLabel(self.desc_box, text="Select a tool to view its function.", 
                                      wraplength=180, font=("Roboto", 11), text_color="#aaaaaa")
        self.desc_label.pack(pady=10, padx=10)

        # --- MAIN DISPLAY AREA ---
        self.main_area = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e1e1e")
        self.main_area.grid(row=0, column=1, padx=20, pady=(20, 50), sticky="nsew")

        # --- STATUS BAR ---
        self.status_bar = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_bar.place(relx=0, rely=1, relwidth=1, anchor="sw")

        self.time_lbl = ctk.CTkLabel(self.status_bar, text="", font=("Roboto", 11))
        self.time_lbl.pack(side="right", padx=20)
        
        self.status_msg = ctk.CTkLabel(self.status_bar, text="Ready", font=("Roboto", 11))
        self.status_msg.pack(side="left", padx=20)

        self.update_clock()
        self.show_welcome()

    # --- UI HELPERS ---
    def setup_nav_button(self, name, cmd):
        ctk.CTkButton(self.sidebar, text=name, command=cmd, height=45, font=("Roboto", 14)).pack(pady=10, padx=20, fill="x")

    def clear_main(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
        self.time_lbl.configure(text=now)
        self.after(1000, self.update_clock)

    def show_welcome(self):
        self.clear_main()
        ctk.CTkLabel(self.main_area, text="WELCOME TO NEXUS OS", font=("Roboto", 32, "bold")).pack(expand=True)

    # --- TOOL 1: SYSTEM MONITOR ---
    def show_sys_monitor(self):
        self.desc_label.configure(text="Monitors live hardware performance. Tracks CPU and RAM load percentages via psutil kernel pings.")
        self.clear_main()
        
        ctk.CTkLabel(self.main_area, text="Hardware Diagnostics", font=("Roboto", 22, "bold")).pack(pady=30)
        
        self.cpu_bar = ctk.CTkProgressBar(self.main_area, width=500)
        self.cpu_bar.pack(pady=10)
        self.cpu_val = ctk.CTkLabel(self.main_area, text="CPU Load: 0%")
        self.cpu_val.pack()

        self.ram_bar = ctk.CTkProgressBar(self.main_area, width=500)
        self.ram_bar.pack(pady=20)
        self.ram_val = ctk.CTkLabel(self.main_area, text="RAM Load: 0%")
        self.ram_val.pack()

        self.refresh_sys_data()

    def refresh_sys_data(self):
        if hasattr(self, 'cpu_bar'):
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.cpu_bar.set(cpu / 100)
            self.ram_bar.set(ram / 100)
            self.cpu_val.configure(text=f"CPU Load: {cpu}%")
            self.ram_val.configure(text=f"RAM Load: {ram}%")
            self.after(1000, self.refresh_sys_data)

    # --- TOOL 2: FILE JANITOR ---
    def show_janitor(self):
        self.desc_label.configure(text="Automatically organizes files into categorized folders based on their extensions. Ideal for cleaning Downloads folders.")
        self.clear_main()
        
        ctk.CTkLabel(self.main_area, text="Storage Janitor", font=("Roboto", 22, "bold")).pack(pady=30)
        
        self.selected_dir = ctk.StringVar(value="No Directory Selected")
        ctk.CTkLabel(self.main_area, textvariable=self.selected_dir, text_color="gray").pack()

        ctk.CTkButton(self.main_area, text="Browse Folder", command=self.pick_folder).pack(pady=15)
        ctk.CTkButton(self.main_area, text="Run Organization", fg_color="green", command=self.start_cleaning).pack(pady=10)

    def pick_folder(self):
        path = filedialog.askdirectory()
        if path: self.selected_dir.set(path)

    def start_cleaning(self):
        path = self.selected_dir.get()
        if not os.path.exists(path) or path == "No Directory Selected":
            messagebox.showerror("Error", "Please select a valid folder.")
            return
            
        categories = {
            "Images": ['.jpg', '.jpeg', '.png', '.gif'],
            "Docs": ['.pdf', '.docx', '.txt', '.xlsx'],
            "Media": ['.mp4', '.mp3', '.wav'],
            "Apps": ['.exe', '.msi']
        }
        
        count = 0
        for file in os.listdir(path):
            ext = os.path.splitext(file)[1].lower()
            for cat, exts in categories.items():
                if ext in exts:
                    dest = os.path.join(path, cat)
                    os.makedirs(dest, exist_ok=True)
                    shutil.move(os.path.join(path, file), os.path.join(dest, file))
                    count += 1
        
        self.status_msg.configure(text=f"Janitor: Processed {count} files.")
        messagebox.showinfo("Success", f"Cleaned {count} files!")

    # --- TOOL 3: WEATHER STATION ---
    def show_weather(self):
        self.desc_label.configure(text="Fetches real-time, detailed meteorological reports including Temp, Humidity, and Wind from global APIs.")
        self.clear_main()
        
        ctk.CTkLabel(self.main_area, text="Weather Station", font=("Roboto", 22, "bold")).pack(pady=30)
        
        self.city_input = ctk.CTkEntry(self.main_area, placeholder_text="Enter city (e.g. New York)", width=300)
        self.city_input.pack(pady=10)
        
        ctk.CTkButton(self.main_area, text="Fetch Report", command=self.fetch_weather).pack(pady=10)
        
        self.weather_info = ctk.CTkLabel(self.main_area, text="", font=("Roboto", 16, "italic"), justify="left")
        self.weather_info.pack(pady=30)

    def fetch_weather(self):
        city = self.city_input.get()
        if not city: return
        self.status_msg.configure(text=f"Fetching {city} data...")
        try:
            # Querying wttr.in for specific data pieces
            res = requests.get(f"https://wttr.in/{city}?format=%C+%t+%h+%w+%f").text.split()
            report = (
                f"📍 Location: {city.capitalize()}\n\n"
                f"☁️ Condition: {res[0]}\n"
                f"🌡️ Temp: {res[1]}\n"
                f"💧 Humidity: {res[2]}\n"
                f"🌬️ Wind: {res[3]}\n"
                f"🧥 Feels Like: {res[4]}"
            )
            self.weather_info.configure(text=report)
            self.status_msg.configure(text="Weather updated.")
        except:
            self.weather_info.configure(text="Error: Could not reach weather service.")

if __name__ == "__main__":
    app = NexusOS()
    app.mainloop()