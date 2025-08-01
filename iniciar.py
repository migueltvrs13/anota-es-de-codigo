import sqlite3

# insert

# executar conexao
conn = sqlite3.connect('banco.db')

with open('schema.sql') as f:
    conn.executescript(f.read())

conn.close()