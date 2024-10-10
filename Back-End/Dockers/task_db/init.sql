-- Connect to the new database
\c task_db;

-- Create a sample table

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
	"name" VARCHAR(100),
	"description" VARCHAR(500)
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
	id_category INTEGER REFERENCES categories(id),
	"name" VARCHAR(100),
	"description" VARCHAR(500),
	previous_task INTEGER REFERENCES tasks(id),
	next_task INTEGER REFERENCES tasks(id),
	duration TIMESTAMP
);

CREATE TABLE progresses (
    id SERIAL PRIMARY KEY,
	id_task INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
	id_user INTEGER,
	pregession_rate NUMERIC(6, 3),
	joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some initial data
INSERT INTO categories ("name", "description")
VALUES
	('sport', 'prenditi cura del tuo corpo'),
	('art', 'attivita` artistiche'),
	('culture', 'attivita` culturali'),
	('alimentation', 'cura la tua alimentazione'),
	('mental', 'migliora il tuo equilibrio mentale');

-- Insert some initial data
INSERT INTO takss (id_category, "name", "description", previous_task, next_task, duration)
VALUES
	(1, 'step by step', 'walking is a simple basic way to improve your health', 0, 0, 0);