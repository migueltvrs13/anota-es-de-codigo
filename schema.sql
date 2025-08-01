
drop table if exists users;

create table if not exists users (
    id integer primary key autoincrement,
    nome text not null,
    senha text not null,
    email text not null unique
);

create table if not exists books (
    id integer primary key autoincrement,
    titulo text not null,
    user_id integer references users
);

create table if not exists filmes (
    id integer primary key autoincrement,
    titulo text not null,
    user_id integer references users
)