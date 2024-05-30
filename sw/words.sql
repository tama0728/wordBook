create table words
(
    id   int auto_increment
        primary key,
    word varchar(30)  not null,
    mean varchar(150) not null,
    lv   int(4)       not null,
    constraint words_pk
        unique (word)
);

