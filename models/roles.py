def create_roles_table(cur):
    cur.execute("""
        CREATE TABLE roles (
            role_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            access VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)