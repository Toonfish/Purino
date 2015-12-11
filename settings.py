# !/usr/bin/python
# -*- coding: iso-8859-15 -*-


def import_settings():
    """
    :return: settings from settings file
    """
    settings_file = open("assets/settings.config", "r")
    data = settings_file.read().split("\n")
    settings_file.close()
    return data


def export_settings():
    """
    :return: exports settings to settings file, returns True if successful
    """
    settings_file = open("assets/settings.config", "r")
    export_string = ""
    for item in [invoice_scans_path, server_path, permissions, gui_bg_color, gui_button_color]:
        export_string += item + "\n"
    if settings_file.write(export_string):
        settings_file.close()
        return True
    else:
        settings_file.close()
        return False

settings_data = import_settings()
username = settings_data[0]
cost_centers = settings_data[1].split(" ")
server_path = settings_data[2]
invoice_scans_path = server_path + "Scans/"
processing_path = server_path + "InBearbeitung/"
invoices_to_pay_path = server_path + "Kontrolliert/Bestätigt/"
filed_invoices_path = server_path + "Abgelegt/"
faulty_invoices_path = server_path + "Kontrolliert/Fehlerhaft/"
deleted_invoices_path = server_path + "Gelöscht/"
temp_path = server_path + "Temp/"
datev_trans_path = settings_data[3]
permissions = settings_data[4]
gui_bg_color = settings_data[5]
gui_button_color = settings_data[6]
gui_abg_color = settings_data[7]
gui_text_color = settings_data[8]
invoice_size = (int(settings_data[9].split(" ")[0]),int(settings_data[9].split(" ")[1]))


reg_invoice_path = server_path + "/Aufgenommen/"

