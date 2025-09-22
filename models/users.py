def create_users_table(cur):
    cur.execute("""
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(60) NOT NULL,
            role_id INT,
            clinic_id INT,
            branch_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)

def add_users_constraints(cur):
    cur.execute("""
        ALTER TABLE users
        ADD CONSTRAINT fk_users_roles
            FOREIGN KEY (role_id)
            REFERENCES roles(role_id)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
        ADD CONSTRAINT fk_users_clinics
            FOREIGN KEY (clinic_id)
            REFERENCES clinics(clinic_id)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
        ADD CONSTRAINT fk_users_branches
            FOREIGN KEY (branch_id)
            REFERENCES branches(branch_id)
            ON DELETE SET NULL
            ON UPDATE CASCADE;
    """)