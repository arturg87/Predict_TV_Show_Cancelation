from bs4 import BeautifulSoup

class get_data:

    def __init__(self):
        self.renewed = []
        self.canceled = [] 
        self.rescued = []
        self.removeFromCanceled = []
        #self.html
           
    def is_renewed(self, text):
        for i in text.find_all('strong'):
            if "under the title" in text.text:
                self.renewed.append(text.find_all('strong')[1].text.strip())
                break
            else:
                self.renewed.append(i.text.strip())

    def is_canceled(self, text):
        for i in text.find_all('strong'):
            if "under the title" in text.text:
                self.canceled.append(text.find_all('strong')[1].text.strip())
                break
            else:
                # Special case.
                if i.text.strip() == 'LA→Vegas':
                    self.canceled.append('LA to Vegas')
                elif "untitled" in i.text.strip():
                    pass
                else:
                    self.canceled.append(i.text.strip())
    
    def is_rescued(self, text):
        for i in text.find_all('strong'):
            if "under the title" in text.text:
                self.rescued.append(text.find_all('strong')[1].text.strip())
                self.removeFromCanceled.append(text.find_all('strong')[1].text.strip())
                break
            else:
                self.rescued.append(i.text.strip())
                self.removeFromCanceled.append(i.text.strip())

    def remove_duplicates(self):
        self.canceled = list(set(self.canceled))  
        self.renewed = list(set(self.renewed))  
        self.rescued = list(set(self.rescued))  
