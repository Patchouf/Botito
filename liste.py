class NodeList:
    def __init__(self, data, link):
        self.data = data
        self.next_node = link
    
    def add_next(self, node):
        self.next_node = node

#création d'une liste chainée qui permet de récupérer les données nécessaire à la récupération de l'historique, sa suppresion. 
class ChainedList:
    def __init__(self):
        self.first_node= None
        self.length = 0
    
    def __str__(self):
        if self.length == 0:
            return "Vide"
        string =  str(self.first_node.data) + ", "
        current_node = self.first_node
        while current_node.next_node is not None:
            string = string + str(current_node.next_node.data) + ", " 
            current_node = current_node.next_node
        return string
    
    def to_str(self):
        if self.length == 0:
            return "Vide"
        string =  str(self.first_node.data) + ",\n"
        current_node = self.first_node
        while current_node.next_node is not None:
            string = string + str(current_node.next_node.data) + ",\n" 
            current_node = current_node.next_node
        return string
    
    def len_node(self):
        return self.length
        
    def append(self, data):
        self.length += 1
        current_node = self.first_node
        if current_node is None:
            self.first_node = NodeList(data, None)
            return
        while current_node.next_node is not None:
            current_node = current_node.next_node
        current_node.next_node = NodeList(data, None)
        
    def get(self, id):
        if id > self.length or id < 0:
            return
        current_node = self.first_node
        while id != 0:
            id -= 1
            current_node = current_node.next_node
        return current_node.data
    
    def create_data(self, data):
        current_node = self.first_node
        while current_node is not None:
            if current_node.data == data:
                return True
            current_node = current_node.next_node
        return False
    
    def clear_hist(self):
        self.first_node = None
        self.length = 0
    
    def insert_data(self, id, data):
        if id > self.length or id < 0:
            return
        self.length += 1
        if id == 0:
            seconde_node = self.first_node
            self.first_node = NodeList(data, seconde_node)
            return
        avant_node = self.first_node
        current_node = self.first_node.next_node
        while id != 1:
            id -= 1
            avant_node = current_node
            current_node = current_node.next_node
        avant_node.next_node = NodeList(data, current_node)
        
    def remove_data(self, id):
        if id > self.length or id < 0:
            return
        self.length -= 1
        if id == 0:
            self.first_node = self.first_node.next_node
        current_node = self.first_node.next_node
        avant_node = self.first_node
        next_node = self.first_node.next_node
        while id != 0:
            id -= 1
            avant_node = current_node
            current_node = current_node.next_node
            next_node = current_node.next_node
        avant_node.next_node = next_node
