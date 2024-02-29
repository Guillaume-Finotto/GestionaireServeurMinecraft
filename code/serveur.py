
import os
from requests import get, head
import subprocess as sp
import shutil
import tkinter as tk
import mimetypes
import zipfile
from tqdm import tqdm
from pyngrok import ngrok as ng
from threading import Thread
from pyperclip import copy
from RessourcePackManager import upload
import sys
import hashlib
import webbrowser

global url

url = False
listelement = ['Ram','Tocken']
filesize = 60000000

GETVERSIONCMD = "java -version"
CHDOSSIER = os.path.dirname(os.path.abspath(sys.argv[0]))+'\\'

PORT = 25555
APPKEY = '5qy5mdqomqx65pq'
SECRETKEY  = 'odoqu193rkpub7e'
DOSSIERJAVA = ""
Startinfo = {
    "Ram":4064,
    "NgTocken": "Entrer Votre Token Trouver sur https://dashboard.ngrok.com/login"
}
urlJava = {
 20:"https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.msi",
 7:"https://api.foojay.io/disco/v3.0/ids/de719282b4a3da09453f2d443f782f3b/redirect",
 16:"https://api.foojay.io/disco/v3.0/ids/e1a907f58837eaf147414665d74756cd/redirect",
 11:"https://api.foojay.io/disco/v3.0/ids/839ff9086f3f157b301045d170333387/redirect",
 8:"https://api.foojay.io/disco/v3.0/ids/3e8c43769dad750a0150435406d843db/redirect",
 10:"https://api.foojay.io/disco/v3.0/ids/72d8c22c9f581352f6a1709beb11ac5f/redirect",
 12:"https://api.foojay.io/disco/v3.0/ids/60a3ecdae72ba7b6a5b3ee4763560661/redirect"
 }


def ajouerUnServeur(nom, version, map=False,ram = 2048,liste_serveurs=None):
    version = str(version)
    path = CHDOSSIER+"Serv\\"+nom
    javaExePath = 'java'
    if os.path.exists(path):
        print('Ce Nom existe déja stp met un Autre Truck BG')
        return False
    os.mkdir(path)
    with open(path+'\\version.txt','w') as file:
       file.write(version)
    shutil.copy(CHDOSSIER+"resource\\server.properties",path+"\\server.properties")
    if map:
        ajouterMap(path)
    dowloadServ(version, path)
    
    installServ(path,ram,version)
    liste_serveurs.insert(tk.END, nom)
    
def obtenir_element_plus_recent(dossier):
    elements = os.listdir(dossier)
    elements = [os.path.join(dossier, element) for element in elements if os.path.isdir(os.path.join(dossier, element)) or element.endswith('.zip')]
    element_plus_recent = max(elements, key=os.path.getmtime)
    return element_plus_recent

def typeDuFichier(chemin_fichier):
    type_fichier, _ = mimetypes.guess_type(chemin_fichier)
    return type_fichier

def decompresser_zip(chemin_fichier_zip, dossier_destination):
    with zipfile.ZipFile(chemin_fichier_zip, 'r') as archive_zip:
        archive_zip.extractall(dossier_destination)
    print("Archive ZIP décompressée avec succès.")
    elements = os.listdir(dossier_destination)

    if len(elements) == 1 and os.path.isdir(os.path.join(dossier_destination, elements[0])):

        chemin_sous_dossier = os.path.join(dossier_destination, elements[0])


        for nom_fichier in os.listdir(chemin_sous_dossier):
            chemin_fichier = os.path.join(chemin_sous_dossier, nom_fichier)
            shutil.move(chemin_fichier, dossier_destination)

        os.rmdir(chemin_sous_dossier)

def ajouterMap(pathMap):
    path = pathMap+"\\world"
    CHEMINTELECHARGEMENT = getinfo(7)

    map = obtenir_element_plus_recent(CHEMINTELECHARGEMENT)
    print("Nom de la Map : ",map.split('\\')[-1])
    if zipfile.is_zipfile(map):
        decompresser_zip(map, path)
    else:
        try:
            shutil.copytree(map, path)
        except:
            print("Tu n'a pas télécharger de map, il faut qu'elle soit dans ton dossier Téléchargement")
    extraire_contenu_dossier_unique(path)
    if os.path.exists(path+"\\resources.zip"):

        ajouterRessourcePack(path,pathMap)

def extraire_contenu_dossier_unique(dossier_parent):
    # Liste tous les éléments dans le dossier parent
    elements = os.listdir(dossier_parent)
    
    # Filtrer les dossiers parmi les éléments
    dossiers = [element for element in elements if os.path.isdir(os.path.join(dossier_parent, element))]
    
    # Vérifie s'il y a exactement un seul dossier
    if len(dossiers) == 1:
        # Obtient le chemin du dossier unique
        dossier_unique = os.path.join(dossier_parent, dossiers[0])
        
        # Parcours tous les fichiers dans le dossier unique
        for element in os.listdir(dossier_unique):
            # Obtient le chemin complet de l'élément à déplacer
            chemin_source = os.path.join(dossier_unique, element)
            
            # Obtient le chemin de destination pour déplacer l'élément
            chemin_destination = os.path.join(dossier_parent, element)
            
            # Déplace l'élément dans le dossier parent
            shutil.move(chemin_source, chemin_destination)
        
        # Supprime le dossier unique maintenant qu'il est vide
        os.rmdir(dossier_unique)

def ajouterRessourcePack(chdossierWorld,chMap):
    print('RESSOURCE PACK DETECTER')
    #link = upload(chdossierWorld+"\\resources.zip",'/resources.zip',APPKEY,SECRETKEY)

   
    
    sha1_hash = hashlib.sha1()
    with open(chdossierWorld+"\\resources.zip", "rb") as file:
            # Lire le fichier par petits morceaux pour économiser la mémoire
            chunk = 0
            while chunk != b'':
                chunk = file.read(4096)
                sha1_hash.update(chunk)
    akey = getinfo(2)
    bkey = getinfo(3)
    with open(chMap+"\\server.properties", "r") as file:
        new_content = file.read()
    new_content = new_content.replace('resource-pack-sha1=', 'resource-pack-sha1='+str(sha1_hash.hexdigest()))
    print("Pour la connextion, vous pouvez utiliser les code d'acces fournie : \n AdresseMail : "+getinfo(4)+'\n MotDePasse :'+getinfo(5) )
    new_content = new_content.replace('hide-online-players=false\nresource-pack=', 'hide-online-players=false\nresource-pack='+upload(chdossierWorld+'\\resources.zip','/resources.zip',akey,bkey))

    with open(chMap+"\\server.properties", "w") as file:
        file.write(new_content)

def lancerUnServ(chdssier, ram, chexe ='java'):
    #sp.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name="BloquerPort"', 'dir=in', 'action=block', f'protocol=TCP', f'localport={25565}'])
    # Construction de la commande avec le chemin absolu du fichier JAR
    os.chdir(chdssier)
    fjar = chdssier+'\\serveur.jar'
    commande = 'java' + f' -Xms512M -Xmx{ram}M -jar "{fjar}"'

    os.system(commande)
    
def installServ(path, ram,versionMC):
    commande = 'java -jar "'+path+'\\serveur.jar"'
    
    try:
        stockinfo(0,ram)
    except:
        print('ERREUR : Valeur de la RAMp non conserver pour la prochaine ouverture')

    """
    try:

        
        # Lancement du processus
        sp.run(commande, check=True)
    
      
    except sp.CalledProcessError as e:
        print(f"Une erreur s'est produite : {e}")
        if ((str(e).count("returned non-zero exit status 1") != 0) and not dejaEreur):
            installJava(versionMC)
            installServ(path, ram,versionMC, True)
        return
    """
    shutil.copy(CHDOSSIER+'resource\\start.bat', path)
    shutil.copy(CHDOSSIER+'resource\\eula.txt', path)
    os.makedirs(path+'\\plugin')

    installJava(versionMC)
    try:        
        # Lancement du processus
        sp.run(commande, check=True)
        print("instalation du serveur completee")
    except sp.CalledProcessError as e:
        print(f"Une erreur s'est produite : {e}")
    
def dowloadJava(version):
    url = urlJava[int(version)]
    response = get(url)
    # Vérifier si la requête a réussi (code 200)
    print('Téléchargement de Java')
    if response.status_code == 200:
        # Ouvrir le fichier en mode binaire et écrire les données téléchargées
        with open("java/jdk"+str(version)+".msi", "wb") as fichier:
            fichier.write(response.content)
        print("Le fichier a été téléchargé avec succès.")
    else:
        print("La requête de téléchargement a échoué avec le code :", response.status_code)

def dowloadServ(version, emplacement):
    nbversion = str(version).split(".")[1]
    urlServMinecraft17plus = "https://download.getbukkit.org/spigot/spigot-"
    urlServMinecraft16moins = "https://cdn.getbukkit.org/spigot/spigot-"

    if int(nbversion) >=17:
        url = urlServMinecraft17plus + version + ".jar"
    else:
        url = urlServMinecraft16moins + version + ".jar"

    try :
        Requetetaille = head(url)
        taille = int(Requetetaille.headers.get("Content-Length"))
    except:
        taille=0
    print('\n\n****************************')
    print('Téléchargement du Serveur : ')
    with get(url, stream=True) as r, open(emplacement + "\\serveur.jar", "wb") as f:
        progress_bar = tqdm(total=taille, unit="B", unit_scale=True)
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                progress_bar.update(len(chunk))
        progress_bar.close()
    response = get(url)
    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:

        with open(emplacement + "\\serveur.jar", "wb") as fichier:
            fichier.write(response.content)
        print("Le Serveur été téléchargé avec succès.")
    else:
        print("Le téléchargement du serveur a échoué avec le code :", response.status_code)

def VersionMCToJava(mcversion):
    mcversion = int(mcversion)
    if(mcversion >=20):
        return 20
    elif(mcversion >=18):
       return 16 # return 17
    elif(mcversion ==17):
        return 16
    elif(mcversion ==16):
        return 11
    elif(mcversion ==15):
        return 8
    elif(mcversion ==14):
        return 8
    elif(mcversion ==13):
        return 10
    elif(mcversion ==12):
        return 8
    
    else:
        return 8

def installerJava(chemin, nbJDK):

    chJavaExe = getinfo(6)+'\\JDK'+str(nbJDK)+ '\\bin\\java.exe'
    if not os.path.exists(chJavaExe):
        sp.run("msiexec /i " + chemin + ' INSTALLDIR="'+getinfo(6)+'\\JDK'+str(nbJDK)+'"')
        
    return chJavaExe
        
def installJava(VersionMc):
    version = str(sp.run(GETVERSIONCMD,shell=True,capture_output=True, text=True))
    chJavaExe = 'java'
    McNb = str(VersionMc).split(".")[1]
    version = version.split('"')[1].split(".")[0]
    
    versionToGet = VersionMCToJava(McNb)
    chemin = CHDOSSIER+"java\\jdk"+str(versionToGet)+".msi"
    
    print(' -----Installation de JAVA '+str(versionToGet)+'----- ')
    
    print("changement des variables environement JAVA_HOME")
    os.environ['PATH'] = '%JAVA_HOME%\\bin:' + os.environ['PATH']
    DOSSIERJAVA =  getinfo(6)
    for nom_fichier in os.listdir(DOSSIERJAVA):
        if (nom_fichier.count("JDK"+str(versionToGet))>0) or (nom_fichier.count("jdk-"+str(versionToGet))>0):
            os.environ['JAVA_HOME'] = DOSSIERJAVA+"\\"+nom_fichier
            break
        return

   

    if not os.path.exists(chemin):
        print('Téléchrargement de JAVA')
        dowloadJava(versionToGet)
        chJavaExe = installerJava(chemin, versionToGet)
    
    for nom_fichier in os.listdir(DOSSIERJAVA):
        if (nom_fichier.count("JDK"+str(versionToGet))>0) or (nom_fichier.count("jdk-"+str(versionToGet))>0):
            os.environ['JAVA_HOME'] = DOSSIERJAVA+"\\"+nom_fichier
            break
        return
    
   
    return chJavaExe

def lancerLeServ(Nom, Ram, java= True):
    javaExePath = 'java'
    chemin = CHDOSSIER + "Serv\\" + Nom

    with open(chemin+'\\version.txt','r') as file:
        version = file.read()
    if java is True:
        javaExePath = installJava(str(version))
    lancerUnServ(chemin, Ram, javaExePath)
    return javaExePath

def SuprimerLeServ(Nom, liste_serveurs):
    chemin = CHDOSSIER + 'Serv\\'+ Nom
    if Nom == "" or Nom == None:
        print('selectioner un fichier a suprimer')
        return
    try:
        shutil.rmtree(chemin)
        print("Le dossier {} et son contenu ont été supprimés avec succès.".format(chemin))
        liste_serveurs.delete('active')
    except OSError as e:
        print("Une erreur est survenue lors de la suppression du dossier {} : {}".format(chemin, str(e)))

def avoirNomToutServ():
    files = os.listdir(CHDOSSIER+'Serv')
    return files


def lancerngrock():
    
    global url
    if url is False:
        print("Lancement de Ngrock (pour avoir l'adresse)")
        token = str(getinfo(1))
        conf = ng.conf.PyngrokConfig(ngrok_path=CHDOSSIER+'resource\\ngrok.exe',auth_token=token,region='eu')
        url = ng.connect(25565,'tcp',pyngrok_config=conf)
        url = url.public_url
        url = str(url)[6:]
        print('URL Copier : '+url)
        copy(url)
    else:
        print('URL Copier : '+url)
        copy(url)
    
def GetdecouperInfo():
    with open(CHDOSSIER+"resource\\variable.txt", "r") as fichier:
       tout = fichier.read()
    couper = tout.splitlines()
    full = []
    for ligne in couper:
        
        decouper = str(ligne).split(' : ')
        full.append(decouper)
        
    return full

def stockinfo(nbligne, valeur):
 try:

    info = GetdecouperInfo()
    ligneainserer = [listelement[nbligne],str(valeur)]
    info.insert(nbligne,ligneainserer)

    info.pop(nbligne+1)

    ecrire = ""
    for ligne in info:
        try:
            ecrire = ecrire + str(ligne[0])
            ecrire = ecrire +" : " 
            ecrire = ecrire + str(ligne[1])
            ecrire = ecrire + "\n"
        except:
            pass

    with open(CHDOSSIER+"resource\\variable.txt", 'w') as fichier:
        fichier.write(ecrire)

 except:
    print('erreur dans la mise a jour du fichier variable.txt : ligne '+str(nbligne+1)+' doit avoir la valeur : '+str(valeur))
def getinfo(indexe):
    info = GetdecouperInfo()
    return info[indexe][1]


class Console(tk.Text):
    def __init__(self, master, **kwargs):
        
        super().__init__(master, **kwargs)
        self.pack(expand=True, fill="both")

    def write(self, text):
        self.insert("end", text)
        self.see("end")

    def flush(a=10):
        pass

def redirect_output(text_widget):
    sys.stdout = text_widget
    sys.stderr = text_widget


def lancerFenetre():
    
    # Création de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Gestion des serveurs Minecraft")

    # Création des widgets
    etiquette_nom = tk.Label(fenetre, text="Ajouter Un Nouveau Serveur \n\nNom du serveur:")
    etiquette_nom.pack()
    champ_nom = tk.Entry(fenetre)
    champ_nom.pack()

    etiquette_version = tk.Label(fenetre, text="Version:")
    etiquette_version.pack()
    champ_version = tk.Entry(fenetre)
    champ_version.pack()

    mape = tk.BooleanVar()
    champ_map = tk.Checkbutton(fenetre, text="Map", variable=mape)
    champ_map.pack()

    java = tk.BooleanVar()
    champ_erreur_java = tk.Checkbutton(fenetre, text="Erreur Java",variable=java)
    champ_erreur_java.pack()

    bouton_ajouter = tk.Button(fenetre, text="Ajouter", command=lambda: Thread(target=ajouerUnServeur,args=(champ_nom.get(), champ_version.get(),mape.get(),Ram.get(), liste_serveurs)).start())
    bouton_ajouter.pack()

    etiquette_liste_serveurs  = tk.Label(fenetre, text="\n\n\nServeurs disponibles:")
    etiquette_liste_serveurs.pack()
    liste_serveurs = tk.Listbox(fenetre)
    liste_serveurs.pack()

    # Remplir la liste des serveurs disponibles
    serveurs_disponibles = avoirNomToutServ()
    for serveur_disponible in serveurs_disponibles:
        liste_serveurs.insert(tk.END, serveur_disponible)

    etiquette_RAM = tk.Label(fenetre, text="Ram:")
    etiquette_RAM.pack()

    DefaultRam = getinfo(0)
    Ram = tk.Entry(fenetre,justify="center")
    Ram.insert(0,str(DefaultRam))
    Ram.pack()

    bouton_lancer = tk.Button(fenetre, text="Lancer", command=lambda: Thread(target=lancerLeServ,args=(liste_serveurs.get(tk.ACTIVE),Ram.get(), java.get())).start())
    bouton_lancer.pack()

    bouton_supprimer = tk.Button(fenetre, text="Supprimer", command=lambda: Thread(target=SuprimerLeServ, args=(liste_serveurs.get(tk.ACTIVE),liste_serveurs)).start())
    bouton_supprimer.pack()


    bouton_ng = tk.Button(fenetre, text="Copier le lien", command=lambda: Thread(target=lancerngrock).start())
    bouton_ng.pack()

    #pas encore implementer (console integrer)
    #console = Console(fenetre, wrap="word", bg="white", fg="black",border=5,borderwidth=5)

# Rediriger la sortie de la console vers le widget Label
    #redirect_output(console)


    fenetre.minsize(300,500)
    fenetre.mainloop()

def verifToken():
    

    if os.path.exists(CHDOSSIER+"resource\\t.txt"):
        stockinfo(1,Startinfo["NgTocken"])
        os.remove(CHDOSSIER+"resource\\t.txt")

    token = getinfo(1)
    if (token == "") or (token == Startinfo["NgTocken"] ) :
        print("\nErreur durant l'ouverture de NgRok, Token Invalide")
        print('Il  faut le changer dans : Resource/variable.txt \n')
        return False
    else:
        return True


def Main():
     
    if verifToken():
        lancerFenetre()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

Main()