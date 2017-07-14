SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for iie_brand_model
-- ----------------------------
DROP TABLE IF EXISTS `iie_device_model`;
CREATE TABLE `iie_device_model` (
  `id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `brand_id` INT UNSIGNED NOT NULL COMMENT '品牌id',
  `brand` varchar(255) NOT NULL COMMENT '品牌英文名',
  `model` varchar(255) NOT NULL COMMENT '型号',
  `device_type_id` INT UNSIGNED NOT NULL COMMENT '设备类型id',
  `category` varchar(255) DEFAULT NULL COMMENT '设备类别简写',
  `type` varchar(255) DEFAULT NULL COMMENT '设备类型简写',
  `description` varchar(255) DEFAULT NULL COMMENT '型号信息描述',
  `model_link` varchar(255) DEFAULT NULL COMMENT '型号网站链接',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  UNIQUE(`brand`,`model`),
  FOREIGN KEY (brand_id) REFERENCES iie_brand(id) ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (device_type_id) REFERENCES iie_device_type(id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
