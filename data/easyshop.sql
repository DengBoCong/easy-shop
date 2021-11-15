/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50734
 Source Host           : localhost:3306
 Source Schema         : easyshop

 Target Server Type    : MySQL
 Target Server Version : 50734
 File Encoding         : 65001

 Date: 16/11/2021 00:35:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for shop_area
-- ----------------------------
DROP TABLE IF EXISTS `shop_area`;
CREATE TABLE `shop_area`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '名称',
  `DESCRIPTION` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '备注',
  `EN_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '英文名称',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_area
-- ----------------------------
INSERT INTO `shop_area` VALUES ('32685ca6-39f3-11ec-9cc8-74dfbf6cbdba', '2021-10-31 10:35:23', '哈哈', '', 'test');
INSERT INTO `shop_area` VALUES ('907d1f0c-37fb-11ec-80c6-74dfbf6cbdba', '2021-10-28 22:30:14', '中国', '', 'China');
INSERT INTO `shop_area` VALUES ('a60d121e-37ff-11ec-99e0-74dfbf6cbdba', '2021-10-28 22:59:28', '美国', '', 'American');
INSERT INTO `shop_area` VALUES ('ba8a2513-3946-11ec-bdf6-74dfbf6cbdba', '2021-10-30 14:00:48', '英国', '', 'English');

-- ----------------------------
-- Table structure for shop_good
-- ----------------------------
DROP TABLE IF EXISTS `shop_good`;
CREATE TABLE `shop_good`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `BRAND` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '品牌',
  `COLOR` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '颜色',
  `STYLE` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '款式',
  `DESCRIPTION` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '描述',
  `SUPPLIER_COLOR` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '供应商配色',
  `MATERIAL` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '材质',
  `PLACE_OF_ORIGIN` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '产地',
  `PRODUCT_NUMBER` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '产品编号',
  `FACTORY_CODE` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '工厂代码',
  `AREA_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属地区ID',
  `CURRENCY` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '货币',
  `CATEGORY_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '产品分类ID',
  `SIZE` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '尺码',
  `SIZE_CHART` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '尺码表地址',
  `STAFF_EMAIL` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '员工邮箱',
  `IS_PUBLISHED` tinyint(1) NOT NULL COMMENT '是否发布',
  `CLASS` enum('SAMPLE','DESIGN','REFERENCE') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '产品归类',
  `TYPE` enum('MEN','WOMEN','KIDS','OTHERS') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '所属类型',
  `COVER` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '封面地址',
  `USER_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'USER ID',
  `NUM` int(11) NOT NULL COMMENT '数量',
  `PRICE` decimal(20, 2) NOT NULL COMMENT '价格',
  `CATEGORY` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '产品分类',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_good
-- ----------------------------
INSERT INTO `shop_good` VALUES ('12c394ac-396e-11ec-abd6-74dfbf6cbdba', '2021-10-30 18:42:27', 'JW ANDERSON', 'Blue', 'Down Lannic Jacket', 'Long sleeve', 'Tobacco', '100% Cotton', 'China', '212477F098000', 'sajkljkldfj32234', 'a60d121e-37ff-11ec-99e0-74dfbf6cbdba', 'JPN', 'ecfa0cfb-3803-11ec-8f4e-74dfbf6cbdba', 'M,L,S,XL', '/static/uploads/images/2021/10/0dfc4eab-396e-11ec-94f1-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'DESIGN', 'MEN', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 23.00, 'Shoes');
INSERT INTO `shop_good` VALUES ('137bad88-430e-11ec-8165-74dfbf6cbdba', '2021-11-12 00:40:28', 'JW ANDERSON123', 'Blue', 'sadf', 'Long sleeve', '啥地方', '啥地方', '啥地方', '212477F098000', 'fdsfa', 'ba8a2513-3946-11ec-bdf6-74dfbf6cbdba', 'RMB', 'f99ac93e-3803-11ec-8089-74dfbf6cbdba', 'L,S', '/static/uploads/images/2021/11/09c5c050-430e-11ec-b1bb-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'REFERENCE', 'MEN', '/static/uploads/images/2021/11/0b41bf1e-430e-11ec-bfc8-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 12.00, 'bag');
INSERT INTO `shop_good` VALUES ('17ae464e-3a30-11ec-8d36-74dfbf6cbdba', '2021-10-31 17:51:17', 'JW ANDERSON123', 'Gray', 'Down Lannic Jacket', 'Long sleeve', 'Tobacco', '100% Cotton', 'China', '212477F098000', 'sajkljkldfj32234', 'ba8a2513-3946-11ec-bdf6-74dfbf6cbdba', 'RMB', '5f511543-39f3-11ec-b74d-74dfbf6cbdba', 'S,XXL,XL,M', '/static/uploads/images/2021/10/bded30ed-3a2f-11ec-86b3-74dfbf6cbdba.jpg', '123', 1, 'SAMPLE', 'WOMEN', '/static/uploads/images/2021/10/ddeb9134-3a2f-11ec-bf68-74dfbf6cbdba.png', 'aa8ff54a-3ee4-11ec-8aa0-74dfbf6cbdba', 0, 12.00, 'sf');
INSERT INTO `shop_good` VALUES ('181807b2-396d-11ec-bee1-74dfbf6cbdba', '2021-10-30 18:35:26', 'JW ANDERSON', 'Brown', 'Down Lannic Jacket', 'Long sleeve', 'Tobacco', '100% Cotton', 'China', '212477F098000', 'sajkljkldfj32234', '907d1f0c-37fb-11ec-80c6-74dfbf6cbdba', 'RMB', 'ecfa0cfb-3803-11ec-8f4e-74dfbf6cbdba', 'L,M,S,XL', '/static/uploads/images/2021/10/e2e51092-396b-11ec-b948-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'SAMPLE', 'KIDS', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 30.00, 'Shoes');
INSERT INTO `shop_good` VALUES ('1a2f7d7b-430e-11ec-9a5d-74dfbf6cbdba', '2021-11-12 00:40:39', 'JW ANDERSON123', 'Blue', 'sadf', 'Long sleeve', '啥地方', '啥地方', '啥地方', '212477F098000', 'fdsfa', 'ba8a2513-3946-11ec-bdf6-74dfbf6cbdba', 'RMB', 'f99ac93e-3803-11ec-8089-74dfbf6cbdba', 'L,S', '/static/uploads/images/2021/11/09c5c050-430e-11ec-b1bb-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'REFERENCE', 'MEN', '/static/uploads/images/2021/11/0b41bf1e-430e-11ec-bfc8-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 1232.00, 'bag');
INSERT INTO `shop_good` VALUES ('3cc09b86-4178-11ec-b7e7-74dfbf6cbdba', '2021-11-10 00:15:21', 'JW ANDERSON123', 'Brown', 'sadf', 'Long sleeve', '啥地方', '100% Cotton', 'China', '4234234234', '234234234', 'a60d121e-37ff-11ec-99e0-74dfbf6cbdba', 'RMB', 'f99ac93e-3803-11ec-8089-74dfbf6cbdba', 'M', '/static/uploads/images/2021/11/c6b58400-4177-11ec-a804-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'REFERENCE', 'WOMEN', '/static/uploads/images/2021/11/c7e67c69-4177-11ec-be66-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 17.00, 'bag');
INSERT INTO `shop_good` VALUES ('4fb74cc0-396d-11ec-bffc-74dfbf6cbdba', '2021-10-30 18:36:59', 'JW ANDERSON', 'Brown', 'Down Lannic Jacket', 'Long sleeve', 'Tobacco', '100% Cotton', 'China', '212477F098000', 'sajkljkldfj32234', '907d1f0c-37fb-11ec-80c6-74dfbf6cbdba', 'RMB', 'ecfa0cfb-3803-11ec-8f4e-74dfbf6cbdba', 'L,M,S,XL', '/static/uploads/images/2021/10/e2e51092-396b-11ec-b948-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'SAMPLE', 'OTHERS', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 30.00, 'Shoes');
INSERT INTO `shop_good` VALUES ('58c8c95c-4240-11ec-837d-74dfbf6cbdba', '2021-11-11 00:07:48', 'JW ANDERSON123', 'Brown', 'sadf', 'Long sleeve', 'Tobacco', '100% Cotton', '啥地方', '3245234523554235', '4134241', '907d1f0c-37fb-11ec-80c6-74dfbf6cbdba', 'RMB', '5f511543-39f3-11ec-b74d-74dfbf6cbdba', 'S,XXL', '/static/uploads/images/2021/11/5311fc1f-4240-11ec-a88a-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'SAMPLE', 'MEN', '/static/uploads/images/2021/11/5435421e-4240-11ec-9fac-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 12.00, 'sf');
INSERT INTO `shop_good` VALUES ('5952ec65-430e-11ec-91f6-74dfbf6cbdba', '2021-11-12 00:42:25', 'JW ANDERSON', 'Blue', 'sadf', 'Long sleeve', 'Tobacco', '100% Cotton', '啥地方', '212477F098000', '32434', '907d1f0c-37fb-11ec-80c6-74dfbf6cbdba', 'RMB', 'ecfa0cfb-3803-11ec-8f4e-74dfbf6cbdba', 'M,S,XL', '/static/uploads/images/2021/11/55085387-430e-11ec-bbac-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'REFERENCE', 'MEN', '/static/uploads/images/2021/11/5631fdf4-430e-11ec-85c3-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 123.00, 'Shoes');
INSERT INTO `shop_good` VALUES ('6bff9ab5-423d-11ec-b123-74dfbf6cbdba', '2021-11-10 23:46:51', 'JW ANDERSON', 'Blue', 'sadf', 'Long sleeve', '啥地方', '100% Cotton', '啥地方', '3245234523554235', '324234234', 'ba8a2513-3946-11ec-bdf6-74dfbf6cbdba', 'RMB', '5f511543-39f3-11ec-b74d-74dfbf6cbdba', 'M,XL,S,XXL', '/static/uploads/images/2021/11/00cd3e09-423d-11ec-b714-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'SAMPLE', 'MEN', '/static/uploads/images/2021/11/0513c045-423d-11ec-a51d-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 15.00, 'sf');
INSERT INTO `shop_good` VALUES ('73ffc887-4240-11ec-b659-74dfbf6cbdba', '2021-11-11 00:08:33', 'JW ANDERSON', 'Blue', 'sadf', '啥地方', 'Tobacco', '100% Cotton', 'China', '3245234523554235', '4132412', '907d1f0c-37fb-11ec-80c6-74dfbf6cbdba', 'RMB', '5f511543-39f3-11ec-b74d-74dfbf6cbdba', 'M,XXL', '/static/uploads/images/2021/11/6f6948e5-4240-11ec-b6a9-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'SAMPLE', 'MEN', '/static/uploads/images/2021/11/70b36de1-4240-11ec-9699-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 43.00, 'sf');
INSERT INTO `shop_good` VALUES ('76845a10-423e-11ec-8d7a-74dfbf6cbdba', '2021-11-10 23:54:19', 'JW ANDERSON', 'Blue', 'sadf', '啥地方', 'Tobacco', '100% Cotton', 'China', '3245234523554235', '253245324523', 'a60d121e-37ff-11ec-99e0-74dfbf6cbdba', 'JPN', 'f99ac93e-3803-11ec-8089-74dfbf6cbdba', 'S,XL,XXL,M,L', '/static/uploads/images/2021/11/6e2256f0-423e-11ec-85d7-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'SAMPLE', 'MEN', '/static/uploads/images/2021/11/708ad6db-423e-11ec-bd7a-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 1232.00, 'bag');
INSERT INTO `shop_good` VALUES ('9ccad44a-423e-11ec-bda3-74dfbf6cbdba', '2021-11-10 23:55:23', 'JW ANDERSON', 'Brown', 'Down Lannic Jacket', 'Long sleeve', '啥地方', '100% Cotton', '啥地方', '3245234523554235', '43242342', 'public', 'RMB', 'ecfa0cfb-3803-11ec-8f4e-74dfbf6cbdba', 'M,S,XXL', '/static/uploads/images/2021/11/98b6909a-423e-11ec-9187-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'SAMPLE', 'MEN', '/static/uploads/images/2021/11/9a0b250d-423e-11ec-a147-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 12.00, 'Shoes');
INSERT INTO `shop_good` VALUES ('9ffe7464-4240-11ec-ba31-74dfbf6cbdba', '2021-11-11 00:09:47', 'JW ANDERSON123', 'Gray', 'sadf', 'Long sleeve', 'Tobacco', '100% Cotton', 'China', '3245234523554235', '43243242', 'public', 'JPN', '5f511543-39f3-11ec-b74d-74dfbf6cbdba', 'L,M,S', '/static/uploads/images/2021/11/9b45caaf-4240-11ec-8d92-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'SAMPLE', 'MEN', '/static/uploads/images/2021/11/9cbd8c3c-4240-11ec-b5fb-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 12.00, 'sf');
INSERT INTO `shop_good` VALUES ('a660c389-4177-11ec-bd05-74dfbf6cbdba', '2021-11-10 00:11:09', 'JW ANDERSON', 'Gray', 'sadf', 'Long sleeve', '啥地方', '100% Cotton', '啥地方', '3245234523554235', '3452345322345', '907d1f0c-37fb-11ec-80c6-74dfbf6cbdba', 'RMB', 'f99ac93e-3803-11ec-8089-74dfbf6cbdba', 'L,S,XL,M', '/static/uploads/images/2021/11/a0e72c91-4177-11ec-b41d-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'DESIGN', 'WOMEN', '/static/uploads/images/2021/11/a4755dff-4177-11ec-b8fe-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 1000000.00, 'bag');
INSERT INTO `shop_good` VALUES ('ac1c3100-39fc-11ec-9782-74dfbf6cbdba', '2021-10-31 11:43:12', 'ha', 'Blue', 'fsd', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'a60d121e-37ff-11ec-99e0-74dfbf6cbdba', 'EUR', 'f99ac93e-3803-11ec-8089-74dfbf6cbdba', 'XL,S,M,L', '/static/uploads/images/2021/10/aade4312-39fc-11ec-949d-74dfbf6cbdba.jpg', 'sdf', 1, 'REFERENCE', 'MEN', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 12.00, 'bag');
INSERT INTO `shop_good` VALUES ('becb055a-3b26-11ec-b8e1-74dfbf6cbdba', '2021-11-01 23:16:54', 'ha', 'Blue', 'fsd', 'sdf', 'sdf', '算法', '算法', 'sdf', '安抚', 'ba8a2513-3946-11ec-bdf6-74dfbf6cbdba', 'JPN', '5f511543-39f3-11ec-b74d-74dfbf6cbdba', 'M,XL', '/static/uploads/images/2021/11/b463839c-3b26-11ec-8f41-74dfbf6cbdba.jpg', 'sdf', 1, 'SAMPLE', 'MEN', '/static/uploads/images/2021/11/b9743e93-3b26-11ec-b4cb-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 12.00, 'sf');
INSERT INTO `shop_good` VALUES ('c2a6c7b6-39fc-11ec-a88f-74dfbf6cbdba', '2021-10-31 11:43:50', 'ha', 'Blue', 'fsd', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'public', 'EUR', 'f99ac93e-3803-11ec-8089-74dfbf6cbdba', 'L,M,S,XL', '/static/uploads/images/2021/10/aade4312-39fc-11ec-949d-74dfbf6cbdba.jpg', 'sdf', 1, 'SAMPLE', 'MEN', '/static/uploads/images/2021/10/8e1c8475-39fc-11ec-a79e-74dfbf6cbdba.jpg', 'aa8ff54a-3ee4-11ec-8aa0-74dfbf6cbdba', 0, 1.00, 'bag');
INSERT INTO `shop_good` VALUES ('c329521d-423e-11ec-9409-74dfbf6cbdba', '2021-11-10 23:56:27', 'JW ANDERSON', 'Blue', 'Down Lannic Jacket', 'Long sleeve', 'Tobacco', '啥地方', 'China', '3245234523554235', 'sdaffrwrewrwe', 'public', 'RMB', 'ecfa0cfb-3803-11ec-8f4e-74dfbf6cbdba', 'M,S,XXL', '/static/uploads/images/2021/11/bed150b2-423e-11ec-be13-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'DESIGN', 'MEN', '/static/uploads/images/2021/11/c02a9cfc-423e-11ec-94ac-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 1000000.00, 'Shoes');
INSERT INTO `shop_good` VALUES ('d3270d02-4240-11ec-8fd9-74dfbf6cbdba', '2021-11-11 00:11:13', 'JW ANDERSON123', 'Pink', 'Down Lannic Jacket', 'Long sleeve', 'Tobacco', '100% Cotton', 'China', '3245234523554235', '41234123423', 'ba8a2513-3946-11ec-bdf6-74dfbf6cbdba', 'RMB', '5f511543-39f3-11ec-b74d-74dfbf6cbdba', 'M,S,XL', '/static/uploads/images/2021/11/ce141761-4240-11ec-920a-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'SAMPLE', 'MEN', '/static/uploads/images/2021/11/d0003967-4240-11ec-b29e-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 34.00, 'sf');
INSERT INTO `shop_good` VALUES ('d775f6bb-423e-11ec-a96e-74dfbf6cbdba', '2021-11-10 23:57:01', 'JW ANDERSON', 'Blue', 'Down Lannic Jacket', '啥地方', 'Tobacco', '100% Cotton', '啥地方', '212477F098000', '423143qrerq', 'ba8a2513-3946-11ec-bdf6-74dfbf6cbdba', 'RMB', 'f99ac93e-3803-11ec-8089-74dfbf6cbdba', 'M,XL,XXL', '/static/uploads/images/2021/11/d28265fa-423e-11ec-b4f5-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'DESIGN', 'MEN', '/static/uploads/images/2021/11/d4b5ec64-423e-11ec-906a-74dfbf6cbdba.jpg', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 0, 1000000.00, 'bag');
INSERT INTO `shop_good` VALUES ('dc16e87b-396c-11ec-9433-74dfbf6cbdba', '2021-10-30 18:33:45', 'JW ANDERSON', 'Brown', 'Down Lannic Jacket', 'Long sleeve', 'Tobacco', '100% Cotton', 'China', '212477F098000', 'sajkljkldfj32234', '907d1f0c-37fb-11ec-80c6-74dfbf6cbdba', 'RMB', 'ecfa0cfb-3803-11ec-8f4e-74dfbf6cbdba', 'L,M,S,XL', '/static/uploads/images/2021/10/e2e51092-396b-11ec-b948-74dfbf6cbdba.jpg', '1210212670@qq.com', 1, 'SAMPLE', 'MEN', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', 'aa8ff54a-3ee4-11ec-8aa0-74dfbf6cbdba', 0, 30.00, 'Shoes');

-- ----------------------------
-- Table structure for shop_good_category
-- ----------------------------
DROP TABLE IF EXISTS `shop_good_category`;
CREATE TABLE `shop_good_category`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '名称',
  `DESCRIPTION` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '备注',
  `EN_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '英文名称',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_good_category
-- ----------------------------
INSERT INTO `shop_good_category` VALUES ('5f511543-39f3-11ec-b74d-74dfbf6cbdba', '2021-10-31 10:36:38', '鞋', '', 'sf');
INSERT INTO `shop_good_category` VALUES ('ecfa0cfb-3803-11ec-8f4e-74dfbf6cbdba', '2021-10-28 23:30:05', '鞋履', '', 'Shoes');
INSERT INTO `shop_good_category` VALUES ('f99ac93e-3803-11ec-8089-74dfbf6cbdba', '2021-10-28 23:30:27', '包', '', 'bag');

-- ----------------------------
-- Table structure for shop_good_img
-- ----------------------------
DROP TABLE IF EXISTS `shop_good_img`;
CREATE TABLE `shop_good_img`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `URL` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '地址',
  `GOOD_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '货物ID',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_good_img
-- ----------------------------
INSERT INTO `shop_good_img` VALUES ('003ea157-3a52-11ec-815b-74dfbf6cbdba', '2021-10-31 21:54:01', '/static/uploads/images/2021/10/8c93bd1c-39fc-11ec-9800-74dfbf6cbdba.jpg', '003e7a8c-3a52-11ec-9bcd-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('003ea158-3a52-11ec-ae5b-74dfbf6cbdba', '2021-10-31 21:54:01', '/static/uploads/images/2021/10/8e1c8475-39fc-11ec-a79e-74dfbf6cbdba.jpg', '003e7a8c-3a52-11ec-9bcd-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('003ea159-3a52-11ec-93d6-74dfbf6cbdba', '2021-10-31 21:54:01', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', '003e7a8c-3a52-11ec-9bcd-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('003ea15a-3a52-11ec-8871-74dfbf6cbdba', '2021-10-31 21:54:01', '/static/uploads/images/2021/10/8c93bd1c-39fc-11ec-9800-74dfbf6cbdba.jpg', '003e7a8c-3a52-11ec-9bcd-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('003ea15b-3a52-11ec-a05e-74dfbf6cbdba', '2021-10-31 21:54:01', '/static/uploads/images/2021/10/8e1c8475-39fc-11ec-a79e-74dfbf6cbdba.jpg', '003e7a8c-3a52-11ec-9bcd-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('12c3bba6-396e-11ec-8f9e-74dfbf6cbdba', '2021-10-30 18:42:27', '/static/uploads/images/2021/10/0f95d4d1-396e-11ec-b333-74dfbf6cbdba.jpg', '12c394ac-396e-11ec-abd6-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('12c3bba7-396e-11ec-9999-74dfbf6cbdba', '2021-10-30 18:42:27', '/static/uploads/images/2021/10/112db016-396e-11ec-9131-74dfbf6cbdba.jpg', '12c394ac-396e-11ec-abd6-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('137bd484-430e-11ec-858f-74dfbf6cbdba', '2021-11-12 00:40:28', '/static/uploads/images/2021/11/0cab540b-430e-11ec-ac33-74dfbf6cbdba.jpg', '137bad88-430e-11ec-8165-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('17ae464f-3a30-11ec-82dd-74dfbf6cbdba', '2021-10-31 17:51:17', '/static/uploads/images/2021/10/e0ca0abd-3a2f-11ec-8530-74dfbf6cbdba.jpg', '17ae464e-3a30-11ec-8d36-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('17ae4650-3a30-11ec-8da7-74dfbf6cbdba', '2021-10-31 17:51:17', '/static/uploads/images/2021/10/e265da56-3a2f-11ec-865a-74dfbf6cbdba.jpg', '17ae464e-3a30-11ec-8d36-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('181807b3-396d-11ec-b1d2-74dfbf6cbdba', '2021-10-30 18:35:26', '/static/uploads/images/2021/10/e4b2cc92-396b-11ec-a17f-74dfbf6cbdba.jpg', '181807b2-396d-11ec-bee1-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('181807b4-396d-11ec-b7f1-74dfbf6cbdba', '2021-10-30 18:35:26', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', '181807b2-396d-11ec-bee1-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('1a2fa48a-430e-11ec-bad2-74dfbf6cbdba', '2021-11-12 00:40:39', '/static/uploads/images/2021/11/0cab540b-430e-11ec-ac33-74dfbf6cbdba.jpg', '1a2f7d7b-430e-11ec-9a5d-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('4fb74cc1-396d-11ec-a711-74dfbf6cbdba', '2021-10-30 18:36:59', '/static/uploads/images/2021/10/e4b2cc92-396b-11ec-a17f-74dfbf6cbdba.jpg', '4fb74cc0-396d-11ec-bffc-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('4fb74cc2-396d-11ec-9438-74dfbf6cbdba', '2021-10-30 18:36:59', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', '4fb74cc0-396d-11ec-bffc-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('58c8c95e-4240-11ec-a748-74dfbf6cbdba', '2021-11-11 00:07:48', '/static/uploads/images/2021/11/556aa4cc-4240-11ec-89b5-74dfbf6cbdba.jpg', '58c8c95c-4240-11ec-837d-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('5952ec66-430e-11ec-94f5-74dfbf6cbdba', '2021-11-12 00:42:25', '/static/uploads/images/2021/11/5772f0fd-430e-11ec-8f88-74dfbf6cbdba.jpg', '5952ec65-430e-11ec-91f6-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('5ddb20d2-3a5b-11ec-8cd6-74dfbf6cbdba', '2021-10-31 23:01:03', '/static/uploads/images/2021/10/8e1c8475-39fc-11ec-a79e-74dfbf6cbdba.jpg', 'c2a6c7b6-39fc-11ec-a88f-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('5ddb20d3-3a5b-11ec-b3f2-74dfbf6cbdba', '2021-10-31 23:01:03', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', 'c2a6c7b6-39fc-11ec-a88f-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('6bffe88c-423d-11ec-b755-74dfbf6cbdba', '2021-11-10 23:46:51', '/static/uploads/images/2021/11/066bae0c-423d-11ec-b191-74dfbf6cbdba.jpg', '6bff9ab5-423d-11ec-b123-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('73ffc88a-4240-11ec-a16d-74dfbf6cbdba', '2021-11-11 00:08:33', '/static/uploads/images/2021/11/71c83f09-4240-11ec-8e9d-74dfbf6cbdba.jpg', '73ffc887-4240-11ec-b659-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('76845a13-423e-11ec-a59b-74dfbf6cbdba', '2021-11-10 23:54:19', '/static/uploads/images/2021/11/71f8fea9-423e-11ec-bb10-74dfbf6cbdba.jpg', '76845a10-423e-11ec-8d7a-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('7cbd9532-430c-11ec-9491-74dfbf6cbdba', '2021-11-12 00:29:05', '/static/uploads/images/2021/11/c91f8588-4177-11ec-95e0-74dfbf6cbdba.jpg', '3cc09b86-4178-11ec-b7e7-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('9ccafb16-423e-11ec-be1e-74dfbf6cbdba', '2021-11-10 23:55:23', '/static/uploads/images/2021/11/9b818273-423e-11ec-8af9-74dfbf6cbdba.jpg', '9ccad44a-423e-11ec-bda3-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('9ffe7467-4240-11ec-bd37-74dfbf6cbdba', '2021-11-11 00:09:47', '/static/uploads/images/2021/11/9df55e06-4240-11ec-9e2a-74dfbf6cbdba.jpg', '9ffe7464-4240-11ec-ba31-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('a660ea5c-4177-11ec-a012-74dfbf6cbdba', '2021-11-10 00:11:09', '/static/uploads/images/2021/11/a5de5706-4177-11ec-ab1c-74dfbf6cbdba.jpg', 'a660c389-4177-11ec-bd05-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('ac1c3101-39fc-11ec-881d-74dfbf6cbdba', '2021-10-31 11:43:12', '/static/uploads/images/2021/10/8c93bd1c-39fc-11ec-9800-74dfbf6cbdba.jpg', 'ac1c3100-39fc-11ec-9782-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('ac1c3102-39fc-11ec-95ca-74dfbf6cbdba', '2021-10-31 11:43:12', '/static/uploads/images/2021/10/8e1c8475-39fc-11ec-a79e-74dfbf6cbdba.jpg', 'ac1c3100-39fc-11ec-9782-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('c329792e-423e-11ec-8cc1-74dfbf6cbdba', '2021-11-10 23:56:27', '/static/uploads/images/2021/11/c188cbcd-423e-11ec-b4f8-74dfbf6cbdba.jpg', 'c329521d-423e-11ec-9409-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('c49391b6-423c-11ec-8a40-74dfbf6cbdba', '2021-11-10 23:42:11', '/static/uploads/images/2021/11/c052a31c-423c-11ec-8fc2-74dfbf6cbdba.jpg', 'becb055a-3b26-11ec-b8e1-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('d3270d05-4240-11ec-9e5f-74dfbf6cbdba', '2021-11-11 00:11:13', '/static/uploads/images/2021/11/d12920fa-4240-11ec-82aa-74dfbf6cbdba.jpg', 'd3270d02-4240-11ec-8fd9-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('d7761dac-423e-11ec-aa60-74dfbf6cbdba', '2021-11-10 23:57:01', '/static/uploads/images/2021/11/d60a154c-423e-11ec-b452-74dfbf6cbdba.jpg', 'd775f6bb-423e-11ec-a96e-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('dc16e87c-396c-11ec-8453-74dfbf6cbdba', '2021-10-30 18:33:45', '/static/uploads/images/2021/10/e4b2cc92-396b-11ec-a17f-74dfbf6cbdba.jpg', 'dc16e87b-396c-11ec-9433-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('dc16e87d-396c-11ec-a3b3-74dfbf6cbdba', '2021-10-30 18:33:45', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', 'dc16e87b-396c-11ec-9433-74dfbf6cbdba');
INSERT INTO `shop_good_img` VALUES ('ecb4723d-3a54-11ec-83d3-74dfbf6cbdba', '2021-10-31 22:14:56', '/static/uploads/images/2021/10/8c93bd1c-39fc-11ec-9800-74dfbf6cbdba.jpg', 'en_us');
INSERT INTO `shop_good_img` VALUES ('ecb4723e-3a54-11ec-9cff-74dfbf6cbdba', '2021-10-31 22:14:56', '/static/uploads/images/2021/10/8e1c8475-39fc-11ec-a79e-74dfbf6cbdba.jpg', 'en_us');
INSERT INTO `shop_good_img` VALUES ('ecb4723f-3a54-11ec-96ad-74dfbf6cbdba', '2021-10-31 22:14:56', '/static/uploads/images/2021/10/e6bec1e6-396b-11ec-8b6e-74dfbf6cbdba.jpg', 'en_us');
INSERT INTO `shop_good_img` VALUES ('ecb47240-3a54-11ec-887d-74dfbf6cbdba', '2021-10-31 22:14:56', '/static/uploads/images/2021/10/8c93bd1c-39fc-11ec-9800-74dfbf6cbdba.jpg', 'en_us');
INSERT INTO `shop_good_img` VALUES ('ecb47241-3a54-11ec-9d20-74dfbf6cbdba', '2021-10-31 22:14:56', '/static/uploads/images/2021/10/8e1c8475-39fc-11ec-a79e-74dfbf6cbdba.jpg', 'en_us');

-- ----------------------------
-- Table structure for shop_good_price
-- ----------------------------
DROP TABLE IF EXISTS `shop_good_price`;
CREATE TABLE `shop_good_price`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `GOOD_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'GOOD ID',
  `START_NUM` int(11) NOT NULL COMMENT '起始数量',
  `END_NUM` int(11) NOT NULL COMMENT '终止数量',
  `PRICE` decimal(20, 3) NOT NULL COMMENT '价格',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_good_price
-- ----------------------------
INSERT INTO `shop_good_price` VALUES ('003ea15c-3a52-11ec-9dbf-74dfbf6cbdba', '2021-10-31 21:54:01', '003e7a8c-3a52-11ec-9bcd-74dfbf6cbdba', 1, 10, 23.000);
INSERT INTO `shop_good_price` VALUES ('003ea15d-3a52-11ec-8a12-74dfbf6cbdba', '2021-10-31 21:54:01', '003e7a8c-3a52-11ec-9bcd-74dfbf6cbdba', 12, 20, 12.500);
INSERT INTO `shop_good_price` VALUES ('12c3bba8-396e-11ec-8c87-74dfbf6cbdba', '2021-10-30 18:42:27', '12c394ac-396e-11ec-abd6-74dfbf6cbdba', 0, 100, 50.000);
INSERT INTO `shop_good_price` VALUES ('12c3bba9-396e-11ec-84bc-74dfbf6cbdba', '2021-10-30 18:42:27', '12c394ac-396e-11ec-abd6-74dfbf6cbdba', 100, 10000, 23.100);
INSERT INTO `shop_good_price` VALUES ('17ae4651-3a30-11ec-b6b6-74dfbf6cbdba', '2021-10-31 17:51:17', '17ae464e-3a30-11ec-8d36-74dfbf6cbdba', 12, 16, 12.000);
INSERT INTO `shop_good_price` VALUES ('181807b5-396d-11ec-b02b-74dfbf6cbdba', '2021-10-30 18:35:26', '181807b2-396d-11ec-bee1-74dfbf6cbdba', 0, 100, 50.000);
INSERT INTO `shop_good_price` VALUES ('181807b6-396d-11ec-a7dc-74dfbf6cbdba', '2021-10-30 18:35:26', '181807b2-396d-11ec-bee1-74dfbf6cbdba', 100, 10000, 30.000);
INSERT INTO `shop_good_price` VALUES ('4fb74cc3-396d-11ec-aaeb-74dfbf6cbdba', '2021-10-30 18:36:59', '4fb74cc0-396d-11ec-bffc-74dfbf6cbdba', 0, 100, 50.000);
INSERT INTO `shop_good_price` VALUES ('4fb74cc4-396d-11ec-a727-74dfbf6cbdba', '2021-10-30 18:36:59', '4fb74cc0-396d-11ec-bffc-74dfbf6cbdba', 100, 10000, 30.000);
INSERT INTO `shop_good_price` VALUES ('58c8c95d-4240-11ec-9014-74dfbf6cbdba', '2021-11-11 00:07:48', '58c8c95c-4240-11ec-837d-74dfbf6cbdba', 1, 10, 12.000);
INSERT INTO `shop_good_price` VALUES ('5ddccd72-3a5b-11ec-b91f-74dfbf6cbdba', '2021-10-31 23:01:03', 'c2a6c7b6-39fc-11ec-a88f-74dfbf6cbdba', 1, 10, 12.000);
INSERT INTO `shop_good_price` VALUES ('5ddccd73-3a5b-11ec-9b46-74dfbf6cbdba', '2021-10-31 23:01:03', 'c2a6c7b6-39fc-11ec-a88f-74dfbf6cbdba', 10, 100, 1.000);
INSERT INTO `shop_good_price` VALUES ('6bffc1a0-423d-11ec-ab01-74dfbf6cbdba', '2021-11-10 23:46:51', '6bff9ab5-423d-11ec-b123-74dfbf6cbdba', 0, 10, 15.000);
INSERT INTO `shop_good_price` VALUES ('6bffc1a1-423d-11ec-9587-74dfbf6cbdba', '2021-11-10 23:46:51', '6bff9ab5-423d-11ec-b123-74dfbf6cbdba', 10, 100, 6565.000);
INSERT INTO `shop_good_price` VALUES ('73ffc888-4240-11ec-b70d-74dfbf6cbdba', '2021-11-11 00:08:33', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 1, 10, 123.000);
INSERT INTO `shop_good_price` VALUES ('73ffc889-4240-11ec-b5d8-74dfbf6cbdba', '2021-11-11 00:08:33', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 10, 100, 43.000);
INSERT INTO `shop_good_price` VALUES ('76845a11-423e-11ec-a3e3-74dfbf6cbdba', '2021-11-10 23:54:19', '76845a10-423e-11ec-8d7a-74dfbf6cbdba', 0, 10, 5435.000);
INSERT INTO `shop_good_price` VALUES ('76845a12-423e-11ec-9e6a-74dfbf6cbdba', '2021-11-10 23:54:19', '76845a10-423e-11ec-8d7a-74dfbf6cbdba', 10, 1000, 1232.000);
INSERT INTO `shop_good_price` VALUES ('9ccad44b-423e-11ec-8d31-74dfbf6cbdba', '2021-11-10 23:55:23', '9ccad44a-423e-11ec-bda3-74dfbf6cbdba', 0, 10, 12.000);
INSERT INTO `shop_good_price` VALUES ('9ccad44c-423e-11ec-b1ce-74dfbf6cbdba', '2021-11-10 23:55:23', '9ccad44a-423e-11ec-bda3-74dfbf6cbdba', 10, 100, 45.000);
INSERT INTO `shop_good_price` VALUES ('9ffe7465-4240-11ec-9f59-74dfbf6cbdba', '2021-11-11 00:09:47', '9ffe7464-4240-11ec-ba31-74dfbf6cbdba', 1, 10, 3312.000);
INSERT INTO `shop_good_price` VALUES ('9ffe7466-4240-11ec-a2db-74dfbf6cbdba', '2021-11-11 00:09:47', '9ffe7464-4240-11ec-ba31-74dfbf6cbdba', 10, 100, 12.000);
INSERT INTO `shop_good_price` VALUES ('ac1c3103-39fc-11ec-a216-74dfbf6cbdba', '2021-10-31 11:43:12', 'ac1c3100-39fc-11ec-9782-74dfbf6cbdba', 1, 10, 23.000);
INSERT INTO `shop_good_price` VALUES ('ac1c3104-39fc-11ec-be84-74dfbf6cbdba', '2021-10-31 11:43:12', 'ac1c3100-39fc-11ec-9782-74dfbf6cbdba', 12, 20, 12.500);
INSERT INTO `shop_good_price` VALUES ('c495654b-423c-11ec-864a-74dfbf6cbdba', '2021-11-10 23:42:11', 'becb055a-3b26-11ec-b8e1-74dfbf6cbdba', 12, 13, 12.000);
INSERT INTO `shop_good_price` VALUES ('d3270d03-4240-11ec-a677-74dfbf6cbdba', '2021-11-11 00:11:13', 'd3270d02-4240-11ec-8fd9-74dfbf6cbdba', 0, 10, 34.000);
INSERT INTO `shop_good_price` VALUES ('d3270d04-4240-11ec-b457-74dfbf6cbdba', '2021-11-11 00:11:13', 'd3270d02-4240-11ec-8fd9-74dfbf6cbdba', 10, 100, 43.000);
INSERT INTO `shop_good_price` VALUES ('dc16e87e-396c-11ec-996c-74dfbf6cbdba', '2021-10-30 18:33:45', 'dc16e87b-396c-11ec-9433-74dfbf6cbdba', 0, 100, 50.000);
INSERT INTO `shop_good_price` VALUES ('dc170f6a-396c-11ec-8c16-74dfbf6cbdba', '2021-10-30 18:33:45', 'dc16e87b-396c-11ec-9433-74dfbf6cbdba', 100, 10000, 30.000);
INSERT INTO `shop_good_price` VALUES ('e5eb6a35-417b-11ec-a6ae-74dfbf6cbdba', '2021-11-10 00:41:34', '3cc09b86-4178-11ec-b7e7-74dfbf6cbdba', 0, 10, 12.000);

-- ----------------------------
-- Table structure for shop_good_size
-- ----------------------------
DROP TABLE IF EXISTS `shop_good_size`;
CREATE TABLE `shop_good_size`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `SIZE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '尺码',
  `DESCRIPTION` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '备注',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_good_size
-- ----------------------------
INSERT INTO `shop_good_size` VALUES ('0723985a-38d3-11ec-a2db-74dfbf6cbdba', '2021-10-30 00:12:35', 'S', '');
INSERT INTO `shop_good_size` VALUES ('97f1880c-38d1-11ec-b03a-74dfbf6cbdba', '2021-10-30 00:02:19', 'XL', '');
INSERT INTO `shop_good_size` VALUES ('da201778-38d1-11ec-abbe-74dfbf6cbdba', '2021-10-30 00:04:10', 'L', '');
INSERT INTO `shop_good_size` VALUES ('da87529b-38d2-11ec-99c2-74dfbf6cbdba', '2021-10-30 00:11:20', 'XXL', '');
INSERT INTO `shop_good_size` VALUES ('f06a2243-38d2-11ec-a033-74dfbf6cbdba', '2021-10-30 00:11:57', 'M', '');

-- ----------------------------
-- Table structure for shop_order
-- ----------------------------
DROP TABLE IF EXISTS `shop_order`;
CREATE TABLE `shop_order`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `NUM` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '订单编号',
  `TOTAL_AMOUNT` decimal(20, 3) NOT NULL COMMENT '总额',
  `STATUS` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '订单状态',
  `TRACK_NUM` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '追踪编号',
  `USER_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'User id',
  `CLASS` enum('NORMAL','SAMPLE') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '分类',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_order
-- ----------------------------
INSERT INTO `shop_order` VALUES ('344f4278-4565-11ec-ba03-74dfbf6cbdba', '2021-11-15 00:09:11', '20211115000911387', 2035.000, 'Processing', '34518ae5456511ec81c774dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');
INSERT INTO `shop_order` VALUES ('3657d8b2-4563-11ec-b2a1-74dfbf6cbdba', '2021-11-14 23:54:56', '20211114235455613', 2035.000, 'Processing', '3659d2cc456311ec866574dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');
INSERT INTO `shop_order` VALUES ('4d9c42de-461d-11ec-9674-74dfbf6cbdba', '2021-11-15 22:07:01', '20211115220701512', 2035.000, 'Processing', '4d9ed8d3461d11ec9ab974dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');
INSERT INTO `shop_order` VALUES ('4dd86d5d-461b-11ec-abe9-74dfbf6cbdba', '2021-11-15 21:52:43', '20211115215242960', 2035.000, 'Processing', '4dda67dd461b11eca7ca74dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');
INSERT INTO `shop_order` VALUES ('6abee022-4504-11ec-b853-74dfbf6cbdba', '2021-11-14 12:36:21', '20211114123621191', 516.000, 'Processing', '6abf7be4450411eca9ed74dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'SAMPLE');
INSERT INTO `shop_order` VALUES ('a87b3908-4565-11ec-824b-74dfbf6cbdba', '2021-11-15 00:12:26', '20211115001226604', 2035.000, 'Processing', 'a87d3385456511ec839174dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');
INSERT INTO `shop_order` VALUES ('afc5af21-461d-11ec-a878-74dfbf6cbdba', '2021-11-15 22:09:46', '20211115220945115', 2035.000, 'Processing', 'afc7a9b6461d11eca43174dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');
INSERT INTO `shop_order` VALUES ('bbca24ac-4565-11ec-900f-74dfbf6cbdba', '2021-11-15 00:12:59', '20211115001258761', 2035.000, 'Processing', 'bbcc4725456511ec9a7474dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');
INSERT INTO `shop_order` VALUES ('bc3c47f2-461d-11ec-8f30-74dfbf6cbdba', '2021-11-15 22:10:07', '20211115221006894', 516.000, 'Processing', 'bc3df328461d11ecaa8574dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'SAMPLE');
INSERT INTO `shop_order` VALUES ('d15f3c5f-4565-11ec-937f-74dfbf6cbdba', '2021-11-15 00:13:35', '20211115001334116', 2035.000, 'Processing', 'd16136c7456511ec8fd274dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');
INSERT INTO `shop_order` VALUES ('dda84a17-4501-11ec-9f30-74dfbf6cbdba', '2021-11-14 12:18:06', '20211114121805153', 1075.000, 'Processing', 'dda933ed450111ecba9574dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');
INSERT INTO `shop_order` VALUES ('e1f124ed-4564-11ec-8382-74dfbf6cbdba', '2021-11-15 00:06:53', '2021111500065336', 2035.000, 'Processing', 'e1f3944f456411ec97dc74dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');
INSERT INTO `shop_order` VALUES ('f4213594-461b-11ec-bbaf-74dfbf6cbdba', '2021-11-15 21:57:22', '20211115215721932', 2035.000, 'Processing', 'f4237dfd461b11ecbab974dfbf6cbdba', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'NORMAL');

-- ----------------------------
-- Table structure for shop_order_good
-- ----------------------------
DROP TABLE IF EXISTS `shop_order_good`;
CREATE TABLE `shop_order_good`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `ORDER_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '订单编号',
  `GOOD_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '货物编号',
  `NUM` int(11) NOT NULL COMMENT '数量',
  `TITLE` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '保留展示描述',
  `PRICE` decimal(20, 3) NOT NULL COMMENT '单个价格',
  `EMAIL` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '货物联系邮箱账号',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_order_good
-- ----------------------------
INSERT INTO `shop_order_good` VALUES ('344fde5c-4565-11ec-8525-74dfbf6cbdba', '2021-11-15 00:09:11', '344f4278-4565-11ec-ba03-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 12, '', 123.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('34502c41-4565-11ec-be83-74dfbf6cbdba', '2021-11-15 00:09:11', '344f4278-4565-11ec-ba03-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('34518ae4-4565-11ec-a6a5-74dfbf6cbdba', '2021-11-15 00:09:11', '344f4278-4565-11ec-ba03-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('3658742a-4563-11ec-b0c0-74dfbf6cbdba', '2021-11-14 23:54:56', '3657d8b2-4563-11ec-b2a1-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 12, '', 123.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('3659110d-4563-11ec-95eb-74dfbf6cbdba', '2021-11-14 23:54:56', '3657d8b2-4563-11ec-b2a1-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('3659abca-4563-11ec-8ab4-74dfbf6cbdba', '2021-11-14 23:54:56', '3657d8b2-4563-11ec-b2a1-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('4d9d0563-461d-11ec-922a-74dfbf6cbdba', '2021-11-15 22:07:01', '4d9c42de-461d-11ec-9674-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 12, '', 123.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('4d9dc825-461d-11ec-bc6d-74dfbf6cbdba', '2021-11-15 22:07:01', '4d9c42de-461d-11ec-9674-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('4d9eb257-461d-11ec-9f69-74dfbf6cbdba', '2021-11-15 22:07:01', '4d9c42de-461d-11ec-9674-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('4dd9302d-461b-11ec-93a5-74dfbf6cbdba', '2021-11-15 21:52:43', '4dd86d5d-461b-11ec-abe9-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 12, '', 123.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('4dd97e16-461b-11ec-a1fe-74dfbf6cbdba', '2021-11-15 21:52:43', '4dd86d5d-461b-11ec-abe9-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('4dda67dc-461b-11ec-b7fb-74dfbf6cbdba', '2021-11-15 21:52:43', '4dd86d5d-461b-11ec-abe9-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('6abf7be3-4504-11ec-9357-74dfbf6cbdba', '2021-11-14 12:36:21', '6abee022-4504-11ec-b853-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 12, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('a87bfbe1-4565-11ec-8005-74dfbf6cbdba', '2021-11-15 00:12:26', 'a87b3908-4565-11ec-824b-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 12, '', 123.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('a87c97e5-4565-11ec-b736-74dfbf6cbdba', '2021-11-15 00:12:26', 'a87b3908-4565-11ec-824b-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('a87d3384-4565-11ec-ab3f-74dfbf6cbdba', '2021-11-15 00:12:26', 'a87b3908-4565-11ec-824b-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('afc64b55-461d-11ec-a0bf-74dfbf6cbdba', '2021-11-15 22:09:46', 'afc5af21-461d-11ec-a878-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 12, '', 123.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('afc698ed-461d-11ec-a0bb-74dfbf6cbdba', '2021-11-15 22:09:46', 'afc5af21-461d-11ec-a878-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('afc782a7-461d-11ec-9641-74dfbf6cbdba', '2021-11-15 22:09:46', 'afc5af21-461d-11ec-a878-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('bbcb35b1-4565-11ec-b6fe-74dfbf6cbdba', '2021-11-15 00:12:59', 'bbca24ac-4565-11ec-900f-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 12, '', 123.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('bbcb8352-4565-11ec-9bf1-74dfbf6cbdba', '2021-11-15 00:12:59', 'bbca24ac-4565-11ec-900f-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('bbcc1f1e-4565-11ec-9562-74dfbf6cbdba', '2021-11-15 00:12:59', 'bbca24ac-4565-11ec-900f-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('bc3d09ab-461d-11ec-b051-74dfbf6cbdba', '2021-11-15 22:10:07', 'bc3c47f2-461d-11ec-8f30-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 12, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('bc3d5750-461d-11ec-a5f6-74dfbf6cbdba', '2021-11-15 22:10:07', 'bc3c47f2-461d-11ec-8f30-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('bc3df327-461d-11ec-9b49-74dfbf6cbdba', '2021-11-15 22:10:07', 'bc3c47f2-461d-11ec-8f30-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 16, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('d15fb143-4565-11ec-b803-74dfbf6cbdba', '2021-11-15 00:13:35', 'd15f3c5f-4565-11ec-937f-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 12, '', 123.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('d1602616-4565-11ec-ae80-74dfbf6cbdba', '2021-11-15 00:13:35', 'd15f3c5f-4565-11ec-937f-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('d16136c6-4565-11ec-9e66-74dfbf6cbdba', '2021-11-15 00:13:35', 'd15f3c5f-4565-11ec-937f-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('dda90cde-4501-11ec-bd22-74dfbf6cbdba', '2021-11-14 12:18:06', 'dda84a17-4501-11ec-9f30-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 12, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('dda90cdf-4501-11ec-ade4-74dfbf6cbdba', '2021-11-14 12:18:06', 'dda84a17-4501-11ec-9f30-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('e1f20ec0-4564-11ec-baa6-74dfbf6cbdba', '2021-11-15 00:06:53', 'e1f124ed-4564-11ec-8382-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 12, '', 123.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('e1f283a3-4564-11ec-8934-74dfbf6cbdba', '2021-11-15 00:06:53', 'e1f124ed-4564-11ec-8382-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('e1f36db9-4564-11ec-838e-74dfbf6cbdba', '2021-11-15 00:06:53', 'e1f124ed-4564-11ec-8382-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('f421f86d-461b-11ec-8d9b-74dfbf6cbdba', '2021-11-15 21:57:22', 'f4213594-461b-11ec-bbaf-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 12, '', 123.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('f4226d4b-461b-11ec-bff9-74dfbf6cbdba', '2021-11-15 21:57:22', 'f4213594-461b-11ec-bbaf-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, '', 0.000, '1210212670@qq.com');
INSERT INTO `shop_order_good` VALUES ('f4237dfc-461b-11ec-8264-74dfbf6cbdba', '2021-11-15 21:57:22', 'f4213594-461b-11ec-bbaf-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, '', 43.000, '1210212670@qq.com');

-- ----------------------------
-- Table structure for shop_sample_good
-- ----------------------------
DROP TABLE IF EXISTS `shop_sample_good`;
CREATE TABLE `shop_sample_good`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `USER_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'USER_ID',
  `GOOD_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'GOOD_ID',
  `NUM` int(11) NOT NULL COMMENT '数量',
  `SIZE` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '尺码',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_sample_good
-- ----------------------------
INSERT INTO `shop_sample_good` VALUES ('3d696194-4561-11ec-b522-74dfbf6cbdba', '2021-11-14 23:40:49', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 12, 'M');
INSERT INTO `shop_sample_good` VALUES ('4e870a70-4562-11ec-9ca5-74dfbf6cbdba', '2021-11-14 23:48:27', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, 'M');
INSERT INTO `shop_sample_good` VALUES ('a782ed8a-4562-11ec-b07f-74dfbf6cbdba', '2021-11-14 23:50:56', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 16, 'M');

-- ----------------------------
-- Table structure for shop_shopping_good
-- ----------------------------
DROP TABLE IF EXISTS `shop_shopping_good`;
CREATE TABLE `shop_shopping_good`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `USER_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'USER ID',
  `GOOD_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'GOOD ID',
  `NUM` int(11) NOT NULL COMMENT '数量',
  `SIZE` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '尺码',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_shopping_good
-- ----------------------------
INSERT INTO `shop_shopping_good` VALUES ('3f1bde6c-455e-11ec-bc78-74dfbf6cbdba', '2021-11-14 23:19:23', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 0, 'M');
INSERT INTO `shop_shopping_good` VALUES ('fcf389ed-445d-11ec-b216-74dfbf6cbdba', '2021-11-13 16:45:01', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 13, 'M');

-- ----------------------------
-- Table structure for shop_user
-- ----------------------------
DROP TABLE IF EXISTS `shop_user`;
CREATE TABLE `shop_user`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `EMAIL` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '邮箱账号',
  `_PWD` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '名称',
  `PHONE` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '联系方式',
  `IF_LOGIN` tinyint(1) NOT NULL COMMENT '是否允许登录',
  `ROLE` enum('ADMIN','AGENT','USER','SUPER') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色',
  `DESCRIPTION` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '备注',
  `AREA_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地区ID',
  `PARENT_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'PARENT_ID',
  `LAST_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'last name',
  `FIRST_NAME` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'first name',
  `COMPANY_NAME` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'company name',
  `ORDERS` int(11) NOT NULL COMMENT '订单数',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_user
-- ----------------------------
INSERT INTO `shop_user` VALUES ('2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', '2021-03-20 19:47:02', '1210212670@qq.com', 'pbkdf2:sha256:150000$M6BVSK6E$3655ec180cd306b50c84c6945338e89d26a60b67c5cebe2edae83de34b34bb32', 'super', '00000000000', 1, 'SUPER', 'none', '907d1f0c-37fb-11ec-80c6-74dfbf6cbdba', 'none', 'ew1', '23', '12', 11);
INSERT INTO `shop_user` VALUES ('52f6a6dc-3ec1-11ec-8ef1-74dfbf6cbdba', '2021-11-06 13:20:58', '1210212672@qq.com', 'pbkdf2:sha256:150000$g4rQNuCC$e782f82731f7a9c69842d0d5f305db1852daa6b0f1081de1c795ea9cc0ea8b06', 'update', '', 1, 'USER', '', 'ba8a2513-3946-11ec-bdf6-74dfbf6cbdba', 'root', 'lll', 'yi', '', 0);
INSERT INTO `shop_user` VALUES ('aa8ff54a-3ee4-11ec-8aa0-74dfbf6cbdba', '2021-11-06 17:33:58', '1210212673@qq.com', 'pbkdf2:sha256:150000$XCIR6Rbs$023c222c2f8f399956a9af91d37abac5b04380ed1343b6019a80ba4130f24284', 'hhh', '', 1, 'USER', '', '907d1f0c-37fb-11ec-80c6-74dfbf6cbdba', 'root', 'agent', 'yi12', '', 0);

-- ----------------------------
-- Table structure for shop_wish_good
-- ----------------------------
DROP TABLE IF EXISTS `shop_wish_good`;
CREATE TABLE `shop_wish_good`  (
  `ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ID',
  `CREATE_DATETIME` datetime NOT NULL COMMENT '创建时间',
  `USER_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'USER ID',
  `GOOD_ID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'GOOD ID',
  `SIZE` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '尺码',
  `NUM` int(11) NOT NULL COMMENT '数量',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shop_wish_good
-- ----------------------------
INSERT INTO `shop_wish_good` VALUES ('66ed45b0-4561-11ec-bdc0-74dfbf6cbdba', '2021-11-14 23:41:58', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', 'a660c389-4177-11ec-bd05-74dfbf6cbdba', 'M', 0);
INSERT INTO `shop_wish_good` VALUES ('71a50ea4-4561-11ec-9b52-74dfbf6cbdba', '2021-11-14 23:42:16', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', '5952ec65-430e-11ec-91f6-74dfbf6cbdba', 'M', 16);
INSERT INTO `shop_wish_good` VALUES ('9f331e66-43d4-11ec-b2b1-74dfbf6cbdba', '2021-11-13 00:21:42', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 'M', 12);
INSERT INTO `shop_wish_good` VALUES ('aee0651f-455d-11ec-8536-74dfbf6cbdba', '2021-11-14 23:15:21', '2ba2e146-a3f7-11eb-8858-74dfbf6cbdba', '73ffc887-4240-11ec-b659-74dfbf6cbdba', 'XXL', 16);

SET FOREIGN_KEY_CHECKS = 1;
