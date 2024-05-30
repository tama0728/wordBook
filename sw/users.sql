create table users
(
    id         int auto_increment
        primary key,
    username   varchar(50)      not null,
    password   varchar(255)     not null,
    admin      bit default b'0' not null,
    phone      char(14)         null,
    rain_score int              null,
    card_score int              null,
    constraint users_pk
        unique (id),
    constraint users_pk_2
        unique (id, username)
);

