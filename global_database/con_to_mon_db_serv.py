from pymongo import *
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from database_fl.connect_to_database import *

client_con = MongoClient(f"mongodb+srv://yerkovlad:02012009@cluster0.g3oloqa.mongodb.net/?retryWrites=true&w=majority")

db = client_con['Main_database']

collection = db['users']

def write_to_mndb(username : str, password : str, list_musics_inp : list=[]):
    """
    The function write information from user in global database
    """
    dict_inp = {
    'username' : username,
    'password' : password,
    'musics' : list_musics_inp}
    try:
        collection.replace_one(collection.find_one({'$and' : [{'username':username},{'password':password}]}), dict_inp)
    except:
        collection.insert_one(dict_inp)

def read_from_mndb(username : str, password : str, write_to_sqlitedb : bool=False, ret_username : bool=False):
    """
    The function read information from user in global database,
    if write_to_sqlitedb == True:
        function write information from users music, write to local database
    elif ret_username == True and write_to_sqlitedb == False:
        return information from some user
    else:
        return col_with_user
    """
    col_with_user = collection.find_one({'$and' : [{'username':username},{'password':password}]})
    all_music_names_in_sqlitedb_list = list()
    if write_to_sqlitedb == True:
        for el in Musics.select():
            all_music_names_in_sqlitedb_list.append(el.music_name)
        for el in col_with_user['musics']:
            if not el['music_name'] in all_music_names_in_sqlitedb_list:
                Musics.create(artist=el['artist'], music_name=el['music_name'], mp3_file=el['mp3_file'])
    else:
        if ret_username == True:
            return collection.find_one({'username' : username})
        else:
            return col_with_user