import os
import tkinter as tk
import tkinter.ttk as ttk
from helpers import mydate, venlist, validate
import settings
import guielements as guie


class InputFrame(tk.Frame):

    def __init__(self, gui_master, input_fields, no_grid_rows, **kwargs):
        tk.Frame.__init__(self, master=gui_master, **kwargs)
        self.input_fields = []
        self.config(bg=settings.gui_bg_color)
        self.gui_master = gui_master

        gui_dict = {"cc":   guie.TextFrame(self, 'Kostenstelle', width=4, height=1), #TODO width
                    "nr":   guie.TextFrame(self, 'Rechnungsnummer', width=13, height=1),
                    "date": guie.TextFrame(self, 'Rechnungsdatum', width=13, height=1),
                    "sum":  guie.TextFrame(self, 'Endsumme', width=13, height=1),
                    "ven":  guie.ComboboxFrame(self, 'Lieferant', venlist.get_vendor_list(), width=15, height=1),
                    "mat":  guie.CheckButtonFrame(self, 'Material'),
                    "not":  guie.TextFrame(self, 'Notizen', width=19, height=3),
                    "sca":  guie.TextFrame(self, 'Scandatum', width=13, height=1),
                    "his":  guie.TextFrame(self, 'Geschichte', width=19, height=3)}

        for s in input_fields.split(" "):
            if s != "":
                self.input_fields.append((s, gui_dict.get(s)))

        counter = 0
        for field in self.input_fields:
            field[1].grid(row=counter, column=0, pady=3)
            counter += 1
            while counter in no_grid_rows:
                counter += 1

    def get_all_inputs(self):
        result = []
        for field in self.input_fields:
            result.append((field[0], field[1].read()))
        return result

    def clear_all_inputs(self):
        for field in self.input_fields:
            field[1].clear()


class InvoiceViewer(tk.Frame):
    def __init__(self, worker, gui_master, mode, min_size, **kwargs):
        tk.Frame.__init__(self, master=gui_master, **kwargs)

        self.worker = worker
        self.gui_master = gui_master

        mode_dict = {"default":   ("cc nr date sum ven mat sca not his", []),
                     "register":  ("cc nr date sum ven mat", []),
                     "approver":  ("cc not", [1]),
                     "accounter": ("cc nr date sum ven mat not his", []),
                     "searcher":  ("cc nr date sum ven mat sca not his", [])}

        gui_master.geometry("%dx%d%+d%+d" % (1000, 650, max(0, self.winfo_screenwidth() / 2 - 508),
                                       max(0, self.winfo_screenheight() / 2 - 320)))
        gui_master.minsize(min_size[0], min_size[1])

        self.image_canvas = guie.MultiImageCanvas(self)
        self.actions_frame = guie.Frame(self)

        self.top_frame = guie.Frame(self.actions_frame)
        self.input_frame = InputFrame(self.actions_frame, mode_dict[mode][0],  mode_dict[mode][1])
        self.bottom_frame = guie.Frame(self.actions_frame)

         # region top_frame
        guie.Button(self.top_frame, height=1, width=9, borderwidth=1, text="Vorherige",
                    command=worker.prev_invoice).grid(row=0, column=0)
        guie.Button(self.top_frame, height=1, width=9, borderwidth=1, text="Nächste",
                    command=worker.next_invoice).grid(row=0, column=1, padx=(6, 0))
        # endregion

        # region bottom_frame
        guie.Button(self.bottom_frame, height=1, width=20, borderwidth=1, text="Rechnung löschen",
                    command=self.worker.delete_current_invoice).grid(row=1)
        #endregion

        self.grid_self()

    def grid_self(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.image_canvas.grid(row=0, column=0)
        self.sep1 = ttk.Separator(self, orient=tk.VERTICAL)
        self.sep1.grid(row=0, column=1, sticky="NS")
        self.actions_frame.grid(row=0, column=2, sticky="NSEW")

        self.actions_frame.grid_rowconfigure(2, weight=5)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10)
        ttk.Separator(self.actions_frame, orient=tk.HORIZONTAL).grid(row=1, sticky="EW")
        self.input_frame.grid(row=2, column=0, padx=10, pady=10)
        ttk.Separator(self.actions_frame, orient=tk.HORIZONTAL).grid(row=4, sticky="EW")
        self.bottom_frame.grid(row=5, column=0, padx=10, pady=(9, 12))

    def get_all_inputs(self):
        return self.input_frame.get_all_inputs()

    def clear_input_fields(self):
        self.input_frame.clear_all_inputs()

    def new_image_list(self, new_images):
        self.image_canvas.new_image_list(new_images)

    def show_page(self):
        os.startfile(self.image_canvas.get_current_page_path())

    def title(self, new_title):
        self.gui_master.title(new_title)


class RegisterGUI(InvoiceViewer):
    def __init__(self, worker, gui_master, mode, min_size, **kwargs):
        InvoiceViewer.__init__(self, worker, gui_master, mode, min_size, **kwargs)

        self.worker = worker

        # region register_button
        self.ri_button = guie.Button(self.input_frame, height=1, width=20, borderwidth=1,
                                     text="Rechnung speichern", command=self.worker.file_current_invoice)
        self.ri_button.unbind('<Return>')
        self.ri_button.bind('<Return>', lambda e: self.file_current_invoice())
        self.ri_button.grid(row=11, column=0, pady=10)
        # endregion
        # region append_button
        self.append_button = guie.Button(self.input_frame, height=2, width=20, borderwidth=1,
                                         text="Anheften an \nvorherige Rechnung",
                                         command=self.append_to_most_recent).grid(row=12,
                                                                                  column=0)
        # endregion

    def file_current_invoice(self): # TODO
        """
        send data to worker and try to register the invoice
        """
        inv_data = self.input_frame.get_all_inputs()
        print(validate.inv_data(inv_data))

    def append_to_most_recent(self):
        if self.worker.append_to_most_recent():
            self.clear_form()
            self.vendor_list = mydate.get_vendor_list()

    def delete_current_invoice_page(self):
        # if invoice page exists
        if self.worker.delete_current_invoice():
            self.clear_form()
            return True
        return False
