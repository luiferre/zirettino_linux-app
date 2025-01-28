import subprocess

# Esegui PyInstaller per creare l'eseguibile
subprocess.run(["pyinstaller", "--onefile", "/home/utente/projects/ZIRETTINO/LINUXAPP/ZIRE_main.py"], shell=True)