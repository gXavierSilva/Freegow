def create_appointments_table(cur):
    cur.execute("""
        CREATE TABLE appointments (
            appointment_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            cpf CHAR(11) NOT NULL UNIQUE,
            birth DATE NOT NULL UNIQUE,
            appointment DATE NOT NULL UNIQUE,
            time TIME NOT NULL UNIQUE,
            professional_id INT,
            image_path VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)

def add_appointments_constraints(cur):
    cur.execute("""
        ALTER TABLE appointments
        ADD CONSTRAINT fk_appointments_users
        FOREIGN KEY (professional_id)
        REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
    """)