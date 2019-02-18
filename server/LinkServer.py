from entity.Windows import Windows
from entity.Linux import Linux


def base(type, name, address, username, password):
    link = None
    if type == 1:
        link = Windows(name, address, username, password)
    elif type == 2:
        link = Linux(name, address, username, password)
    else:
        return None
    if link.connect():
        return link.base()
    else:
        return "服务器无法连接"