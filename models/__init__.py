from .users import create_users_table, add_users_constraints
from .branches import create_branches_table, add_branches_constraints
from .roles import create_roles_table
from .clinics import create_clinics_table
from .patients import create_patients_table
from .companies import create_companies_table
from .appointments import create_appointments_table
from .allotments import create_allotments_table

def create_all_tables(cur):
    try:
        cur.execute("BEGIN;")
        create_roles_table(cur)
        create_clinics_table(cur)
        create_branches_table(cur)
        create_users_table(cur)
        create_patients_table(cur)
        create_companies_table(cur)
        create_appointments_table(cur)
        create_allotments_table(cur)
        print("Tabelas criadas com sucesso!")

        add_branches_constraints(cur)
        add_users_constraints(cur)
        print("Constraints adicionadas com sucesso!")

        cur.execute("COMMIT;")
    except Exception as e:
        cur.execute("ROLLBACK;")
        print(f"Erro ao criar tabelas: {e}")
        raise

def drop_all_tables_cascade(cur):
    try:
        cur.execute("BEGIN;")
        
        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
        cur.execute("DROP TABLE IF EXISTS branches CASCADE;")
        cur.execute("DROP TABLE IF EXISTS clinics CASCADE;")
        cur.execute("DROP TABLE IF EXISTS roles CASCADE;")
        cur.execute("DROP TABLE IF EXISTS patients CASCADE;")
        cur.execute("DROP TABLE IF EXISTS companies CASCADE;")
        cur.execute("DROP TABLE IF EXISTS appointments CASCADE;")
        cur.execute("DROP TABLE IF EXISTS allotments CASCADE;")
        
        cur.execute("COMMIT;")
        print("Todas as tabelas excluídas com sucesso usando CASCADE!")
        
    except Exception as e:
        cur.execute("ROLLBACK;")
        print(f"Erro ao excluir tabelas: {e}")
        raise