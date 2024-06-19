create database jet; 

use jet; 

CREATE table clientes (
	id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nome_cliente VARCHAR(100) NOT NULL,
    cpf_cliente VARCHAR(11) NOT NULL UNIQUE,
    telefone_cliente VARCHAR(15),
    email_cliente VARCHAR(100),
    veiculo_cliente VARCHAR(50),
    modelo_veiculo VARCHAR(50),
    placa_veiculo VARCHAR(50),
    tipo_servico VARCHAR(50),
    data_agendamento VARCHAR(50),
    hora_agendamento VARCHAR(50)
);

select * from clientes; 
