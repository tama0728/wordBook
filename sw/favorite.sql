create table favorite
(
    id   int      not null,
    word char(30) not null,
    constraint favorite_ibfk_1
        foreign key (id) references users (id),
    constraint favorite_ibfk_2
        foreign key (word) references words (word)
);

create index id
    on favorite (id);

create index word
    on favorite (word);

