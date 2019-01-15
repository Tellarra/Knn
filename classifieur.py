import math
from random import shuffle
import re
nom = "Richard Adèle"

class Instance(object) :
    def __init__(self,categorie,coords) :
        """Constructeur d'Instance.

        Arguments:
            categorie (str): La catégorie de l'instance
            coords (tuple): Un tuple de float
                représentant la position de l'instance.
        """
        self.cat = categorie
        self.coords = coords

    def __str__(self) :
        """
        Méthode qui renvoie une représentation de cette instance
            sous forme de string.

        Arguments: 
            None
        
        Renvois: 
            Une représentation de l'instance sous forme de string.
        """
        string = "Catégorie : " + self.cat + "\nCoords :" 
        for coord in self.coords :
            string += " " + str(coord) 
        return string
    
    def distance(self, other) :
        """
        Méthode qui calcule et renvoie 
            la distance Euclidienne entre cette instance
                et une autre.
            
        Arguments :
            self (instance) : 1ère instance
            other (instance) : 2ème instance
            d (int) : La distance
            i (int) : Index commençant à 1

        Renvois : 
            La racine carré de la distance entre x et y
        """
        dist = 0
        i = 1
        for i in range(min(len(self.coords), len(other.coords))) :
            dist += (float(self.coords[i]) - float(other.coords[i]))**2

        return math.sqrt(dist)
        
    def knn(self, k, listeInstances) :
        """
        Méthode qui trouve dans listeInstances les k plus proches 
            instances de l'instance considerée

        Arguments : 
            self (instance) = L'instance considérée
            k (int) = Le nombre de voisins que l'on doit trouver
            listeInstances (liste) = Liste d'instances
            newListe (liste) = Liste avec l'instance associée à sa distance
            distanceElem (tuple) = Tuple avec l'instance associée à sa distance

        Renvois : 
            Une liste d'instance de taille k
        """
        newListe = []
        for i in range(len(listeInstances)) :
            distanceElem = (listeInstances[i], self.distance(listeInstances[i]))
            newListe.append(distanceElem)
        newListe.sort(key=lambda x: x[1])
        proche = []
        for i in range(k) :
            proche.append(newListe[i][0])
        return proche
#Fin de la classe Instance

def most_common(listeInstances) :
    """
    Méthode qui cherche la catégorie la plus fréquente
        parmis une liste d'instance

    Arguments : 
        listeInstances (liste) = Liste d'instances
        dicoCat (dictionnaire) = Dictionnaire ou chaque 
            catégorie sera associé au nombre de fois 
                où elle apparait dans la liste
    
    Renvois : 
        La catégorie la plus fréquente (str)
    """
    dicoCat = {}
    for instance in listeInstances :
        categorie = instance.cat
        if categorie not in dicoCat :
            dicoCat[categorie] = 1
        else :
            dicoCat[categorie] += 1
    return max(dicoCat, key=lambda x: x[1])

def classify_instance(k, instance, all_instances) :
    """
    Methode qui renvoie la categorie la plus frequente 
        parmi les k plus proches voisins de instance.

    Arguments : 
        k (int) = Le nombre de voisins que l'on doit trouver
        instance (instance) = L'instance que l'on prend comme référence
        all_instances (liste) = La liste de toutes les instances

    Renvois :
        La catégorie la plus fréquente (str)
    """
    return most_common(instance.knn(k, all_instances))

def read_instances(filename) :
    """
    Méthode qui lit des instances
        dans un chier et renvoie une liste d'instances ainsi lues.
    
    Arguments :
        filename (file) = Le fichier que l'on lis
        listeInstances (liste) = Liste des instances que l'on va trouver
        line (liste) = Liste de chaque ligne que l'on a split à chaque ","

    Renvois :
        La liste des instances trouvées dans le fichier
    """
    listeInstances = []
    line = []
    with open(filename, "r", encoding = "utf-8") as file :
        for line in file :
            line = line.rstrip()
            line = line.split(',')
            if len(line) < 2 or len(line[len(line) - 1]) < 1:
                continue
            if any(re.match(r"I.*", line[len(line) - 1]) for string in line):
                newTuple = tuple((line[:len(line) - 1]))
            else : 
                newTuple = tuple((line[:len(line)]))
            newInstance = Instance(line[len(line) - 1], newTuple)
            listeInstances.append(newInstance)
    return listeInstances

def predict(listeInstancesConnues, listeInstancesInconnues, k) :
    """
    Méthode qui prédit la catégorie de chaque instance dans une liste sans catégorie

    Arguments :
        listeInstancesConnues (liste) = Liste d'instances avec les catégories
        listeInstancesInconnues (liste) Liste d'instances sans catégories

    Renvois :
        None
    """
    for unknownInstance in listeInstancesInconnues :
        unknownInstance.cat = classify_instance(k, unknownInstance, listeInstancesConnues)

def eval_classif(ref_instances, pred_instances) :
    """
    Méthode qui évalue le pourcentage de catégorie qui sont identiques, 
        instance par instance.

    Arguments : 
        ref_instances (liste) = Liste d'instances que nous n'avons pas prédit
        pred_instances (liste) = Liste d'instances dont nous avons prédit les catégories
        same (int) = Le nombre de fois où chaque instance est identique
    
    Renvois :
        Le pourcentage en float du nombre de catégories identiques
    """
    same = 0
    for instance in pred_instances :
        for refInstance in ref_instances :
            if instance.cat == refInstance.cat and instance.coords == refInstance.coords :
                same += 1
                break
    return (same / float(len(ref_instances))) * 100.0

def mixAndSplit(filename) :
    """
    Methode qui prend le fichier initial 
        et qui le sépare en 2 fichiers
            avec chaque ligne mélangée
    
    Arguments :
        filename (file) = Fichier que l'on va lire
        fileContent (liste) = Liste contenant chaque instance 
            qui sera ensuite slice en 2
        halfContent (liste) = Liste avec la moitié des instances de fileContent
        half (int) = La longueur de fileContent divisé par 2

    Renvois :
        None
    """
    fileContent = []
    with open(filename, "r", encoding = "utf-8") as file :
        for line in file :
            if len(line) > 0 :
                fileContent.append(line)
    shuffle(fileContent)
    half = int(len(fileContent) / 2)
    writeContentToFile("part1.data", fileContent[:half])
    halfContent = fileContent[half:]
    for i in range(len(halfContent)) :
        halfContent[i] = re.sub(r",I.*", "", halfContent[i])
    writeContentToFile("part2.data", halfContent)

def writeContentToFile(filename, content) :
    """
    Méthode qui prend un fichier et qui écrit dedans

    Arguments :
        filename (file) = Fichier dans lequel nous allons écrire.
    
    Renvois :
        None
    """
    with open(filename, "w", encoding = "utf-8") as file :
        file.writelines(content)

def feature(w) :
    """
    Méthode qui va attribuer une coordonée 
        en fonction du premier mot de la liste

    Arguments :
        w (str) = Le mot que l'on va annalyser

    Renvois :
        Un nombre entre 0 et 1
    """
    detList = ["Le", "La", "Les", "Des", "Du"]
    pronList = ["Je", "Tu", "Il", "Nous", "Vous", "Ils"]
    coord = 0

    if w in detList :
        coord = 1
    return coord

def compute_coords(wordList) :
    """
    Méthode qui donne les coordonnées de chaque mot de la liste
    
    Arguments :
        wordList (liste) = Liste de mots
        coords (liste) = Liste des coordonées que l'on 
            va récupérer avec la méthode feature()
    
    Renvois :
        Les coordonnées en tuple
    """
    coords = []
    for word in wordList :
        coords.append(feature(word))

    return tuple(coords)

def read_word_instances(filename) :
    """
    Méthode qui va lire le fichier texte et le renvoyer en liste d'instances

    Arguments :
        filename (file) = Fichier que l'on va lire
        listeInstances (liste) = Liste d'instance 
            que nous allons récuper dans cette méthode
        
    Renvois :
        Une liste d'instances
    """
    listeInstances = []
    with open (filename, "r", encoding = "utf-8") as file :
        for line in file :
            line = line.rstrip()
            words = re.split(r'\t+', line)
            coords = compute_coords(words[1:])
            newInstance = Instance(words[0], coords)
            listeInstances.append(newInstance)
    return listeInstances
    