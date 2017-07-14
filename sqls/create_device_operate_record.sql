SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for iie_device_operate_record
-- ----------------------------
DROP TABLE IF EXISTS `iie_device_operate_record`;
CREATE TABLE `iie_device_operate_record` (
  `id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `table_name` ENUM('iie_device_brand','iie_device_type','iie_device_model','iie_banner') NOT NULL COMMENT '操作表名',
  `record_id` INT UNSIGNED NOT NULL COMMENT '操作记录的id',
  `operate_time` TIMESTAMP NOT NULL COMMENT '操作的时间',
  `source` ENUM('relic', 'file','web_site','manual') NOT NULL DEFAULT 'relic' COMMENT '数据来源类型',
  `description` VARCHAR(255) NOT NULL DEFAULT 'insert' COMMENT '操作描述',
  `spider_id` INT UNSIGNED DEFAULT NULL COMMENT '来源为file或web_site的，爬取记录id，其他来源的为NULL',
  FOREIGN KEY (spider_id) REFERENCES iie_device_spider_record(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
