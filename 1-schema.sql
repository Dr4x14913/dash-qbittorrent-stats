--
-- Table structure for table `teams`
--
DROP TABLE IF EXISTS `torrents`;
CREATE TABLE `torrents` (
  `name`      varchar(256),
  `uploaded`  varchar(256),
  `downloaded`varchar(256),
  `ratio`     varchar(256),
  `size`      varchar(256),
  `day`       varchar(30),
  PRIMARY KEY (`name`, `day`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

