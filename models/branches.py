def create_branches_table(cur):
    cur.execute("""
        CREATE TABLE branches (
            branch_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            cnpj CHAR(14) NOT NULL UNIQUE,
            cep CHAR(8) NOT NULL,
            address VARCHAR(100) NOT NULL,
            manager_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)

def add_branches_constraints(cur):
    cur.execute("""
        ALTER TABLE branches
        ADD CONSTRAINT fk_branches_users
        FOREIGN KEY (manager_id)
        REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
    """)