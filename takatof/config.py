import os

SECRET_KEY = "8c344795eb9dcaae0797ebd7c9820ea0"
DB_URI = os.environ['DATABASE_URL']
BUILDING_ROOM_LIST = list(map(str, list(range(101,136)) + list(range(201,236)) + list(range(301,336))))
HIDE_AFTER_ONE_MONTH = True

