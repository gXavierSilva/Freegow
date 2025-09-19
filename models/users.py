def create_users_table(cur):
    cur.execute("""
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(60) NOT NULL,
            role_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (role_id)
                REFERENCES roles(role_id)
                ON DELETE SET NULL
                ON UPDATE CASCADE
        );
    """)