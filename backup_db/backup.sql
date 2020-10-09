-- MySQL dump 10.13  Distrib 5.7.30, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: myflaskapp
-- ------------------------------------------------------
-- Server version	5.7.30-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `body` text,
  `downloadComplete` varchar(5) DEFAULT NULL,
  `downloadFolder` varchar(200) DEFAULT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_articles_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
INSERT INTO `articles` (`id`, `title`, `author`, `body`, `downloadComplete`, `downloadFolder`, `create_date`) VALUES (117,'teste','glopes.santos@gmail.com','7003187271\r\n7003187284\r\n7003187300\r\n7003187343','Sim','C:\\Anaconda3\\envs\\petronectFlask\\codesLocal\\downloads\\oportunidades\\glopes.santos@gmail.com\\teste','2020-10-08 14:35:41');
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;

--
-- Table structure for table `classifica`
--

DROP TABLE IF EXISTS `classifica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classifica` (
  `unique_key` varchar(20) NOT NULL,
  `user` varchar(45) DEFAULT NULL,
  `id_lista` varchar(45) DEFAULT NULL,
  `Oportunidade` varchar(45) DEFAULT NULL,
  `item` varchar(45) DEFAULT NULL,
  `descricao` text,
  `emp_menor_valor` varchar(200) DEFAULT NULL,
  `menor_valor` varchar(45) DEFAULT NULL,
  `empr_seg_men_val` varchar(200) DEFAULT NULL,
  `seg_men_val` varchar(45) DEFAULT NULL,
  `emp_maior_val` varchar(200) DEFAULT NULL,
  `maior_valor` varchar(45) DEFAULT NULL,
  `valor_sua_empresa` varchar(45) DEFAULT NULL,
  `res_percentual` varchar(4) DEFAULT NULL,
  `status_sua_empresa` varchar(45) DEFAULT NULL,
  `margem_seg_menor_valor` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classifica`
--

/*!40000 ALTER TABLE `classifica` DISABLE KEYS */;
/*!40000 ALTER TABLE `classifica` ENABLE KEYS */;

--
-- Table structure for table `resumo_oportunidades`
--

DROP TABLE IF EXISTS `resumo_oportunidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resumo_oportunidades` (
  `id` int(11) NOT NULL,
  `user` varchar(45) DEFAULT NULL,
  `lista` varchar(45) DEFAULT NULL,
  `id_oportunidade` varchar(45) NOT NULL,
  `data_abertura` varchar(45) DEFAULT NULL,
  `data_vencimento` varchar(45) DEFAULT NULL,
  `horario` varchar(45) DEFAULT NULL,
  `descricao` mediumtext,
  `nome_arquivo` varchar(100) DEFAULT NULL,
  `nome_anexo` varchar(45) DEFAULT NULL,
  `realizar_download` varchar(5) DEFAULT NULL,
  `proposta_baixada` varchar(30) DEFAULT NULL,
  `caminho_proposta` varchar(100) DEFAULT NULL,
  `func_classifica` varchar(45) DEFAULT NULL,
  `create_date` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resumo_oportunidades`
--

/*!40000 ALTER TABLE `resumo_oportunidades` DISABLE KEYS */;
INSERT INTO `resumo_oportunidades` (`id`, `user`, `lista`, `id_oportunidade`, `data_abertura`, `data_vencimento`, `horario`, `descricao`, `nome_arquivo`, `nome_anexo`, `realizar_download`, `proposta_baixada`, `caminho_proposta`, `func_classifica`, `create_date`) VALUES (117,'glopes.santos@gmail.com','teste','7003187271','31.07.2020','07.08.2020','20:00:00','CHAVE DE FLUXO PRINCIPIO DE','7003187271 - AQUISICAO DE CHAVE DE FLUXO PRINCIPIO DE.pdf','Anexos7003187271.zip',NULL,NULL,NULL,NULL,'08/10/2020'),(117,'glopes.santos@gmail.com','teste','7003187284','31.07.2020','07.08.2020','20:00:00','TRANSMISSOR DE NIVEL','7003187284 - AQUISICAO DE TRANSMISSOR DE NIVEL.pdf','Anexos7003187284.zip',NULL,NULL,NULL,NULL,'08/10/2020'),(117,'glopes.santos@gmail.com','teste','7003187300','31.07.2020','07.08.2020','20:00:00','TRANSMISSOR DE NIVEL','7003187300 - AQUISICAO DE TRANSMISSOR DE NIVEL.pdf','Anexos7003187300.zip',NULL,NULL,NULL,NULL,'08/10/2020'),(117,'glopes.santos@gmail.com','teste','7003187343','31.07.2020','07.08.2020','20:00:00','VALVULA ESFERA METALICA, MA','7003187343 - AQUISICAO DE VALVULA ESFERA METALICA, MA.pdf','Anexos7003187343.zip',NULL,NULL,NULL,NULL,'08/10/2020');
/*!40000 ALTER TABLE `resumo_oportunidades` ENABLE KEYS */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `empresa` varchar(45) DEFAULT NULL,
  `usernamePet` varchar(25) DEFAULT NULL,
  `passwordPet` varchar(100) DEFAULT NULL,
  `fromEmail` varchar(50) DEFAULT NULL,
  `fromPwd` varchar(100) DEFAULT NULL,
  `smtpServer` varchar(50) DEFAULT NULL,
  `smtpPort` varchar(50) DEFAULT NULL,
  `mailList` varchar(500) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`, `empresa`, `usernamePet`, `passwordPet`, `fromEmail`, `fromPwd`, `smtpServer`, `smtpPort`, `mailList`, `register_date`) VALUES (8,'Gabriel Lopes dos Santos','glopes.santos@gmail.com','glopes.santos@gmail.com','F100stres','EMERSON','RENATA_L','Insaut28','gabriel@insaut.com.br','f100siii','smtp.insaut.com.br','587','gabriel@insaut.com.br','2020-06-16 22:08:42'),(19,'Daniele de Assis Fonte','engfonte@hotmail.com','insaut','123',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2020-10-08 01:45:26');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-08 18:28:06
