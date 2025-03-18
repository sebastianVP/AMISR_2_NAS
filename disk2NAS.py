"""
Autor: Alexander Valdez
AKA: Magic 
Fecha de creación: [18/03/2025]
Descripción: [ENVIO DE DATA ISR-ESF A NAS AMISR-14]
Versión: [1.0]
"""

import os
import shutil
import logging
from datetime import datetime
from tqdm import tqdm

def detectMode(source_path):
    """
    Método para detectar si el modo es ISR o ESF.
    Busca dentro de la carpeta Setup si existen archivos que inicien con ISR o ESF.
    """
    setup_path = os.path.join(source_path, "Setup")
    if not os.path.exists(setup_path):
        print("Error: No se encontró la carpeta Setup en el directorio de origen.")
        return "Desconocido"
    
    for filename in os.listdir(setup_path):
        if filename.startswith("ISR"):
            return "ISR"
        elif filename.startswith("ESF"):
            return "ESF"
    
    print("Advertencia: No se encontró ningún archivo que indique ISR o ESF.")
    return "Desconocido"

def copy_with_progress(source_path, destination_path):
    """
    Copia los archivos de source_path a destination_path mostrando una barra de progreso.
    """
    """
    Copia los archivos de source_path a destination_path mostrando una barra de progreso.
    """
    files_list = []
    dirs_list = []
    
    for root, dirs, files in os.walk(source_path):
        #print("WALK:",os.walk(source_path))
        rel_path = os.path.relpath(root, source_path)
        #print("rel_path",rel_path)        
        dest_dir = os.path.join(destination_path, rel_path)
        dirs_list.append(dest_dir)
        
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            files_list.append((src_file, dest_file))
    #print("CHECK:",files_list)
    # Crear directorios primero
    for dir in dirs_list:
        os.makedirs(dir, exist_ok=True)
    
    # Copiar archivos con progreso
    with tqdm(total=len(files_list), desc="Copiando archivos", unit="archivo") as pbar:
        for src_file, dest_file in files_list:
            os.system(f'cp "{src_file}" "{dest_file}"')
            logging.info(f"Copiado: {src_file} -> {dest_file}")
            pbar.update(1)

def move_data(source_path):
    print("[INICIO DE LA SECUENCIA]")
    print("SOURCE PATH:", source_path)
    logging.basicConfig(filename="/home/soporte/Documents/AMISR_SCRIPT_NAS/transfer.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    if not os.path.exists(source_path):
        print(f"Error: La ruta de origen {source_path} no existe.")
        logging.error(f"La ruta de origen {source_path} no existe.")
        return
    
    # Extraer la parte relevante del path
    path_parts = source_path.split("/AMISR/")
    print("PARTES RELEVANTES:", path_parts)
    if len(path_parts) < 2:
        print("Error: La estructura del directorio no es válida.")
        return
    
    relative_path = path_parts[1]  # 2024/20250101.001

    print("RELATIVE_PATH",relative_path)
    print(relative_path.split("/")[1][0:4], relative_path.split("/")[1])
    year, folder_name = relative_path.split("/")[1][0:4], relative_path.split("/")[1]
    
    # Obtener el mes y año en formato adecuado
    date_obj = datetime.strptime(folder_name[:8], "%Y%m%d")
    formatted_month = date_obj.strftime("%Y_%m")
    print("FORMATTED-MONTH",formatted_month)    
    
    # Detectar el modo
    mode = detectMode(source_path)
    print("Mode:",mode)
    if mode== "Desconocido":
        logging.error("No se pudo determinar el modo, abortando la operación.")
        return
    # Construir la ruta de destino
    destination_base = f"/run/user/1000/gvfs/smb-share:server=10.10.20.21,share=data-amisr/{formatted_month}/{mode}/amisr_radar/rawdata"
    destination_path = os.path.join(destination_base, folder_name)
    print("DESTINATION_PATH:",destination_path)
    #import time
    #time.sleep(10)
    # Crear directorios si no existen
    os.makedirs(destination_path, exist_ok=True)
    
    # Copiar datos con progreso
    copy_with_progress(source_path, destination_path)
    logging.info(f"Datos movidos exitosamente a {destination_path}")
    print(f"Datos movidos exitosamente a {destination_path}")

if __name__ == "__main__":
        #source_path = input("Ingrese la ruta de los datos de origen: ")
    #source_path = "/run/user/1000/gvfs/smb-share:server=10.10.20.21,share=expansion/AMISR/2024/20250102.002"
    #-------------------------------------MODIFICAR RUTA SI CAMBIAMOS EL DISCO-----------------------#
    directory   = "/run/user/1000/gvfs/smb-share:server=10.10.20.21,share=expansion/AMISR/2024"
    #------------------------------------MODIFICAR EL DIA --------------------------------------------#
    dir_doy     = "20250103.00"
    list_dir_path= [os.path.join(directory,f"{dir_doy}{i}") for i in range(1,6)]
    for source_path in list_dir_path:
        print("-----------------------------------------------------")
        move_data(source_path)
