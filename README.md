# Botito

Botito est un bot discord crée en projet de fin de matière en Python.
Botito permet de donner des recettes de patisserie, de faire sa propre pizza etc

## Configuration

Créer un fichier config où vous mettrez votre Token.
Il doit être formaté ainsi `TOKEN=(votre token)`.

## Documentation

Toute commande ci-dessous doivent être précéder du signe `!` pour fonctionner correctement.

```
Exemple : 
    - !reset
    - !pizza
    - !recette cookie 2
```
## Commandes
- [aide](#aide)
- [pizza](#pizza)
- [speak_about](#speak_about)
- [reset](#reset)
- [clear](#clear)
- [historique](#historique)
- [last_command](#last_command)
- [clear_historique](#clear_historique)
- [recette](#recette)


### aide 
  permet de visualiser les commandes
  
### pizza
  création de l'arbre qui permet de faire une pizza
  
#### speak_about 
  permet de savoir si le bot est capable de parler d'un sujet
  
### reset 
  permet de réinitialiser l'arbre
  
#### clear
  permet d'effacer les messages de la conversation (par exemple : `!clear 2`)
  il est obligatoire d'ajouter un argument : un chiffre après `!clear`
     
#### historique 
   permet de voir tout l'historique
   
#### last_command 
  permet de voir la dernière commande saisie
  
#### clear_historique 
  permet de vider/supprimer l'historique du bot
  
#### recette
  propose plusieurs recettes de pâtisseries (par exemple : `!recette cookie 2`)
  il est obligatoire d'ajouter deux arguments : la recette choisi et pour le nombre de personne après `!recette`


## Aide/lien utilisé
aide de mes camarades de classe pour la liste chainé et l'arbre.
https://www.docstring.fr/blog/creer-un-bot-discord-avec-python/
https://github.com/Rapptz/discord.py/blob/master/examples/deleted.py
https://www.youtube.com/watch?v=ksAtGCFxrP8&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=2&ab_channel=JamesS
https://rapidapi.com/humorapi/api/humor-jokes-and-memes/
