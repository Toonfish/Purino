__author__ = 'Robert'

import guielements as guie


def print_error(error_code, optional=""):
    t = guie.Toplevel(title=errors[error_code][0])
    t.grab_set()
    error_text = errors[error_code][1]
    if optional != "":
        error_text += "\nZusätzliche Informationen: " + optional
    guie.Label(t, text=error_text).grid(padx=20, pady=9)
    return False


errors = {
    # helpers
    "val_cc_syntax": ("Fehlercode: val_cc_syntax",
                      "Die angegebene Kostenstelle ist nicht möglich, bitte prüfen Sie die Eingabe\n"
                      "Nur Zahlen von 2 bis 6 sind erlaubt."),
    # helpers
    "val_cc_missing": ("Fehlercode: val_cc_missing",
                      "Bitte geben Sie eine Kostenstelle an."),
    # helpers
    "val_nr_syntax": ("Fehlercode: val_nr_syntax",
                      "Die angegebene Rechnungsnummer ist nicht möglich, bitte prüfen Sie die Eingabe"
                      '.\nDie folgenden Sonderzeichen sind nicht erlaubt: | > : < \\ / , ? * " ' + "'\n"
                      "(Am besten bitte einfach die entsprechenden Sonderzeichen löschen.)"),
    # helpers
    "val_nr_missing": ("Fehlercode: val_nr_missing",
                       "Bitte geben Sie eine Rechnungsnummer an."),
    # helpers
    "val_date_syntax": ("Fehlercode: val_date_syntax",
                      "Das angegebene Rechnungsdatum ist nicht möglich, bitte prüfen Sie die Eingabe.\n"
                       "Das Format lautet DD-MM-YY oder DD-MM-YYYY."),
    # helpers
    "val_date_missing": ("Fehlercode: val_date_missing",
                       "Bitte geben Sie eine Rechnungsnummer an."),
    # helpers
    "val_sum_syntax": ("Fehlercode: val_sum_syntax",
                      "Die angegebene Endsumme ist nicht möglich, bitte prüfen Sie die Eingabe."),
    # helpers
    "val_sum_missing": ("Fehlercode: val_sum_missing",
                       "Bitte geben Sie eine Endsumme an."),
    # helpers
    "val_sup_syntax": ("Fehlercode: val_sup_syntax",
                      "Der angegebene Lieferant ist nicht möglich, bitte prüfen Sie die Eingabe."
                      '.\nDie folgenden Sonderzeichen sind nicht erlaubt: | > : < \\ / , ? * " ' +
                      "'\n(Am besten bitte einfach die entsprechenden Sonderzeichen löschen.)"),
    # helpers
    "val_sup_missing": ("Fehlercode: val_sup_missing",
                       "Bitte geben Sie einen Lieferanten an."),

    "inv_move_move": ("Fehlercode: inv_move_move",
                      "Beim Verschieben der Rechnung ist ein Fehler aufgetreten"),
    "Reg_ATEI_1": ("Fehlercode: Reg_ATEI_1",
                   "Beim Zugriff auf die Datenbank ist ein Fehler aufgetreten."),
    "App_CCC_CC_1": ("Fehlercode: Reg_Sci_CC_1",
                     "Die angegebene Kostenstelle ist nicht möglich, bitte prüfen Sie die Eingabe\n"
                     "Nur Zahlen von 2 bis 6 sind erlaubt."),
    "Val_Dat_Notes_1": ("Fehlercode: Val_Dat_Notes_1",
                        "Notizen dürfen kein Apostroph (') enthalten, bitte ändern Sie die Eingabe."),
    "reo_n_v": ("Fehlercode: reo_n_v", "Rechnungseingangsordner nicht vorhanden."),
    "dat_n_v": ("Fehlercode: reo_n_v", "Datevordner nicht vorhanden."),
    "ACC_ACI_1": ("Fehlercode: ACC_ACI_1", "Eine Rechnung mit dieser Rechnungsnummer existiert bereits."),
    "Inv_Upd_1": ("Fehlercode: Inv_Upd_1", "Die Datenbank ist im Moment gesperrt weil ein anderer Mitarbeiter auf"
                                           " sie zugreift, bitte versuchen Sie es später erneut."),
    "Inv_Upd_2": ("Fehlercode: Inv_Upd_2", "Ein unbekannter Fehler ist aufgetreten.")}
