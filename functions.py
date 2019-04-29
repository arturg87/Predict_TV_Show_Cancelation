from bs4 import BeautifulSoup

class get_data:

    def __init__(self):
        self.renewed = []
        self.canceled = [] 
        self.rescued = []
        #self.html
           
    def is_renewed(self, text):
        for i in text.find_all('strong'):
            if "under the title" in text.text:
                self.renewed.append(text.find_all('strong')[1].text)
                break
            else:
                self.renewed.append(i.text)

    def is_canceled(self, text):
        for i in text.find_all('strong'):
            if "under the title" in text.text:
                self.canceled.append(text.find_all('strong')[1].text)
                break
            else:
                self.canceled.append(i.text)
    
    def is_rescued(self, text):
        for i in text.find_all('strong'):
            if "under the title" in text.text:
                self.rescued.append(text.find_all('strong')[1].text)
                break
            else:
                self.rescued.append(i.text)
            
            while i.text in self.canceled:
                self.canceled.remove(i.text)
            
