create table d_power
(
  id   int auto_increment
    primary key,
  code int          not null,
  name varchar(255) null,
  constraint code
    unique (code)
);

INSERT INTO monitor.d_power (id, code, name) VALUES (1, 999, '超级管理员');
INSERT INTO monitor.d_power (id, code, name) VALUES (2, 1, '用户');