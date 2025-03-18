**REPOSITORIO Y SCRIPT DE COPIADO DE DATOS DE DISCO AL NAS DE AMISR-14**

Desarrollo de un script que permita ubicar los datos de AMISR en directorios correspondientes a ISR y ESF.

* La estructura es la siguiente:

SOURCE_PATH: /run/user/1000/gvfs/smb-share:server=10.10.20.21,share=expansion/AMISR/2024/20250102.001

* Los Destinos pueden ser los siguientes:

	Opcion1: /run/user/1000/gvfs/smb-share:server=10.10.20.21,share=data-amisr/2025_01/ISR/amisr_radar/rawdata/20250102.001
	Opcion2: /run/user/1000/gvfs/smb-share:server=10.10.20.21,share=data-amisr/2025_01/ESF/amisr_radar/rawdata/20250102.001

* El programa debe revisar internamente el contenido de una carpeta denominada Setup e identificar el experimento correspondiente.


* El script desarrollado se llama disk2NAS.py








