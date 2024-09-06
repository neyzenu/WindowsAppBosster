import psutil
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def boost_apps():
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        if proc.info['status'] == psutil.STATUS_RUNNING:
            try:
                p = psutil.Process(proc.info['pid'])
                p.nice(psutil.HIGH_PRIORITY_CLASS)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    messagebox.showinfo("Bilgilendirme", "Çalışan uygulamaların önceliği artırıldı.")

def update_chart():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent

    # CPU ve RAM kullanımını gösteren pie chart
    labels = ['Kullanılan CPU', 'Boşta CPU', 'Kullanılan RAM', 'Boşta RAM']
    sizes = [cpu_usage, 100 - cpu_usage, ram_usage, 100 - ram_usage]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

    fig.clear()
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    canvas.draw()

    root.after(1000, update_chart)  # Her 1 saniyede bir güncelleniyor


root = tk.Tk()
root.title("Bilgisayar Durumu Takip ve Uygulama Hızlandırıcı")

boost_button = tk.Button(root, text="Uygulamaları Hızlandır", command=boost_apps)
boost_button.pack(pady=10)


fig, ax = plt.subplots(figsize=(6, 4), subplot_kw=dict(aspect="equal"))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()


update_chart()

root.mainloop()
