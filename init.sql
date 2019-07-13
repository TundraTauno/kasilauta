DROP DATABASE IF EXISTS `kasilauta`;
CREATE DATABASE `kasilauta`
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

USE 'kasilauta';
GRANT ALL PRIVILEGES ON kasilauta.* TO 'kasilauta'@'localhost' IDENTIFIED BY 'kasilauta'

WITH GRANT OPTION;
FLUSH PRIVILEGES;
