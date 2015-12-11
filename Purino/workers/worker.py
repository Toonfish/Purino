from gui import InvoiceViewer

__author__ = 'Vagt'

import os


class Worker():
    def __init__(self, gui_master):
        self.gui_master = gui_master
        self._current_invoice_nr = 0
        self.interface = InvoiceViewer(self, self.gui_master, "default", (600,500))
        self._invoice_list = []

    def get_current_invoice(self):
        """
        :return:filename of the invoice currently shown
        """
        return self._invoice_list[self._current_invoice_nr]

    def load_current_invoice_page(self):
        self.interface.new_image_list(self.get_current_invoice().pages)

    def next_invoice(self):
        if self._current_invoice_nr + 1 >= len(self._invoice_list):
            self._current_invoice_nr = 0
        else:
            self._current_invoice_nr += 1
        return True

    def prev_invoice(self):
        if self._current_invoice_nr - 1 < 0:
            self._current_invoice_nr = len(self._invoice_list) - 1
        else:
            self._current_invoice_nr -= 1
        return True

    def delete_current_invoice(self, save_copy=False):
        self.get_current_invoice().delete(save_copy)
        self._invoice_list.remove(self.get_current_invoice())
        return True

    def get_invoice_count(self):
        return len(self._invoice_list)
