import os

import settings
import invoice as inv
from workers.worker import Worker
from helpers import validate, mydate
import gui

class Register(Worker):
    def __init__(self, gui_master):
        Worker.__init__(self, gui_master)
        self._invoice_list = []
        self.gui_master = gui_master
        self.interface = gui.RegisterGUI(self, gui_master, "register", (500,600))
        self.interface.pack()
        self.get_invoice_list()
        self.load_current_invoice_page()

    def get_invoice_list(self):
        if os.path.exists(settings.invoice_scans_path):
            for file in os.listdir(settings.invoice_scans_path):
                if "jpg" in file:
                    self._invoice_list.append(inv.Invoice(pages=[settings.invoice_scans_path + file]))

    def file_current_invoice(self):
        print("Register process started\n__________")
        inv_data = self.interface.get_all_inputs()
        inv_data.append(("sca", mydate.today()))
        inv_data.append(("his", mydate.timestamp() + "Aufgenommen"))
        if not validate.inv_data(inv_data):
            print("Register process failed on data validation\n____________________")
            return False
        this_inv = self.get_current_invoice()
        this_inv.edit_data(inv_data)
        if this_inv.export():
            print("Invoice successfully registered\n____________________")
            return True
        print("Register process failed on export\n____________________")
        return False

