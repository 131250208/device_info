SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for iie_device_spider_record
-- ----------------------------
DROP TABLE IF EXISTS `iie_device_spider_record`;
CREATE TABLE `iie_device_spider_record` (
  `id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `source` varchar(255) NOT NULL COMMENT '记录来源：网站名称或文件名称',
  `source_type` ENUM('file', 'web_site') NOT NULL,
  `record_type_list` varchar(255) NOT NULL COMMENT '记录内容列表：品牌，类型，型号',
  `spider_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间或上传时间',
  `record_num` INT UNSIGNED NOT NULL COMMENT '文件包含的记录数目',
  `record_file_path` VARCHAR(255) NOT NULL COMMENT '文件存储路径',
  `status` ENUM('handled', 'unhandled') NOT NULL COMMENT '文件处理状态',
  `handled_num` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '已处理记录数目',
  `handled_time` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '上次处理文件时间',
  `saved_num` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '存入数据库记录数目',
  `valid_num` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '有效记录数目'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
