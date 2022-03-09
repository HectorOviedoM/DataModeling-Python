# DataModeling-Python

Data Engineer Programming Test

Pregunta 1
1-Como resolvería este tipo de petición? Explique detalladamente el proceso de limpieza y transformación del modelo inicial. ¿Qué tecnologías utilizaría y por qué?
Pasos para cumplir con la petición:


1-usando la tabla de origen crearía las tablas dimensiones DIMUSUARIOS, DIMEVENTO , DIMSEGMENTO y DIMSESSION, y una tabla de hecho FactSesiónes.


•	La tabla de hecho tendría: USER_ID, EVENT_ID , SEGMENT_ID Y SESSION_ID como FK, crash_detection y time_spent

•	La tabla de DIMUSUARIOS tendría user_id como clave principal, user_city

•	La tabla DIMEVENTO tendría EVENT_ID como clave principal, server_time y evento_description

•	La tabla DIMSESSION tendría SESSION_ID como clave principal, device_browser , device_movile y device_os

•	La tabla DIMSEGMENTO tendría SEGMENT_ID como clave principal , segment_description


2- a nivel general utilizaría una base de datos relacional, por cuestión de performance, más robusta , mejores features y ser open Source elegiría PostgreSQL por sobre otros gestores. 
En caso de tener que mover la tabla de origen optaría por spark(pyspark) ya que sqoop,que es una herramienta ideal para esto, esta deprecada y si se necesitara planificar ejecución de procesos batch lo haría con airflow



Ejercicio 1                
Realice el DER que de soporte al modelo dimensional solicitado por la banca privada.

![image](https://user-images.githubusercontent.com/63317932/157447080-d5703e99-fd7a-40d3-8f02-81be8f45cbd7.png)

 

Ejercicio 2
En caso de necesitarlo se crea la tabla origen en postgres y se cargan los datos con python/pyspark:
CREATE TABLE origin_table (user_id serial PRIMARY KEY,session_id int UNIQUE NULL,segment_id int UNIQUE NULL,segment_description VARCHAR(100) NULL,	user_city VARCHAR(100) NULL,server_time TIMESTAMP NULL,device_browser VARCHAR ( 50 ) NULL,device_os VARCHAR ( 50 ) NULL,device_mobile VARCHAR ( 50 ) NULL,time_spent int null,event_id int UNIQUE NULL,event_description VARCHAR(100) NULL,crash_detection VARCHAR(100) NULL);

Teniendo los datos cargados en PostgreSQL:

•	create table dimusuarios (
     			user_id serial primary key,
     			user_city text not null);
			
•	create table dimevento (
     			event_id serial primary key,
     			server_time date not null,
     			evento_description text not null);
			
•	create table dimsegmento (
     			segment_id serial primary key,
     			segment_description text not null);
			
•	create table dimsession (
     			sesión_id serial primary key,
     			device_os text not null default 'unknown',
     			device_browser text not null,
			device_movile text not null);
			
•	create table factsessiones ( user_id integer references dimusuarios, 
			     event_id integer references dimevento,  
                             segment_id integer references dimsegmento,
                             sesión_id integer references dimsession, 
                             time_spent integer, 
                             crash_detection text,  
                             constraint pk primary key (user_id, event_id,segment_id,sesión_id))

						  

•	inserts:

o	INSERT INTO dimevento (event_id, server_time, evento_description)
SELECT event_id, server_time, event_description FROM origin_table

o	INSERT INTO dimsession (sesión_id,device_os,device_browser,device_movile)
SELECT session_id,device_os,device_browser,device_mobile FROM origin_table;

o	INSERT INTO dimsegmento (segment_id,segment_description) SELECT segment_id,segment_description FROM origin_table;

o	INSERT INTO dimusuarios(user_id,user_city) SELECT user_id,user_city FROM origin_table;



Ejercicio 3:

SELECT  user_id,count(session_id) FROM dimevento INNER JOIN factsessiones ON dimevento.event_id = factsessiones.event_id where date_part('month',server_time) = date_part('month',CURRENT_DATE) group by user_id  limit 10  ;



Pregunta 2
¿Qué parámetros de spark tendría en cuenta a la hora de realizar dicha ingesta? Explique brevemente en que consta cada uno de ellos. ¿En qué formato de compresión escribiría los resultados? ¿Por qué?


Al momento de realizar dicha ingesta tendría en cuenta principalmente las configuracioens sobre los ejecutors de spark  y el driver , por nombrar algunos, en relacion a los ejecutors seria la cantidad de ejecutores(spark.executor.instances), la cantidad de memoria utilizada por cada ejecutor(spark.executor.memory), y los núcleos de cada ejecutor (spark.executor.cores) y en relacion al driver la cantidad de memoria a utilizar(spark.driver.memory)

Por otro lado , sobre el formato del archivo, Lo escribiría en formato avro ya que hay relativamente poca cantidad de columnas por lo que ser un formato orientado a filas no es una desventaja , es adecuado para operaciones de escritura intensiva como la que necesitamos y puede ser utilizado en procesos streamming en caso de necesitarlo. en caso de no utilizar avro me inclinaria por el formato parquet.


Pregunta 3
Describa brevemente que implementaría para garantizar la confiabilidad de los datos.

hablando en forma general implementaría test de calidad de datos, con esto me refiero a someter a diferentes tablas de mi datawarehouse a pruebas para verificar que ,por ejemplo, una columna no tenga nulos o que sus valores sean unicos en caso de que debieran serlos.
Una herramienta que se podría utilizar es dbt, es una herramienta que se encarga exclusivamente de la transformación de los datos con la ventaja de que ofrece test automáticos sobre nuestras tablas que aseguran una calidad de datos, sino que además realiza documentación de forma automática de nuestras transformaciones, teniendo así un mayor control del recorrido de nuestro dato incluyendo su origen y las transformaciones que le fueron aplicadas. Es una herramienta open Source que tiene conexiones nativas con herramientas como redshift , snowflake o bigquery.
Otras alternativas que se podrían estudiar, ya sin modificar mucho la arquitectura, serian librerías como lo es pydeequ, la cual es una librería de python para asegurar la calidad de los datos, misma función que mencione anteriormente por ejemplo encontrar valores nulos, distribuciones de datos incorrectas ,etc. Tambien podría mencionar “great_expectation” que es otra librería de python que cumple una función similar.
