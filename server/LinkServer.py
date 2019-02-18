from entity.Windows import Windows
from entity.Linux import Linux


def base(type, name, address, username, password):
    link = None
    if type == 1:
        link = Windows(name, address, username, password)
    elif type == 2:
        link = Linux(name, address, username, password)
    else:
        return False, "服务器类型不存在"
    if link.connect():
        return True, link.base()
    else:
        return False, "服务器无法连接"