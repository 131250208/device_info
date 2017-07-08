/*
Navicat MySQL Data Transfer

Source Server         : MySQL
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : upnp

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-06-22 20:39:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for iie_device_type
-- ----------------------------
DROP TABLE IF EXISTS `iie_device_type`;
CREATE TABLE `iie_device_type` (
  `id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `category` varchar(50) NOT NULL COMMENT '设备一级类型内部标识',
  `category_cn_name` varchar(50) DEFAULT NULL COMMENT '设备一级类型中文全称',
  `category_en_name` varchar(50) DEFAULT NULL COMMENT '设备一级类型英文全称',
  `type` varchar(50) NOT NULL COMMENT '设备二级类型内部标识',
  `type_cn_name` varchar(50) DEFAULT NULL COMMENT '设备二级类型中文全称',
  `type_en_name` varchar(50) DEFAULT NULL COMMENT '设备二级类型英文全称',
  `description` text COMMENT '设备类型描述',
  UNIQUE(`category`, `type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of iie_device_type
-- ----------------------------
