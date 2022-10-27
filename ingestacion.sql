DROP DATABASE IF EXISTS pi01;
CREATE DATABASE pi01;
USE pi01;

SELECT @@global.secure_file_priv;

DROP TABLE IF EXISTS sucursal;
CREATE TABLE IF NOT EXISTS sucursal (
  	Id_Sucursal				VARCHAR(30) NOT NULL,
  	Id_Comercio 			VARCHAR(30),
  	Id_Bandera	 			VARCHAR(30),
    banderaDescripcion		VARCHAR(150),
  	comercioRazonSocial		VARCHAR(150),
    provincia				VARCHAR(10),
    localidad				VARCHAR(50),
    direccion				VARCHAR(100),
    lat						DECIMAL(25,20),
    lng						DECIMAL(25,20),
    sucursalNombre			VARCHAR(100),
    sucursalTipo	 		VARCHAR(50),
    PRIMARY KEY (Id_Sucursal)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

LOAD DATA INFILE 'C:/files/PI/sucursal_out.csv'
INTO TABLE sucursal 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;


DROP TABLE IF EXISTS producto;
CREATE TABLE IF NOT EXISTS producto (
	Id_Producto				VARCHAR(20) NOT NULL,
  	marca		 			VARCHAR(50),
  	nombre		 			VARCHAR(150),
    presentacion_cant		DECIMAL(15,3),
  	presentacion_UMB		VARCHAR(10),
    PRIMARY KEY (Id_Producto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

LOAD DATA INFILE 'C:/files/PI/producto_out.csv'
INTO TABLE producto 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;






DROP TABLE IF EXISTS precio_semana;
CREATE TABLE IF NOT EXISTS precio_semana (
	Id_precio_semana		INT NOT NULL AUTO_INCREMENT,
  	precio					DECIMAL(25,5),
  	Id_Producto	 			VARCHAR(20),
  	Id_Sucursal	 			VARCHAR(30),
    Fecha					DATE,
  	PRIMARY KEY (Id_precio_semana)
    -- FOREIGN KEY (Id_Producto) REFERENCES producto(Id_Producto),
    -- FOREIGN KEY (Id_Sucursal) REFERENCES sucursal(Id_Sucursal)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- ALTER TABLE precio_semana ADD FOREIGN KEY (Id_Sucursal) REFERENCES sucursal (Id_Sucursal);
-- ALTER TABLE precio_semana ADD FOREIGN KEY (Id_Producto) REFERENCES producto (Id_Producto);
 
-- csv
LOAD DATA INFILE 'C:/files/PI/producto_precio_20200413.csv'
INTO TABLE precio_semana
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;


-- xls 2da hoja (hoja1)
LOAD DATA INFILE 'C:/files/PI/producto_precio_20200419.csv'
INTO TABLE precio_semana
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;

-- xls 1er hoja (hoja 0)
LOAD DATA INFILE 'C:/files/PI/producto_precio_20200426.csv'
INTO TABLE precio_semana
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;



-- json
LOAD DATA INFILE 'C:/files/PI/producto_precio_20200503.csv'
INTO TABLE precio_semana
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;



-- txt
LOAD DATA INFILE 'C:/files/PI/producto_precio_20200518.csv'
INTO TABLE precio_semana
FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '' 
LINES TERMINATED BY '\n' IGNORE 1 LINES;



-- producto_precio_20200413 CSV
-- producto_precio_20200419 XLS HOJA1
-- producto_precio_20200426 XLS HOJA0
-- producto_precio_20200503 JSON
-- producto_precio_20200518 TXT

-- query de prueba solicitado
SELECT Id_Sucursal, AVG(precio) 
FROM precio_semana
GROUP BY Id_Sucursal
HAVING Id_Sucursal = '9-1-688';