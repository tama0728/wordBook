create table wrong
(
    id   int      not null,
    word char(30) not null,
    constraint wrong_ibfk_1
        foreign key (id) references users (id),
    constraint wrong_ibfk_2
        foreign key (word) references words (word)
);

create index id
    on wrong (id);

create index word
    on wrong (word);

