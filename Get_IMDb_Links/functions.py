import re

class get_data:

    def __init__(self):
        self.renewed = []
        self.canceled = [] 
        self.rescued = []
        self.removeFromCanceled = []
        #self.html
           
    def is_renewed(self, text):
        for i in text.find_all('strong'):
            network = internal_get_network(text)

            self.renewed.append({
                'show_name':i.text.strip(), 
                'network': network
            })
            break

    def is_canceled(self, text):
        for i in text.find_all('strong'):
            # Special case.
            if i.text.strip() == 'LA→Vegas':
                network = internal_get_network(text)

                self.canceled.append({
                    'show_name':'LA to Vegas', 
                    'network': network
                })
                break
            elif "untitled" in i.text.strip():
                pass
            else:
                network = internal_get_network(text)

                self.canceled.append({
                    'show_name':i.text.strip(), 
                    'network': network
                })
                break

    def is_rescued(self, text):
        for i in text.find_all('strong'):
            network = internal_get_network(text)

            self.rescued.append({
                'show_name':i.text.strip(), 
                'network': network
            })
    
            self.removeFromCanceled.append({
                'show_name':i.text.strip(), 
                'network': network
            })

    def remove_duplicates(self):
        self.canceled = [ dict(t) for t in { tuple(d.items()) for d in self.canceled } ]  
        self.renewed = [ dict(t) for t in { tuple(d.items()) for d in self.renewed } ]
        self.rescued = [ dict(t) for t in { tuple(d.items()) for d in self.rescued } ]  

def internal_get_network(data):
    removeList = ['13-episode', 'probably']
    try:
        network = re.search(r'\(([^\)]+)\)', data.text).group(1)
    except:
        network = None

    if len(str(network)) > 15:
        network = None

    if (str(network).lower() in removeList):
        network = None

    return network