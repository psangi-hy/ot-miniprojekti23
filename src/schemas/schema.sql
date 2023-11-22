CREATE TABLE articles(
    id INTEGER PRIMARY KEY,
    key VARCHAR (40) UNIQUE,
    author VARCHAR (100),
    title VARCHAR (200),
    journal VARCHAR (200),
    year INTEGER,
    volume VARCHAR (100),
    pages VARCHAR (50)
);
