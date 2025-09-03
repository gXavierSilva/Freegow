def create_appointments_table(cur):
    cur.execute("""
        CREATE TABLE patients (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            cpf INT(11) NOT NULL UNIQUE,
            birth DATE NOT NULL UNIQUE,
            appointment DATE NOT NULL UNIQUE,
            time TIME NOT NULL UNIQUE,
            professional VARCHAR(100) NOT NULL,
            image_path VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)