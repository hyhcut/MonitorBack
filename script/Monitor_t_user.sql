create table t_user
(
  id        int auto_increment
    primary key,
  username  varchar(20)  not null,
  password  varchar(255) null,
  power_id  int          null,
  last_time datetime     null,
  constraint username
    unique (username),
  constraint t_user_ibfk_1
    foreign key (power_id) references d_power (code)
);

create index power_id
  on t_user (power_id);

INSERT INTO Monitor.t_user (id, username, password, power_id, last_time) VALUES (1, 'hyh', 'pbkdf2:sha256:50000$rR3OpbN4$cfdd8d8c55ac49652f0f61ea7c66cb2c1a4b505d5651587b7d54eee8830ecee0', 999, '2019-02-13 21:11:18');