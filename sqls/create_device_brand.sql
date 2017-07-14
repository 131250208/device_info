SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for iie_device_brand
-- ----------------------------
DROP TABLE IF EXISTS `iie_device_brand`;
CREATE TABLE `iie_device_brand` (
  `id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `en_name` varchar(255) DEFAULT NULL COMMENT '品牌英文名',
  `cn_name` varchar(255) DEFAULT NULL COMMENT '品牌中文名',
  `country` varchar(255) DEFAULT NULL COMMENT '品牌所属国家',
  `description` varchar(255) DEFAULT NULL COMMENT '品牌信息描述',
  `product_type` varchar(255) DEFAULT NULL COMMENT '该品牌下产品类型',
  `brand_link` varchar(255) DEFAULT NULL COMMENT '品牌厂商官网链接',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  UNIQUE(`en_name`, `cn_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
