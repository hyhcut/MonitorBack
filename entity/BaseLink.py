from dataclasses import dataclass


@dataclass
class BaseLink:
    name: str
    host: str
    user: str
    password: str

    def connect(self):
        print("测试连接方法")

    def run(self, cmd):
        print('运行命令方法')

    def cpu(self):
        print('获取CPU使用率方法')

    def mem(self):
        print('获取MEM使用率方法')

    # 返回CPU和MEM基础信息
    def base(self):
        return {
            'name': self.name,
            'address': self.host,
            'info_list': [
                {
                    'name': 'CPU使用率',
                    'value': self.cpu()
                },
                {
                    'name': 'MEM使用率',
                    'value': self.mem()
                }
            ]
        }