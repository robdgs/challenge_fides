-- Connect to the new database
\c login_db;
-- Create a sample table
CREATE TABLE mytable (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some initial data
INSERT INTO mytable (name) VALUES ('Sample Data 1'), ('Sample Data 2');