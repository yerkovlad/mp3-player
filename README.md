# mp3-player

h1 Mp3-Player

h2 About Program
***
This is an mp3-player where you can create accounts, download music from the Internet and listen to it
***

IMPORTANT
========
In file [global_database/con_to_mon_db_serv.py](https://github.com/yerkovlad/mp3-player/blob/main/global_database/con_to_mon_db_serv.py).
In the 7th line, client_con, pay attention to the link, there are parameters, **YOURMONGOLOGIN** - the login of the mongodb account, **YOURMONGOPASSWORD** - the password of the account and **YOURMONGODBNAME** - and the name of the table, or you can simply replace this entire field with your link with the Mongodb database
========

What in the all files:
============
File name                                   | Contents of the file
--------------------------------------------|--------------------------------------------------------------------------
main.py                                     | The main code of the project, and the main window
account_information.py                      | The file displays user account information, ***username and password***
database_fl/connect_to_database.py          | The file contains functions for working with a local database
global_database/con_to_mon_db_serv.py       | The file contains functions for working with a global database
login/log.py                                | The file displays a window for logging into the account
registration/registr.py                     | The file displays a window for registering an account
widget_down_files/widget_download.py        | Window to download music
================

![Image](https://github.com/yerkovlad/mp3-player/blob/main/images/image.png)
