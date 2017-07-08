/*
Navicat MySQL Data Transfer

Source Server         : MySQL
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : upnp

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-06-22 20:39:25
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for iie_brand
-- ----------------------------
DROP TABLE IF EXISTS `iie_brand`;
CREATE TABLE `iie_brand` (
  `id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `en_name` varchar(255) DEFAULT NULL,
  `cn_name` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `product_type` varchar(255) DEFAULT NULL,
  `brand_link` varchar(255) DEFAULT NULL,
  UNIQUE(`en_name`, `cn_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of iie_brand
-- ----------------------------
