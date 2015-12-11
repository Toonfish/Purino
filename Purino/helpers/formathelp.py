import datetime




def format_date(date_text):
    print(date_text)
    try:
        date_text = date_text.replace(",", ".")
        if len(date_text.split(".")) == 3:
            if len(date_text.split(".")[0]) == 1:
                date_text = "0" + date_text
            if len(date_text.split(".")[1]) == 1:
                date_text = date_text[:3] + "0" + date_text[3:]
            if len(date_text.split(".")[2]) == 2:
                date_text = date_text[0:-2] + "20" + date_text[-2:]
        if len(date_text.split(".")) == 1:
            # if date format == DDMM
            if len(date_text) == 4:
                # check if invoice is from previous year
                if int(date_text[2:4]) > int(datetime.date.today().month):
                    date_text = date_text[0:2] + "." + date_text[2:4] + "." + str(datetime.date.today().year - 1)
                else:
                    date_text = date_text[0:2] + "." + date_text[2:4] + "." + str(datetime.date.today().year)
            # if date format = DMM or DDM
            elif len(date_text) == 3:
                # if date format = DDM
                if (int(date_text[-2:]) >= 13 or 0 >= int(date_text[-2:]) - datetime.datetime.now().month >= -3):
                    return format_date(date_text[:2] + "0" + date_text[2])

                else:
                    return format_date("0" + date_text[0] + date_text[1:])
#                elif (date_text[-1:] == str(datetime.datetime.now().month) or date_text[-1:] == str(
#                            datetime.datetime.now().month - 1)):
#                    if date_text[1] == "0":
#                        return validate_date("0" + date_text[0] + date_text[1:])
#                    else:
#                        return validate_date(date_text[:2] + "0" + date_text[2])
            # if date format = DM
            elif len(date_text) == 2:
                return format_date("0" + date_text[0] + "0" + date_text[1])
            # if date format == DDMMYY
            elif len(date_text) == 6:
                date_text = date_text[0:2] + "." + date_text[2:4] + ".20" + date_text[4:]
        datetime.datetime.strptime(date_text, "%d.%m.%Y")
        return date_text
    except Exception as e:
        print(e)
        return False


def date_to_program(sql_date):
    if "." in sql_date:
        return sql_date
    else:
        return sql_date.split("-")[2] + "." + sql_date.split("-")[1] + "." + sql_date.split("-")[0]


def date_to_sql(p_date):
    if "-" in p_date:
        return p_date
    else:
        return p_date.split(".")[2] + "-" + p_date.split(".")[1] + "-" + p_date.split(".")[0]


def translate_attribute(attribute_code):
    code_to_full = {"nr": "number",
                    "cc": "cost_center",
                    "date": "date",
                    "sum": "total_sum",
                    "ven": "vendor",
                    "mat": "material",
                    "sca": "scan_date",
                    "not": "notes",
                    "his": "history"}
    return code_to_full[attribute_code]