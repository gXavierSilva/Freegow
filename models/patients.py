def create_patients_table(cur):
    cur.execute("""
        CREATE TABLE patients (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            cpf INT(11) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)