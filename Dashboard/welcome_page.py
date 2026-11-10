import tkinter as tk

def open_welcome():
root = tk.Tk()
root.title("Face Attendance System")
root.geometry("600x400")


title = tk.Label(root, text="Face Recognition Attendance System",
                 font=("Helvetica", 18, "bold"))
title.pack(pady=40)

start_btn = tk.Button(root, text="Start Attendance",
                      font=("Helvetica", 14),
                      bg="green", fg="white",
                      width=20, height=2)
start_btn.pack(pady=20)

exit_btn = tk.Button(root, text="Exit",
                     font=("Helvetica", 12),
                     bg="red", fg="white",
                     command=root.destroy)
exit_btn.pack(pady=10)

root.mainloop()

