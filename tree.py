# class Node :
#   def __init__(self,data):
#     self.data = data
#     self.right_child = None
#     self.left_child = None

#   def add_node(self,data):
#     if data < self.data:
#       if self.left_child == None:
#         self.left_child = Node(data)
#       else:
#         self.left_child.add_node(data)
#     else:
#       if self.right_child == None:
#         self.right_child = Node(data)
#       else:
#         self.right_child.add_node(data)

# class Binary_tree:
#   def __init__(self):
#     self.first_node = None
#     self.current_node = None

#   def add_data(self, data):
#     if self.first_node == None:
#       self.first_node = Node(data)
#     else:
#       self.first_node.add_node(data)

#   def get_question(self):
#     self.current_node = "Coucou! Ma première question est : comment te sens tu ? (Répondre par bien ou pas bien)"
#     return self.current_node
#   def send_answer(self,message_content):
#     if message_content ==  "bien": 
#       return "Super! Ma deuxième question est : Veux tu continuer à parler ?"
#       # return self.current_node
#     elif message_content == "pas bien":
#       # self.current_node = self.current_node.left_child
#       self.current_node = "Oh non! Ma deuxième question est : Veux tu m'en parler ?"
#       return self.current_node
#     elif message_content != "bien" or message_content != "pas bien" :
#       return "Je n'ai pas compris, répond que bien ou pas bien ?"

#     if self.current_node == None :
#       self.current_node = self.first_node
#       return "C'est fini"

#     return self.current_node