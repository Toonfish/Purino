import tkinter as tk

from gui import InvoiceViewer
from workers.register import Register

print("________________________________________")
root = tk.Tk()

w = Register(root)

root.mainloop()