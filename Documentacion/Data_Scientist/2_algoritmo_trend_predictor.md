## Documentación Técnica para Script de Base de Datos

### Descripción General
Este script SQL se utiliza para configurar una base de datos llamada `Legacy_Inmobiliaria` en MySQL. El script incluye la creación de tablas y la inserción de datos de ejemplo para un sistema de gestión inmobiliaria.

### Pasos del Script

1. **Eliminar Base de Datos Existente:**
   ```sql
   DROP DATABASE IF EXISTS legacy_inmobiliaria;
   ```

2. **Crear Base de Datos:**
   ```sql
   CREATE DATABASE IF NOT EXISTS Legacy_Inmobiliaria;
   USE Legacy_Inmobiliaria;
   ```

3. **Crear Tabla `Propiedades`:**
   - Almacena información sobre las propiedades.
   ```sql
   CREATE TABLE Propiedades (
       ID_Propiedad INT AUTO_INCREMENT PRIMARY KEY,
       Direccion VARCHAR(255) NOT NULL,
       ID_Propietario INT NOT NULL
   );
   ```

4. **Crear Tabla `Publicaciones_Alquileres`:**
   - Almacena información sobre publicaciones y alquileres.
   ```sql
   CREATE TABLE Publicaciones_Alquileres (
       Publicacion INT AUTO_INCREMENT PRIMARY KEY,
       ID_Propiedad INT,
       Fecha_Publicacion DATE,
       Fecha_Alquiler DATE,
       Valor_Alquiler_Pretendido DECIMAL(10, 2),
       ID_Vendedor INT,
       ID_Contrato INT,
       FOREIGN KEY (ID_Propiedad) REFERENCES Propiedades(ID_Propiedad)
   );
   ```

5. **Crear Tabla `Inquilinos`:**
   - Almacena información sobre los inquilinos.
   ```sql
   CREATE TABLE Inquilinos (
       ID_Inquilino INT AUTO_INCREMENT PRIMARY KEY,
       Nombre VARCHAR(255),
       Fecha_Alta DATE,
       Telefono VARCHAR(15),
       valoracion_res DECIMAL(2, 1) CHECK (valoracion_res IN (0, 0.5, 1)),
       res_asian TINYINT(1) CHECK (res_asian IN (0, 1)),
       res_latin TINYINT(1) CHECK (res_latin IN (0, 1)),
       res_north TINYINT(1) CHECK (res_north IN (0, 1)),
       res_veg TINYINT(1) CHECK (res_veg IN (0, 1)),
       valoracion_rel DECIMAL(2, 1) CHECK (valoracion_rel IN (0, 0.5, 1)),
       religion TINYINT(1) CHECK (religion IN (0, 1, 2, 3, 4, 5)),
       valoracion_rec DECIMAL(2, 1) CHECK (valoracion_rec IN (0, 0.5, 1)),
       recreation TINYINT(1) CHECK (recreation IN (0, 1, 2, 3))
   );
   ```

6. **Crear Tabla `Contratos`:**
   - Almacena información sobre los contratos de alquiler.
   ```sql
   CREATE TABLE Contratos (
       ID_Contrato INT AUTO_INCREMENT PRIMARY KEY,
       Fecha_Alquiler DATE,
       ID_Inquilino INT,
       ID_Propiedad INT,
       Valor_Alquiler DECIMAL(10, 2),
       Fecha_Finalizacion DATE,
       ID_Contrato_Nuevo INT,
       Satisfaccion_Propiedad DECIMAL(2, 1),
       Satisfaccion_Barrio DECIMAL(2, 1),
       Satisfaccion_Vendedor DECIMAL(2, 1),
       Satisfaccion_General DECIMAL(2, 1),
       FOREIGN KEY (ID_Inquilino) REFERENCES Inquilinos(ID_Inquilino),
       FOREIGN KEY (ID_Propiedad) REFERENCES Propiedades(ID_Propiedad)
   );
   ```

7. **Insertar Datos en la Tabla `Propiedades`:**
   - Inserta 50 registros de ejemplo.
   ```sql
   INSERT INTO Propiedades (ID_Propiedad, Direccion, ID_Propietario)
   VALUES
       (1, '123 Main St, Los Angeles, CA', 1),
       -- más filas aquí
       (50, '4747 Poplar St, Los Angeles, CA', 50);
   ```

8. **Insertar Datos en la Tabla `Inquilinos`:**
   - Inserta 56 registros de ejemplo.
   ```sql
   INSERT INTO Inquilinos (ID_Inquilino, Nombre, Telefono, valoracion_res, res_asian, res_latin, res_north, res_veg, valoracion_rel, religion, valoracion_rec, recreation, Fecha_Alta)
   VALUES
       (1, 'Inquilino 1', '555-0001', 1, 0, 1, 0, 1, 0.5, 1, 1, 2, '2022-12-08'),
       -- más filas aquí
       (56, 'Inquilino 56', '555-0056', 0.5, 1, 0, 1, 0, 1, 3, 0.5, 3, '2022-01-24');
   ```

9. **Insertar Datos en la Tabla `Contratos`:**
   - Inserta registros de ejemplo.
   ```sql
   INSERT INTO Contratos (ID_Contrato, Fecha_Alquiler, ID_Inquilino, ID_Propiedad, Valor_Alquiler, Fecha_Finalizacion, ID_Contrato_Nuevo, Satisfaccion_Propiedad, Satisfaccion_Barrio, Satisfaccion_Vendedor, Satisfaccion_General)
   VALUES
       (1, '2023-01-01', 1, 1, 1000, '2024-01-01', 2, 5, 4, 4, 4),
       -- más filas aquí
       (14, '2023-08-01', 7, 7, 1100, '2024-08-01', NULL, 5, 5, 4, 5);
   ```

### Consideraciones Adicionales

- **Llaves Foráneas:** Las tablas `Publicaciones_Alquileres` y `Contratos` tienen llaves foráneas que aseguran la integridad referencial con las tablas `Propiedades` e `Inquilinos`.
- **Restricciones y Chequeos:** Se utilizan restricciones y chequeos (`CHECK`) para validar los valores en ciertas columnas, asegurando que los datos sean consistentes y dentro de los rangos esperados.
- **Datos de Ejemplo:** Se proporcionan datos de ejemplo para cada tabla, lo que facilita la prueba y validación del sistema una vez que la base de datos está creada.

Este script proporciona una estructura básica para una base de datos de gestión inmobiliaria, permitiendo el almacenamiento y manejo de propiedades, inquilinos, publicaciones de alquiler y contratos.