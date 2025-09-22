def create_allotments_table(cur):
    cur.execute("""
        CREATE TABLE allotments (
            allotment_id SERIAL PRIMARY KEY,
            value DECIMAL(8, 2) NOT NULL,
            type VARCHAR(100) NOT NULL,
            agreement VARCHAR(100),
            status VARCHAR(100) NOT NULL,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    """)