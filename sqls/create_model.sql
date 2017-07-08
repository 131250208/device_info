SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for iie_brand_model
-- ----------------------------
DROP TABLE IF EXISTS `iie_brand_model`;
CREATE TABLE `iie_brand_model` (
  `id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `brand` varchar(255) NOT NULL,
  `model` varchar(255) NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `model_link` varchar(255) DEFAULT NULL,
  UNIQUE(`brand`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of iie_brand_model
-- ----------------------------
