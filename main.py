import asyncio
import discord
import os
import requests
import json

#intents pour que le bot puisse lire les messages
intents = discord.Intents.all()
intents.message_content = True

#importe les modules, les fichiers et les librairies
from discord.ext import commands
from dotenv import load_dotenv
from historique import *
from liste import ChainedList


#création du préfixe "!" pour les commandes 
client = commands.Bot(command_prefix="!", intents = intents)

#classe pour créer les nodes permettant la création de l'arbre
class ConversationNode:
    def __init__(self, question, right_node=None, left_node=None, answer=None):
        self.question = question
        self.yes_node = right_node
        self.no_node = left_node
        self.answer = answer

#arbre de conversation
pizza_tree = ConversationNode(
    "Voulez-vous composer votre propre pizza?",
    right_node=ConversationNode(
        "Souhaitez-vous une base de sauce à la crème?",
        right_node=ConversationNode(
            "D'accord ! Voulez-vous du fromage?",
            right_node=ConversationNode(
                "Excellent choix! Voulez-vous ajouter du jambon?",
                right_node=ConversationNode("Votre pizza sauce tomate, fromage et jambon est prête! \n Fin du programme \n Pour recommencer, tapez '!reset'"),
                left_node=ConversationNode("Votre pizza sauce tomate et fromage est prête! \n Fin du programme \n Pour recommencer, tapez '!reset'")
            ),
            left_node=ConversationNode("D'accord, votre pizza  à la sauce tomate est prête! \n Fin du programme \n Pour recommencer, tapez '!reset'")
        ),
        left_node=ConversationNode(
            "D'accord, ajoutons des supléments! Voulez-vous du fromage?",
            right_node=ConversationNode(
                "Excellent choix! Voulez-vous ajouter des olives?",
                right_node=ConversationNode("Votre pizza à la crème, fromage et olives est prête! \n Fin du programme \n Pour recommencer, tapez '!reset'"),
                left_node=ConversationNode("Votre pizza à la crème et fromage est prête! \n Fin du programme \n Pour recommencer, tapez '!reset'")
            ),
            left_node=ConversationNode("D'accord, votre pizza à la crème et sans fromage est prête! \n Fin du programme \n Pour recommencer, tapez '!reset'")
        )
    ),
    left_node=ConversationNode("D'accord, peut-être une prochaine fois. Bon appétit! \n Fin du programme \n Pour recommencer, tapez '!reset'")
)

current_node = pizza_tree

#commande pour savoir si le bot est capable de parler d'un sujet
@client.command(name='speak_about')
async def speak_about_command(ctx, *, topic):
    if topic == "pizza":
        await ctx.send("Je peux vous aider à composer votre pizza. Commencez par '!pizza'.")
    else :
       await ctx.send(f"Je ne traite pas encore le sujet {topic}.")

#commande pour réinitialiser l'arbre
@client.command(name='reset')
async def reset_command(message):
    global current_node
    command_ajout_hist(str(message.author), "!reset")
    current_node = pizza_tree
    await message.send("La composition de la pizza a été réinitialisée. Commencez par '!pizza'.")

#commande pour commencer l'arbre
@client.command(name='pizza')
async def pizza_command(message):
    command_ajout_hist(str(message.author), "!pizza")
    global current_node
    current_node = pizza_tree
    await message.send("Commencez par 'yes' si vous souhaitez composer votre pizza.")

#commande pour supprimer n messages + le message de la commande
@client.command(name="clear")
async def delet(message, amount: int):
    command_ajout_hist(str(message.author), "!clear")
    await message.channel.purge(limit=amount + 1)
    await message.send(f'{amount} messages ont été supprimés.', delete_after=3.0)

#fonction pour gérer les messages, les commandes et les réponses du bot
@client.event
async def on_message(message):
    global current_node
    #boucle if pour gérer le préfixe ! des comandes
    if message.content.startswith(client.command_prefix):
        await client.process_commands(message)
        return
    
    if message.author == client.user:
      return
    
    message.content = message.content.lower()

    #réponse sans intêret
    if message.content.startswith("hello"):
      await message.channel.send("Hello")

    if "cochon" in message.content:
      await message.channel.send("R")

    if message.content == "azerty":
      await message.channel.send("qwerty")

    await client.process_commands(message)
    
    #boucle if pour gérer le reset de l'arbre, le début de l'arbre et la suppresion des messages de l'utilisateur
    if message.content.lower() == "!reset":
        current_node = pizza_tree
        command_ajout_hist(str(message.author), "!reset")
        await message.channel.send("La composition de la pizza a été réinitialisée. Commencez par '!pizza'.")
    elif message.content.lower() == "!pizza":
        command_ajout_hist(str(message.author), "!pizza")
        current_node = pizza_tree
        await message.channel.send("Commencez par 'yes' si vous souhaitez composer votre propre pizza.")
    elif message.content.lower() == "!clear":
        command_ajout_hist(str(message.author), "!clear")
        await delet(message.channel)
    elif current_node is not None:
        await handle_question(message.channel, message.content)
    else:
        await message.channel.send("Désolé, je ne comprends pas. Tapez '!aide' pour obtenir de l'aide.")

#fonction pour gérer les questions/réponses de l'arbre
async def handle_question(channel, user_input):
    global current_node

    if user_input.lower() == "yes" and current_node.yes_node:
        current_node = current_node.yes_node
        await channel.send(current_node.question)
    elif user_input.lower() == "no" and current_node.no_node:
        current_node = current_node.no_node
        await channel.send(current_node.question)
    elif current_node.answer:
        await channel.send(current_node.answer)
        current_node = None

#création de l'historique
historique = ChainedList()

#fonction pour ajouter une commande à l'historique
def command_ajout_hist(auteur, commande):
  historique.append(commande)

#commande pour voir la dernière commande effectué par l'utilisateur
@client.command(name="last_command")
async def last_cmd(message):
  if historique.length == 0:
    await message.channel.send(f"Aucune commande")
  else:
    await message.channel.send(f"Dernière commande de l'utilisateur: {historique.get(historique.length - 1)}")
  command_ajout_hist(str(message.author), "!last_command")

#commande pour supprimer/vider l'historique
@client.command(name="clear_historique")
async def vider(message):
  command_ajout_hist(str(message.author), "!clear_historique")
  historique.clear_hist()
  await message.channel.send("L'historique a été vider!")

#commande pour accéder à l'historique
@client.command(name="historique")
async def histori(message):
  command_ajout_hist(str(message.author), "!historique")
  await message.channel.send(f"Historique des commandes de l'utilisateur : \n {historique.to_str()}")

# commande d'aide pour retrouver les commandes
@client.command(name="aide")
async def aide(message):
  command_ajout_hist(str(message.author), "!aide")
  await message.channel.send("```Vous pouvez utiliser les commandes suivantes : \n !pizza :  création de pizza, \n !speak_about : pour parler d'un sujet, \n !reset : pour réinitialiser la pizza, \n !clear + n : pour effacer n message, \n !historique : voir tout l'historique, \n !last_command : pour voir les dernières commandes, \n !clear_historique : pour vider l'historique du bot, \n !recette + le nom + personnes : propose plusieurs recettes de patisseries \n !aide : pour obtenir de l'aide.```")

#fonctionalité bonus envoie une blague à l'arrivée d'un nouveau membre
@client.event
async def on_member_join(member):
    
   url = "https://humor-jokes-and-memes.p.rapidapi.com/jokes/search"

  #  querystring = {"exclude-tags":"nsfw","min-rating":"7","include-tags":"one_liner","max-length":"200", "avaible": "true"}

   headers = {
	    "X-RapidAPI-Key": "624dbe0564msh1d8309e0091d718p198e17jsn106216569acc",
	    "X-RapidAPI-Host": "humor-jokes-and-memes.p.rapidapi.com"
    }

   response = requests.request("GET", url, headers=headers)
   dictinnaire = json.loads(response.text)
   
   joke = dictinnaire["jokes"][0]["joke"]
    # response = requests.request("GET", url, headers=headers)
   channel = client.get_channel(1168925833348517971)
   await channel.send("welcome "+ member.name + "!! Here is a joke:")
   #await channel.send(
    # await channel.send("haha")
   await channel.send(joke)

#fonctionalité bonus envoie un message d'au revoir à un membre qui quitte le serveur
@client.event
async def on_member_remove(member):
    general_channel = client.get_channel(1168925833348517971)
    await general_channel.send("Au revoir "+ member.name)    

#gérer l'erreur liée à un argument manquant
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument) and ctx.command.name == "recette":
    await ctx.send("Veuillez fournir un choix de recette parmi : gateau, cookie, muffin, tarte. Ainsi que les portions par personne N'oubliez pas le préfixe '!recette'")
  elif isinstance(error, commands.MissingRequiredArgument) and ctx.command.name == "clear":
    await ctx.send("Veuillez fournir un nombre de messages à supprimer. N'oubliez pas le préfixe '!clear'")
  elif isinstance(error, asyncio.TimeoutError):
    await ctx.send("Temps écoulé. Veuillez réessayer.")
  else:
    raise error
    
#fonctionalité bonus pour afficher une recette de pâtisserie    
@client.command(name="recette")
async def recette_patisserie(message, choix_patisserie, portions):
    command_ajout_hist(str(message.author), "!recette")
    portions = int(portions)

    #dictionnaire
    patisserie = {
        'gateau': gateau,
        'cookie': cookie,
        'muffin': muffin,
        'tarte': tarte,
    }
    if choix_patisserie is None:
        def check(message):
            return message.author == message.author and message.channel == message.channel

        try:
            choix_patisserie = await client.wait_for('message', check=check, timeout=30.0)
            choix_patisserie = choix_patisserie.content.lower()
        except asyncio.TimeoutError:
            await message.send("Temps écoulé. Veuillez réessayer.")
            return

    fonction_patisserie_choisie = patisserie.get(choix_patisserie, defaut)
    recette = fonction_patisserie_choisie(portions)

    await message.send(recette)

# fonction pour ajuster les portions par personne de la recette
def ajuster_portions(recette, portions):
    facteur_echelle = portions / 4.0
    recette_ajustee = "\n".join(
        f"{ligne.split('.')[0]} : {int(float(ligne.split(':')[1].strip().split(' ')[0]) * facteur_echelle)} {ligne.split(':')[1].strip().split(' ')[1]}"
        if (':' in ligne) and ligne.split(':')[1].strip().split(' ')[0] else ligne
        for ligne in recette.split('\n')
    )
    return f"\nRecette ajustée pour {portions} personnes :\n{recette_ajustee}"

#recette de pâtisserie gateau, cookie, muffin, tarte aux fruits
def gateau(portions):
    recette = """
    ```Ingrédients pour {portions} personnes} :
    1. Farine : 150 g
    2. Sucre : 100 g
    3. Levure chimique : 1 cuillère à café
    4. Sel : 1 pincée
    5. Oeufs : 3
    6. Lait : 20 cl
    7. Extrait de vanille : 1 cuillère à café
    8. Beurre (pour le moule)

    Recette du gâteau :
    1. Préchauffez le four à 160°C.
    2. Mélangez 150 grammes de farine, 100 grammes de sucre, 1 cuillère à café de levure chimique et une pincée de sel dans un bol.
    3. Ajoutez 3 œufs, 20cl de lait et 1 cuillère à café d'extrait de vanille. Bien mélanger.
    4. Versez la pâte dans un moule à gâteau beurré.
    5. Faites cuire au four pendant 30-35 minutes ou jusqu'à ce qu'un cure-dent/ la pointe d'un couteau en ressorte propre.
    6. Laissez refroidir avant de glacer.```
    """
    return ajuster_portions(recette, portions)

def cookie(portions):
    recette = """
    ```Ingrédients :
    1. Beurre : 50 g
    2. Sucre : 120 g
    3. Oeufs : 2 unités
    4. Farine : 100 g
    5. Bicarbonate de soude : 1 cuillère à café
    6. Sel : 1 pincée
    7. (Optionnel) Pépites de chocolat : 150 g
    8. (Optionnel) Noix hachées : 150 g
    9. (Optionnel) Vanille :  1 cuillère à café```
    Recette des cookies :
    1. Préchauffez le four à 170°C.
    2. Dans un bol, mélangez le beurre, le sucre et les œufs.
    3. Ajoutez farine, bicarbonate de soude et sel. Bien mélangez.
    4. Déposez des cuillerées de pâte sur une plaque de cuisson.
    5. Faites cuire de 10 à 12 minutes ou jusqu'à ce que les bords soient dorés.
    6. Laissez refroidir les cookies sur une grille.
    """
    return ajuster_portions(recette, portions)

def muffin(portions):
    recette = """
    ``` Ingrédients :
    1. Farine : 200 g
    2. Levure chimique : 1 cuillère à soupe
    3. Sucre : 120 g
    4. Oeufs : 2 unités
    5. Lait : 20 ml
    6. Beurre fondu : 50 g
    7. (Optionnel) Arômes ou ingrédients de votre choix
    8. (Optionnel) Pépites de chocolat, fruits, noix, etc. : 120 g
    Recette des muffins :
    1. Préchauffez le four à 185°C.
    2. Mélangez  farine, levure chimique et sucre dans un bol.
    3. Dans un autre bol, fouettez œufs, le lait et le beurre fondu.
    4. Combinez les ingrédients humides et secs, en remuant juste assez pour les humidifié.
    5. Remplissez les moules à muffins aux deux tiers et faites cuire entre 15 et 18 minutes.
    6. Laissez refroidir les muffins avant de les servir.```
    """
    return ajuster_portions(recette, portions)

def tarte(portions):
    recette = """
    ``` Ingrédients :
    1. Pâte à tarte maison ou prête à l'emploi
    2. Fruits de votre choix : 200 g
    3. Sucre : 100 g
    4. Épices (cannelle, etc.) : 1 cuillère à café
    5. Beurre (pour le moule)
    6. (Optionnel) Garnitures supplémentaires selon le goût```
    Recette de tarte aux fruits:
    1. Préchauffez le four à 160°C.
    2. Préparez votre pate à tarte faite maison ou utilisez une prête à l'emploi.
    3. Dans un bol, mélangez fruits de votre choix, le sucre et les épices.
    4. Versez la garniture dans un moule tarte, en scellant les bords.
    5. Placez le moule sur une grille.
    6. Faites cuire au four pendant 45 à 50 minutes ou jusqu'à ce que la croûte soit dorée.
    7. Laissez refroidir la tarte avant de la découper.```
    """
    return ajuster_portions(recette, portions)

def defaut():
    return "Choix de pâtisserie non valide."    

#prépare le bot à l'emploi
@client.event
async def on_ready():
    print("Le bot est prêt !")    


#TOKEN caché
load_dotenv(dotenv_path="config") 
client.run(os.getenv("TOKEN"))