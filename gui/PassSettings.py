class PassSettings():
    def __init__(self):
        self.email = ''
        self.password = ''
        self.update()
        
    def update(self):
        file = open('settings.txt','r')
        txt = file.read().split(' ')
        try:
            self.email = txt[1]
            self.password = txt[0]
        except:
            self.email = ""
            self.password = ""
        file.close()
    
    def get1(self):
        return self.decode(self.email)
    
    def get2(self):
        return self.decode(self.password)
    
    def add(self, txt1, txt2):
        file = open('settings.txt', 'w')
        txt = self.encode(txt1) + " " + self.encode(txt2)
        file.write(txt)
        file.close()
    
    def clear(self):
        self.add('','')
    
    def decode(self, txt):
        txt = txt[::-1]
        return txt
    
    def encode(self, txt):
        txt = txt[::-1]
        return txt