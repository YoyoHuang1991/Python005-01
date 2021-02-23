use db1;
show tables;
select * from T;

-- class 04
create table T04(
id int primary key, 
k int not null, 
name varchar(16),
index (k))engine=InnoDB;
insert into T04 values(100,1,'yoyo'),(200,2,'yoyo2'),(300,3,'yoyo3'),(500,5,'yoyo4'),(600,6,'yoyo5');
select k from T04 where k=2;
delete from T04 where k=3;
-- 重建index
alter table T04 drop index k;
alter table T04 add index(k);
-- 重建主鍵，“尽量使用主键查询”原则，直接将这个索引设置为主键，可以避免每次查询需要搜索两棵树。
alter table T04 drop primary key;
alter table T04 add primary key(id);
-- 重建主鍵，節省空間，應將上兩句改為
alter table T04 engine=InnoDB;

-- 1. 新增table T，以及插入7筆資料，k為index是一B+樹 
create table T (
	ID int primary key,
	k int NOT NULL DEFAULT 0, 
	s varchar(16) NOT NULL DEFAULT '',
	index k(k))
	engine=InnoDB;
-- 插入資料
insert into T values(100,1, 'aa'),(200,2,'bb'),(300,3,'cc'),(500,5,'ee'),(600,6,'ff'),(700,7,'gg');

-- 2. 新增table 'tuser'，
CREATE TABLE `tuser` (
  `id` int(11) NOT NULL,
  `id_card` varchar(32) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `ismale` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_card` (`id_card`),
  KEY `name_age` (`name`,`age`)
) ENGINE=InnoDB;


insert into tuser values(1,'H123','李四', 24, 1),
	(2,'H224','王五', 20,1),
	(3,'B123','張三',10,1),
    (4,'B1223','張三',10,1),
    (5,'B123','張三',20,1);

insert into tuser values(10,'A111','張六',10,0);

select id_card from tuser where id_card like "B%";
select * from tuser where name like "張%";

