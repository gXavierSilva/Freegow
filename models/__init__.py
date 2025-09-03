from .users import create_users_table
from .patients import create_patients_table
from .companies import create_companies_table
from .appointments import create_appointments_table

def create_all_tables(cur):
    create_users_table(cur)
    create_patients_table(cur)
    create_companies_table(cur)
    create_appointments_table(cur)