from helpers import formathelp
import sqlite3

__author__ = 'Vagt'

import shutil, os

import errors as errors
import settings as settings
from helpers import sqlhelper as sql
from helpers import mydate

class Invoice():
    def __init__(self, cost_center="", inv_nr="", inv_date="", total_sum="", vendor="", is_material=0, notes="", pages=None, state=1):
        self.number = inv_nr
        self.date = inv_date
        self.cost_center = cost_center
        self.total_sum = total_sum
        self.vendor = vendor
        self.notes = notes
        self.history = ""  # helpers.timestamp() + " Aufgenommen\n"
        self.scan_date = ""  # helpers.today()
        if pages is None: self.pages = []
        else: self.pages = pages
        self.state = state
        if is_material != 1 or is_material is None:
            self.material = 0
        else:
            self.material = is_material

    def add_page(self, path):
        self.pages.append(path)



    def edit_data(self, inv_data):
        for key, value in inv_data:
            if key == "date" or key == "sca":
                setattr(self, formathelp.translate_attribute(key), mydate.MyDate(value))
            else:
                setattr(self, formathelp.translate_attribute(key), value)
            

    def update_data(self, new_invoice_number=""):
        if new_invoice_number == "":
            new_invoice_number = self.number
        print("Update Initiated")
        try:
            if sql.update_entry(self, new_invoice_number):
                print("Update Worked")
                return True
        except sqlite3.OperationalError as e:
            return errors.print_error("Inv_Upd_1", e)
        except Exception as e:
            return errors.print_error("Inv_Upd_2", e)
        return False

    def delete(self, save_copy=False):
        if save_copy:
            self.move(settings.deleted_invoices_path)
        else:
            for item in self.pages:
                os.remove(item)
        sql.remove_invoice(self.number)
        return True

    def get_current_location(self):
        if len(self.pages) != 0:
            return self.pages[0][:self.pages[0].rfind("/")+1]
        return False

    def get_pages_string(self):
        res = ""
        for item in self.pages:
            res += "{},".format(item)
        return res[:-1]

    def export(self):
        query = sql.export_query(self)
        sqlconn = sql.getconn()
        if sql.execute(query, sqlconn):
            if self.move(settings.processing_path, sqlconn):
                return True
            else:
                return False
        sqlconn.rollback()
        return False


    def move(self, new_path, sqlconn=sql.getconn()):
        """
        Moves invoice and changes the object and SQL data
        """
        if len(self.pages) == 1:
            old_path = self.pages[0]
            self.pages = []
            self.pages.append(new_path + str(self.number) + "_1")
            if sql.execute(sql.move_query(self)):
                try:
                    shutil.move(old_path, new_path + str(self.number) + "_1")
                    sqlconn.commit()
                    sqlconn.close()
                    return True
                except Exception as e:
                    sqlconn.rollback()
                    sqlconn.close()
                    return errors.print_error("inv_move_move", e)
            else:
                sqlconn.rollback()
                sqlconn.close()
                return errors.print_error("inv_move_sql")
        else:  #TODO move multiple pages
            sqlconn.rollback()
            sqlconn.close()
            return errors.print_error("inv_move_nyi")

    def pretty_print(self):
        result =    "Rechnungsnummer: " + str(self.number)
        result += "\nRechnungsdatum:  " + str(self.date)
        result += "\nKostenstelle:    " + str(self.cost_center)
        result += "\nEndsumme:        " + str(self.total_sum)
        result += "\nLieferant:       " + str(self.vendor)
        result += "\nScandatum:       " + str(self.scan_date)
        result += "\nRechnungsseiten: " + str(self.pages)
        result += "\nRechnungsstatus: " + str(self.state)
        result += "\nIst Material?:   " + str(self.material)
        result += "\nNotizen:         " + str(self.notes)
        result += "\nGeschichte:      " + str(self.history)
        return result


def import_invoice(inv_nr):
    """
    :return: Invoice object from SQL data
    """
    data = sql.get_invoice(inv_nr)
    print(data)
    # cost_center, inv_nr, inv_date, total_sum, vendor
    inv = Invoice(data[2], data[0], helpers.date_to_program(data[1]), data[3], data[4], data[10])
    inv.scan_date = helpers.date_to_program(data[5])
    inv.notes = data[6]
    for item in data[7].split(","):
        inv.add_page(item)
    inv.history = data[8]
    inv.state = data[9]
    return inv

def import_many(inv_data_list):
    res = []
    for data in inv_data_list:
        print(data)
        inv = Invoice(data[2], data[0], helpers.date_to_program(data[1]), data[3], data[4], data[10])
        inv.scan_date = helpers.date_to_program(data[5])
        inv.notes = data[6]
        for item in data[7].split(","):
            inv.add_page(item)
        inv.history = data[8]
        inv.state = data[9]
        res.append(inv)
    return res

def import_invoices_to_approve():
    numbers = sql.get_invoice_numbers_to_approve()
    invoices = []
    for item in numbers:
        invoices.append(import_invoice(item[0]))
    return invoices

def import_invoices_to_account():
    numbers = sql.get_invoice_numbers_to_account()
    invoices = []
    for item in numbers:
        invoices.append(import_invoice(item[0]))
    return invoices
