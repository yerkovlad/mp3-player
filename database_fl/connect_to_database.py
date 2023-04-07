from peewee import *
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
db = SqliteDatabase('database_fl/database.sqlite')

class Musics(Model):
    """
    The class that create table in database,
    where will all musics and information about music
    """
    artist = TextField()
    music_name = TextField()
    mp3_file = DateField()

    class Meta:
        database = db

class Account(Model):
    """
    The class that create table in database,
    where will all information about account
    """
    username = TextField()
    password = TextField()

    class Meta:
        database = db

def files_in_dir(dir):
    """
    The function return all files name in some directory
    """
    for root, dirs, files in os.walk(f"{dir}"):  
        pass
    return files

def write_to_database(name_dir_with_mus : str, dir_inp : dict):
    """
    The function write information to database in Musics table
    """
    musics_files_name_list = files_in_dir(name_dir_with_mus)

    for el in musics_files_name_list:
        with open(f'{name_dir_with_mus}/{el}', 'rb') as fl:
            br_file = fl.read()
        Musics.create(artist=dir_inp['artist'], music_name=dir_inp['title'], mp3_file=br_file)

def read_from_mus_table():
    """
    The function read all information from Musics table
    and return list with dictionary with information from music
    """
    list_out = list()

    for el in Musics.select():
        list_out.append({'music_name' : el.music_name, 'artist' : el.artist, 'mp3_file' : el.mp3_file})

    return list_out

def write_ac_inf_to_database(username : str, password : str):
    """
    This function write information from user(username and password) in Account table
    """
    try:
        Account[1].delete_instance()
    except:
        pass
    Account.create(username=username, password=password)

def read_from_ac_inf_to_database():
    """
    This function read information from user(username and password) in Account table,
    and return list with username[0] and password[1]
    """
    for el in Account.select():
        return [el.username, el.password]

try:
    Musics.create_table()
except:
    pass
try:
    Account.create_table()
except:
    pass