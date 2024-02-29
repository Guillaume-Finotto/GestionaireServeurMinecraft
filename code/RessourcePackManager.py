import dropbox
import os
from webbrowser import open as wbopen
def getRetoken(APP_KEY,APP_SECRET):
    
# Créer un objet DropboxOAuth2FlowNoRedirect pour le flux d'authentification
    flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

    # Générer l'URL d'autorisation pour rediriger l'utilisateur
    authorize_url = flow.start()
    # Demander à l'utilisateur de se connecter et d'autoriser l'application
    print("Veuillez visiter cette URL pour vous connecter et autoriser l'application :", authorize_url)
    wbopen(authorize_url)
    auth_code = input("Copiez le code d'autorisation affiché après l'autorisation : ")
    print('CODE RESSUS')
    # Obtenir le jeton d'accès initial et le jeton de rafraîchissement
    end = flow.finish(auth_code)
    print("Code Accepté")
    return str(end).split(',')[0].split('(')[1]


def upload_large_file(file_path, destination_path,dbx, chunk_size=4 * 1024 * 1024):
    """Télécharge un fichier volumineux en utilisant des sessions d'upload."""
    print("envoie du gros ressource pack")

    # Ouverture du fichier en mode lecture binaire
    with open(file_path, "rb") as file:
        file_size = os.path.getsize(file_path)

        if file_size <= chunk_size:
            # Le fichier est petit, utilisez files_upload pour le télécharger
            dbx.files_upload(file.read(), destination_path, mode=dropbox.files.WriteMode.overwrite)
            print("Fichier téléchargé avec succès (méthode simple) :", destination_path)
        else:
            # Le fichier est gros, utilisez files_upload_session pour le télécharger par blocs
            upload_session_start_result = dbx.files_upload_session_start(file.read(chunk_size))

            cursor = dropbox.files.UploadSessionCursor(
                session_id=upload_session_start_result.session_id,
                offset=file.tell()
            )
            commit = dropbox.files.CommitInfo(path=destination_path,mode=dropbox.files.WriteMode.overwrite)

            # Continuation de l'upload en utilisant des blocs de données
            while file.tell() < file_size:
                if (file_size - file.tell()) <= chunk_size:
                    # Dernier bloc de données
                    dbx.files_upload_session_finish(file.read(chunk_size),
                                                    cursor,
                                                    commit)
                else:
                    # Bloc de données intermédiaire
                    dbx.files_upload_session_append(file.read(chunk_size),
                                                    cursor.session_id,
                                                    cursor.offset)
                    cursor.offset = file.tell()

            print("Fichier téléchargé avec succès (méthode sessions) :", destination_path)

def upload_file(file_path, destination_path,dbx):
    """Télécharge un fichier en utilisant la méthode simple files_upload."""
    print("Envoie du ressource PAck")
    
    # Ouverture du fichier en mode lecture binaire
    with open(file_path, "rb") as file:
        dbx.files_upload(file.read(), destination_path,mode=dropbox.files.WriteMode.overwrite)
        print("Fichier téléchargé avec succès (méthode simple) :", destination_path)

def upload(local_file_path, destination_path, appKey,SecKey):
    token = getRetoken(appKey,SecKey)
    dbx = dropbox.Dropbox(token)
    # Choix de la méthode en fonction de la taille du fichier
    if os.path.getsize(local_file_path) <= 4 * 1024 * 1024:
        upload_file(local_file_path, destination_path,dbx)
    else:
        upload_large_file(local_file_path, destination_path, dbx)
    return create_shared_link(destination_path, dbx)

def create_shared_link(file_path, dbx):
    """Crée     return shared_link.url.replace("dl=0", "dl=1")
un lien partagé pour le téléchargement d'un fichier."""
    
    shared_link = dbx.files_get_temporary_link(file_path)
    shared_link = str(shared_link).split("'")[1]
    return shared_link
