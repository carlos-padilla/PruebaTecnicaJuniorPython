DROP DATABASE Sancho_Limitada_Data_Base;

CREATE DATABASE IF NOT EXISTS Sancho_Limitada_Data_Base;

USE Sancho_Limitada_Data_Base;

CREATE TABLE IF NOT EXISTS clientes(
	id_cliente INT NOT NULL AUTO_INCREMENT,
	cedula_cliente CHAR(11) NOT NULL,
	nombre_cliente CHAR(20) NOT NULL,
    direccion_cliente CHAR(40) NOT NULL,
    telefono_cliente CHAR(10) NOT NULL,
    foto_cliente VARCHAR(255) NOT NULL,
	PRIMARY KEY(id_cliente)
)ENGINE = INNODB;
CREATE TABLE IF NOT EXISTS productos(
	id_producto INT NOT NULL AUTO_INCREMENT,
	codigo_producto CHAR(120) NOT NULL,
	categoria_producto CHAR(120) NOT NULL,
    nombre_producto CHAR(40) NOT NULL,
    precio_producto CHAR(255) NOT NULL,
    cantidad_bodega_producto INT(100),
    estado_producto ENUM('ACTIVO', 'INACTIVO'),
	PRIMARY KEY(id_producto)
)ENGINE = INNODB;
CREATE TABLE IF NOT EXISTS facturas(
	id_factura INT NOT NULL AUTO_INCREMENT,
	codigo_factura CHAR(120) NOT NULL,
	cliente_compra_factura CHAR(20) NOT NULL,
    productos_factura CHAR(40) NOT NULL,
    cantidad_productos_factura INT(100) NOT NULL,
    fecha_compra_factura DATE,
    valor_total_factura CHAR(100),
    metodo_pago_factura CHAR(40),
	PRIMARY KEY(id_factura),
    id_relacion_cliente INT NOT NULL,
    CONSTRAINT factura_cliente
    FOREIGN KEY(id_relacion_cliente)
		REFERENCES clientes(id_cliente)
		ON DELETE CASCADE
)ENGINE = INNODB;
CREATE TABLE IF NOT EXISTS facturas_productos(
	id_relacion_facturas INT NOT NULL,
    id_relacion_producto INT NOT NULL,
    PRIMARY KEY(id_relacion_facturas, id_relacion_producto),
    CONSTRAINT factura_producto
    FOREIGN KEY(id_relacion_facturas)
    REFERENCES facturas(id_factura)
    ON DELETE CASCADE,
    CONSTRAINT producto_factura
    FOREIGN KEY(id_relacion_producto)
    REFERENCES productos(id_producto)   
)ENGINE = INNODB;
