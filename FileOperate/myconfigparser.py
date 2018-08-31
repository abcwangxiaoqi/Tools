import configparser

class myConfigparser:

    def __init__(self,path):
        self.cfg = configparser.ConfigParser()
        self._path = path
        return

    def add_section(self,selection):
        self.cfg.add_section(selection)
        return

    def read(self,encoding=None):
        self.cfg.read(self._path, encoding=encoding)
        return

    def set(self,section, option,value):
        self.cfg.set(section, option,value)
        return

    def get(self,section, option):
        return self.cfg.get(section,option)

    def save(self,encoding=None):

        with open(self._path,"w+",encoding=encoding) as fp:
            self.cfg.write(fp)
            fp.close()

        return