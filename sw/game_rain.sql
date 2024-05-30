create table game_rain
(
    id       int         not null,
    username varchar(50) not null,
    score    int         not null,
    constraint game_rain_users_id_username_fk
        foreign key (id, username) references users (id, username)
            on update cascade on delete cascade
);

