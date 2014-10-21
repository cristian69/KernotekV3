drop table if exists entries;
create table usuarios(
    id integer primary key autoincrement,
    nombre text not null,
    password text not null
);
