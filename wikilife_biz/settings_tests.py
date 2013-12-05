# coding=utf-8

#===================================
# TESTS SETTINGS
#===================================

DB_SETTINGS = {
    "db_main_live": {"host": "localhost", "port": 27017, "name": "wikilife_main_live"},
    "db_main_edit": {"host": "localhost", "port": 27017, "name": "wikilife_main_edit"},
    "db_users": {"host": "localhost", "port": 27017, "name": "wikilife_users"},
    "db_logs": {"host": "localhost", "port": 27017, "name": "wikilife_logs"},
    "db_processors": {"host": "localhost", "port": 27017, "name": "wikilife_processors"},
    "db_crawler": {"host": "localhost", "port": 27017, "name": "wikilife_crawler"},
    "db_admin": {"host": "localhost", "port": 27017, "name": "wikilife_admin"}
}

QUEUE_LOGS = {"host": "localhost", "port": 5672, "name": "log_queue"}
