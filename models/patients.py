def create_patients_table(cur):
    cur.execute("""
        CREATE TABLE patients (
            patient_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            cpf CHAR(11) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)