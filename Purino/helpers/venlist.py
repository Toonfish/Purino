def get_vendor_list():
    file = open(settings.server_path + "Lieferanten.txt", "r")
    vendors = []
    for line in file:
        vendors.append(line.strip())
    file.close()
    return vendors


def add_to_vendor_list(name):
    file = open(settings.server_path + "Lieferanten.txt", "a")
    file.write(str(name) + "\n")
    file.close()
    return True
