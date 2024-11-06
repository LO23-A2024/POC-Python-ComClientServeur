#POC Communication Client-Serveur en Python

Utilise les sockets python pour envoyer des messages entre clients et serveur.
Utilise les threads python pour l'écoute des sockets.
Utilise select pour check les flags des sockets afin de n'utiliser qu'un seul thread.
Test de la sérialisation de JSON

Version 3 simplifié(moins de gestion d'exceptions et de cas spéciaux parce que ça devenait du code spaghetti)