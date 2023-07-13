import sys, shutil, re
from pathlib import Path
from threading import Thread
import logging
import concurrent.futures
from time import sleep
from random import randint


dic = {'А':'A', 'а':'a', 'Б':'B', 'б':'b', 'В':'V', 'в':'v',
       'Г':'H', 'г':'h', 'Ґ':'G', 'ґ':'g', 'Д':'D', 'д':'d', 'Е':'E', 'Є':'e', 'е':'e', 'є':'e', 'Ж':'Zh', 'ж':'zh',
       'З':'Z', 'з':'z', 'И':'Y', 'и':'y', 'Й':'Y', 'й':'y', 'К':'K', 'к':'k', 'Л':'L', 'л':'l',
       'М':'M', 'м':'m', 'Н':'N', 'н':'n', 'О':'O', 'о':'o', 'П':'P', 'п':'p', 'Р':'R', 'р':'r', 
       'С':'S', 'с':'s', 'Т':'T', 'т':'t', 'У':'U', 'у':'u', 'Ф':'F', 'ф':'f', 'Х':'Kh', 'х':'kh',
       'Ц':'Tc', 'ц':'tc', 'Ч':'Ch', 'ч':'ch', 'Ш':'Sh', 'ш':'sh', 'Щ':'Shch', 'щ':'shch', 'Ю':'Iu', 'ю':'iu', 'Я':'Ia', 'я':'ia', 'Ь':'', 'ь':'',}

list_ext = []
files_list = []

path = Path(sys.argv[1])

# path = Path('D:\Розбрати')

fix_path = path

def normalize(name_):                          
    result = str()
    file_name = name_.stem
    ext = name_.suffix
    for i in range(0,len(file_name)):
        if file_name[i] in dic:
            simb = dic[file_name[i]]
        else:
            simb = file_name[i]
        result = result + simb
    new_file_name = (''.join(re.findall(r"\w+", result)))+ext
    return new_file_name


def move_and_rename(file_old_name, file_new_name, path, new_path):          
    path_file: str = f"{path}\{file_old_name}"
    path_file_new: str = f"{new_path}\{file_new_name}"
    shutil.move(path_file, path_file_new)

foldername_ext = []
def create_folders_sort_extensions(folder):      
    path_folder = path/folder
    if not path_folder.is_dir():                                
        path_folder.mkdir()
        foldername_ext.append(path_folder)

folders = []
def parse_folder(path):
    for element in path.iterdir():
        if element.is_dir():
            folders.append(element)
            parse_folder(element)
    return folders

def file_processing(path):
    for element in path.iterdir():
        if element.is_file():
            extension_file = element.suffix.upper()
            extension_file.removeprefix('.')
            try:
                create_folders_sort_extensions(extension_file)
            except OSError as e:
                logging.error(e)
            path_folder = fix_path/extension_file
            file_new_name = normalize(element)
            move_and_rename(element.name, file_new_name, path, path_folder)


def delete_empty_folders(path):    
    for element in path.iterdir():
        if element.is_dir():
            try:                
                delete_empty_folders(element)
                path_empty_folder = path/element.name
                path_empty_folder.rmdir()
                
            # except OSError as e:
                # print("Folder: %s : %s" % (path/element.name, e.strerror))
            except OSError as e:
                logging.error(e) 
            except:
                pass 
            
     
def list_files_category(folder_path):
    lst = []
    
    logging.debug(f'It is {folder_path.name} folder')
    
    for file in folder_path.iterdir():           
        lst.append(file.name)
    lst_str = ', '.join(lst)       
    return f'{folder_path.name}: {lst_str}' 


def unpack_archive(path):
    if path.is_dir():
    # if Path(path).exists():
        for archive in path.iterdir():
            archive_name = path/archive.name
            folder_name = path/archive.stem
            try:
                shutil.unpack_archive(archive_name, folder_name )
                if archive.is_dir() == False:
                    archive.unlink()
            except OSError as e:
                # print("Ошибка: %s : %s" % (archive_name, e.strerror))
                logging.error(e)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s',
        handlers=[
        logging.FileHandler("program.log"),
        logging.StreamHandler()
    ])
    logging.debug('Start program')

    threads = []
    parse_folder(path)
    for folder in folders:
        thread = Thread(target=file_processing, args=(folder,))
        thread.start()
        threads.append(thread)
  
    for folder in path.iterdir():
        thread = Thread(target=list_files_category, args=(folder,))
        thread.start()
        threads.append(thread)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(list_files_category, foldername_ext))

    print(results)

    [el.join() for el in threads]

    # path_archive_folder = path / 'archives'
    # unpack_archive(path_archive_folder)

    delete_empty_folders(path)
  
    logging.debug('End program') 




   