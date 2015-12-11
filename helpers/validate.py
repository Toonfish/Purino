import errors
from helpers import formathelp


def inv_nr(inv_nr):
    if len(str(inv_nr)) != 0:
        if any(i in inv_nr for i in ["|", ">", ":", "<", "\\", "?", "*", '"', "'", "/", ","]):
            return errors.print_error("val_nr_syntax")
        return True
    return errors.print_error("val_nr_missing")


def cost_center(cost_center):
    if len(str(cost_center)) != 0:
        if cost_center not in ["0", "1", "2", "3", "4", "5", "6", 0, 1, 2, 3, 4, 5, 6] or len(str(cost_center)) == 0:
            return errors.print_error("val_cc_syntax")
        return True
    return errors.print_error("val_cc_missing")


def date(inv_date):
    if len(str(inv_date)) != 0:
        inv_date = formathelp.format_date(inv_date)
        if not inv_date:
            return errors.print_error("val_date_syntax")
        return True
    return errors.print_error("val_date_missing")


def price(price):
    if len(str(price)) != 0:
        try:
            float(price)
            return True
        except ValueError:
            return errors.print_error("val_sum_syntax")
    return errors.print_error("val_sum_missing")


def vendor(vendor):
    if len(vendor) != 0:
        if any(i in vendor for i in ["|", ">", ":", "<", "\\", "?", "*", '"', "'", "/", ","]):
            return errors.print_error("val_sup_syntax")
        return True
    return errors.print_error("val_sup_missing")


def notes(notes):
    if "'" in notes:
        return errors.print_error("Val_Dat_Notes_1")
    return True


def material(is_mat):
    if is_mat in (0, 1):
        return True
    return False


def inv_data(data):
    dispatch = {"nr": inv_nr,
                "cc": cost_center,
                "date": date,
                "sum": price,
                "ven": vendor,
                "mat": material,
                "sca": date,
                "not": notes,
                "his": notes}
    for item in ["cc", "nr", "date", "sum", "ven", "mat", "sca", "not", "his"]:
        if find_tuple_data(data, item) != False and not dispatch[item](find_tuple_data(data, item)):
            return False
    return True


def find_tuple_data(tuple_list, name):
    """
    Searches a list of tuples for a tuple with name at tuple[0] and returns tuple[1]
    :param tuple_list: the list of tuples to search through
    :param name: tuple[0] of the tuple to find
    :return: tuple[1] where tuple[0]=name, False if name not in any tuple[0] of tuple_list
    """
    for item in tuple_list:
        if item[0] == name:
            return item[1]
    return False
