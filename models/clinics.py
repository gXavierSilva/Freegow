def create_clinics_table(cur):
    cur.execute("""
        CREATE TABLE clinics (
            clinic_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            cnpj CHAR(14) NOT NULL UNIQUE,
            street VARCHAR(100) NOT NULL,
            number CHAR(10) NOT NULL,
            city VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)