DROP TABLE IF EXISTS scores;

CREATE TABLE scores (
  id INTEGER PRIMARY KEY,
  plname TEXT UNIQUE NOT NULL,
  points INTEGER NOT NULL
);