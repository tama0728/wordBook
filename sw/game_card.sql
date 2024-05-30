create table game_card
(
    id       int         not null,
    username varchar(50) null,
    score    int         not null,
    constraint game_card_users_id_username_fk
        foreign key (id, username) references users (id, username)
            on update cascade on delete cascade
);

