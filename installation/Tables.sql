CREATE TABLE `actividades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` text,
  `descripcion` text,
  `tiempo` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `actividadesasignadas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` text,
  `descripcion` text,
  `tiempo` int DEFAULT NULL,
  `idEquipo` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `idEquipo` (`idEquipo`),
  CONSTRAINT `actividadesasignadas_ibfk_1` FOREIGN KEY (`idEquipo`) REFERENCES `equipos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `areas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` text NOT NULL,
  `descripcion` text,
  `responsable` int NOT NULL,
  `departamento` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `responsable` (`responsable`),
  KEY `departamento` (`departamento`),
  CONSTRAINT `areas_ibfk_1` FOREIGN KEY (`responsable`) REFERENCES `empleados` (`id`),
  CONSTRAINT `areas_ibfk_2` FOREIGN KEY (`departamento`) REFERENCES `departamentos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `category` (
  `id` int NOT NULL,
  `name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `departamentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `empleados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `clave` int DEFAULT NULL,
  `nombre` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `equipos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` text,
  `descripcion` text,
  `area` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `inventory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `category` int DEFAULT NULL,
  `description` text NOT NULL,
  `brand` text,
  `model` text,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `category` (`category`),
  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`category`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `inventory_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL,
  `type` text NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `comment` text,
  `origin` text,
  `origin_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `inventory_detail_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `inventory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=235 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `mantenimientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` timestamp NOT NULL,
  `estado` text NOT NULL,
  `responsable` int NOT NULL,
  `comentario` text,
  `tipo` text NOT NULL,
  `tiempoProgramado` int DEFAULT NULL,
  `anteriorId` int DEFAULT NULL,
  `siguienteId` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `siguienteId` (`siguienteId`),
  KEY `anteriorId` (`anteriorId`),
  KEY `responsable` (`responsable`),
  CONSTRAINT `mantenimientos_ibfk_1` FOREIGN KEY (`siguienteId`) REFERENCES `mantenimientos` (`id`),
  CONSTRAINT `mantenimientos_ibfk_2` FOREIGN KEY (`anteriorId`) REFERENCES `mantenimientos` (`id`),
  CONSTRAINT `mantenimientos_ibfk_3` FOREIGN KEY (`responsable`) REFERENCES `empleados` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=309 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `mantenimientos_actividadesasignadas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mantenimientoId` int DEFAULT NULL,
  `actividadesId` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `actividadesId` (`actividadesId`),
  KEY `mantenimientoId` (`mantenimientoId`),
  CONSTRAINT `mantenimientos_actividadesasignadas_ibfk_1` FOREIGN KEY (`actividadesId`) REFERENCES `actividadesasignadas` (`id`),
  CONSTRAINT `mantenimientos_actividadesasignadas_ibfk_2` FOREIGN KEY (`mantenimientoId`) REFERENCES `mantenimientos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=516 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `requisitions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL,
  `status` text NOT NULL,
  `description` text,
  `delivered` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `requisitions_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `requisition_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `comment` text,
  `status` text NOT NULL,
  `deliveredQuantity` int DEFAULT NULL,
  `deliveredDate` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `requisition_id` (`requisition_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `requisitions_detail_ibfk_1` FOREIGN KEY (`requisition_id`) REFERENCES `requisitions` (`id`),
  CONSTRAINT `requisitions_detail_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `inventory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=318 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `tools` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `description` text,
  `brand` text,
  `model` text,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `tools_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tool_id` int NOT NULL,
  `employer_id` int NOT NULL,
  `quantity` int NOT NULL,
  `comment` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `employer_id` (`employer_id`),
  KEY `tool_id` (`tool_id`),
  CONSTRAINT `tools_detail_ibfk_1` FOREIGN KEY (`employer_id`) REFERENCES `empleados` (`id`),
  CONSTRAINT `tools_detail_ibfk_2` FOREIGN KEY (`tool_id`) REFERENCES `tools` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `workorders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL,
  `status` text NOT NULL,
  `responsible` int NOT NULL,
  `comment` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `responsible` (`responsible`),
  CONSTRAINT `workorders_ibfk_1` FOREIGN KEY (`responsible`) REFERENCES `empleados` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `workorders_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `workorder_id` int NOT NULL,
  `maintenance_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `workorder_id` (`workorder_id`),
  KEY `maintenance_id` (`maintenance_id`),
  CONSTRAINT `workorders_detail_ibfk_1` FOREIGN KEY (`workorder_id`) REFERENCES `workorders` (`id`),
  CONSTRAINT `workorders_detail_ibfk_2` FOREIGN KEY (`maintenance_id`) REFERENCES `mantenimientos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb3;
