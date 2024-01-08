# historique = []
# en_attente = None
# waiting_line = []

# async def last_cmd(message):
#     if historique and len(historique)>0:
#         print(historique)
#         last = historique[-1]
#         await message.channel.send(f"Dernière commande {last}")
#     else:
#         await message.channel.send("Il n'y a pas de dernière commande")
       
  
# async def acceder_historique(message):
#     #création de la liste pour créer l'historique
#     if historique and len(historique)>0:
#         print(historique)
#         historique_str = "\n".join(historique)
#         await message.channel.send(f"Voici l'historique des commandes : \n {historique_str}")
#     else:
#         await message.channel.send("Il n'y a pas d'historique")

# async def clear_historique(user_id, message):
#     #supprimer l'historique
#     if user_id in historique:
#         del historique[user_id]
#         await message.channel.send("Votre historique a été supprimé")
 
# async def ajouter_commande(user_id, command):
#     #ajouter une commande à l'historique
#     if user_id not in historique:
#         historique[user_id] = command
#     else:
#         last_command = historique[user_id]
#         historique[user_id] = command, last_command


