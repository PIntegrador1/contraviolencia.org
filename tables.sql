DROP TABLE IF exists users;
DROP TABLE IF exists registros;

CREATE OR REPLACE FUNCTION set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.ref =  now()::timestamp(0);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;




CREATE TABLE users (id SERIAL PRIMARY KEY,
                    ref TIMESTAMP DEFAULT  now()::timestamp(0),
                    usuario varchar(60) not null,
                    senha varchar(10) not null
                    );

CREATE TABLE registros (id SERIAL PRIMARY KEY,
                        ref TIMESTAMP DEFAULT  now()::timestamp(0),
                        nome varchar(60)  NULL,
                        dt_nasc DATE NULL,
                        endereco varchar(60) NULL,
                        grupo_violacao varchar(60)  NULL,
                        observacoes varchar(10000)  NULL
                        );

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON public.users
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON public.registros
FOR EACH ROW
EXECUTE FUNCTION set_timestamp();
