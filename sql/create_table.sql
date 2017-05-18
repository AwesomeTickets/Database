drop table if exists Cinema;

drop table if exists CinemaHall;

drop table if exists Country;

drop table if exists Movie;

drop table if exists MovieOnShow;

drop table if exists MovieStatus;

drop table if exists MovieStyle;

drop table if exists MovieType;

drop table if exists R_Movie_MovieStyle;

drop table if exists Seat;

drop table if exists Ticket;

drop table if exists User;

create table Cinema
(
   cinema_id            int not null auto_increment,
   cinema_name          varchar(30) not null comment '影院名',
   cinema_addr          varchar(50) not null comment '影院地址',
   primary key (cinema_id)
)
engine = InnoDB
default character set = utf8;

alter table Cinema comment '影院';

create table CinemaHall
(
   cinema_hall_id       int not null auto_increment,
   cinema_id            int not null,
   hall_name            varchar(10) not null comment '影厅名',
   seat_layout          varchar(400) not null comment '表示座位分布的01串',
   primary key (cinema_hall_id),
   constraint FK_R_CinemaHall_Cinema foreign key (cinema_id)
      references Cinema (cinema_id) on delete cascade on update cascade
)
engine = InnoDB
default character set = utf8;

alter table CinemaHall comment '影厅';

create table Country
(
   country_id           int not null auto_increment,
   country_name         varchar(6) not null comment '国家名',
   primary key (country_id)
)
engine = InnoDB
default character set = utf8;

alter table Country comment '国家';

create table MovieStatus
(
   movie_status_id      int not null auto_increment,
   status_name          varchar(4) not null comment '电影状态名（“正在上映”、”即将上映“等）',
   primary key (movie_status_id)
)
engine = InnoDB
default character set = utf8;

alter table MovieStatus comment '电影状态';

create table MovieType
(
   movie_type_id        int not null auto_increment,
   type_name            varchar(8) not null comment '电影类型名（”2D“、”3D“等）',
   primary key (movie_type_id)
)
engine = InnoDB
default character set = utf8;

alter table MovieType comment '电影类型';

create table Movie
(
   movie_id             int not null auto_increment,
   movie_type_id        int not null,
   country_id           int not null,
   movie_status_id      int not null,
   pub_date             date not null comment '首映日期',
   title                varchar(10) not null comment '电影标题',
   rating               decimal(2,1) not null default 0.0 comment '电影评分',
   length               int not null comment '电影时长（分钟）',
   poster_small         varchar(128) comment '电影海报图片（小尺寸）URL',
   poster_large         varchar(128) comment '电影海报图片（大尺寸）URL',
   primary key (movie_id),
   constraint FK_R_Movie_Country foreign key (country_id)
      references Country (country_id) on delete cascade on update cascade,
   constraint FK_R_Movie_MovieStatus foreign key (movie_status_id)
      references MovieStatus (movie_status_id) on delete cascade on update cascade,
   constraint FK_R_Movie_MovieType foreign key (movie_type_id)
      references MovieType (movie_type_id) on delete cascade on update cascade
)
engine = InnoDB
default character set = utf8;

alter table Movie comment '电影';

create index IDX_poster_large on Movie
(
   poster_large
);

create table MovieOnShow
(
   movie_on_show_id     int not null auto_increment,
   cinema_hall_id       int not null,
   movie_id             int not null,
   show_date            date not null comment '放映日期',
   show_time            time not null comment '放映时间',
   lang                 varchar(2) not null comment '影片语言',
   price                decimal(4,1) not null comment '电影票单价',
   primary key (movie_on_show_id),
   constraint FK_R_MovieOnShow_CinemaHall foreign key (cinema_hall_id)
      references CinemaHall (cinema_hall_id) on delete cascade on update cascade,
   constraint FK_R_MovieOnShow_Movie foreign key (movie_id)
      references Movie (movie_id) on delete cascade on update cascade
)
engine = InnoDB
default character set = utf8;

alter table MovieOnShow comment '电影排期';

create unique index IDX_4_attr on MovieOnShow
(
   movie_id,
   show_date,
   cinema_hall_id,
   show_time
);

create table MovieStyle
(
   movie_style_id       int not null auto_increment,
   style_name           varchar(2) not null comment '电影风格名（”科幻“、”恐怖“等）',
   primary key (movie_style_id)
)
engine = InnoDB
default character set = utf8;

alter table MovieStyle comment '电影风格';

create table R_Movie_MovieStyle
(
   movie_id             int not null,
   movie_style_id       int not null,
   primary key (movie_id, movie_style_id),
   constraint FK_R_MovieStyle_Movie foreign key (movie_id)
      references Movie (movie_id) on delete cascade on update cascade,
   constraint FK_R_Movie_MovieStyle foreign key (movie_style_id)
      references MovieStyle (movie_style_id) on delete cascade on update cascade
)
engine = InnoDB
default character set = utf8;

create table User
(
   user_id              int not null auto_increment,
   phone_num            char(11) not null comment '手机号',
   password             char(32) not null comment '密码（哈希值）',
   remain_purchase      int not null default 99999 comment '剩余购票次数',
   primary key (user_id)
)
engine = InnoDB
default character set = utf8;

alter table User comment '用户';

create table Ticket
(
   ticket_id            int not null auto_increment,
   user_id              int not null,
   valid                bool not null default True comment '电影票是否被取出',
   code                 char(10) not null comment '取票码',
   primary key (ticket_id),
   constraint FK_R_Ticket_User foreign key (user_id)
      references User (user_id) on delete cascade on update cascade
)
engine = InnoDB
default character set = utf8;

alter table Ticket comment '电影票';

create table Seat
(
   seat_id              int not null auto_increment,
   ticket_id            int,
   movie_on_show_id     int not null,
   row                  int not null comment '座位行号',
   col                  int not null comment '座位列号',
   available            bool not null default True comment '座位是否可用（未售出）',
   primary key (seat_id),
   constraint FK_R_Seat_Ticket foreign key (ticket_id)
      references Ticket (ticket_id) on delete set null on update cascade,
   constraint FK_R_Seat_MovieOnShow foreign key (movie_on_show_id)
      references MovieOnShow (movie_on_show_id) on delete cascade on update cascade
)
engine = InnoDB
default character set = utf8;

alter table Seat comment '座位';

create index IDX_id_available on Seat
(
   movie_on_show_id,
   available
);

create unique index IDX_id_row_col on Seat
(
   movie_on_show_id,
   row,
   col
);

create unique index IDX_code on Ticket
(
   code
);

create unique index IDX_phone_num on User
(
   phone_num
);

