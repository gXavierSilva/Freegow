from .users import create_users_table

def create_all_tables(cur):
    create_users_table(cur)