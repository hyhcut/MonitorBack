create table d_power
(
  id   int auto_increment
    primary key,
  code int          not null,
  name varchar(255) null,
  constraint code
    unique (code)
);

INSERT INTO Monitor.d_power (id, code, name) VALUES (1, 999, '管理员');