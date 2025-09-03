def create_companies_table(cur):
    cur.execute("""
        CREATE TABLE companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            plan VARCHAR(100) NOT NULL,
            exam VARCHAR(100) NOT NULL,
            value DECIMAL(8, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)