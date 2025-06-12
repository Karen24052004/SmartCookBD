import psycopg2
from psycopg2 import OperationalError
from psycopg2 import Error

def connect_SmartCook():
    try:
        cnx = psycopg2.connect(
            host='localhost',
            port='5432',
            database='SmartCookBD',
            user='postgres',
            password='karen24'
        )

        cursor = cnx.cursor()

        # Verifica a versão do PostgreSQL
        cursor.execute("SELECT version();")
        db_info = cursor.fetchone()
        print("Conectado ao servidor PostgreSQL versão:", db_info)

        # Verifica o banco de dados conectado
        cursor.execute("SELECT current_database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados:", linha[0])

        cursor.close()
        return cnx

    except OperationalError as e:
        print("Erro operacional ao conectar ao PostgreSQL:", e)
        return None
    except Error as e:
        print("Erro ao conectar ao PostgreSQL:", e)
        return None

tables = { 
        'RECEITA': """
            CREATE TABLE RECEITA (
            id_receita INTEGER PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            descricao VARCHAR(50) NOT NULL,
            porcoes INTEGER,
            tempo_duracao VARCHAR(20)
        );
    """,
        'CATEGORIA': """ 
            CREATE TABLE CATEGORIA (
            id_categoria INTEGER PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            descricao VARCHAR(50)
        );
    """,
        'USUARIO': """
        CREATE TABLE USUARIO (
        id_usuario INTEGER,
        nome VARCHAR(50) NOT NULL,
        cpf INTEGER NOT NULL,
        PRIMARY KEY (id_usuario)
        );
    """,
        'META_NUTRICIONAL': """
            CREATE TABLE META_NUTRICIONAL (
            id_meta INTEGER,
            proteina_dia NUMERIC,
            calorias_dia NUMERIC,
            carboidratos_dia NUMERIC,
            id_usuario INTEGER,
            PRIMARY KEY (id_meta),
            FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario)
        );
    """,
        'PAIS_ORIGEM': """ 
            CREATE TABLE PAIS_ORIGEM (
            id_pais INTEGER PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            caracteristicas VARCHAR(50),
            sigla VARCHAR(3)
        );
    """,
        'EVENTO_CULINARIO': """ 
            CREATE TABLE EVENTO_CULINARIO (
            id_evento INTEGER PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            descricao VARCHAR(50),
            data_inicio TIMESTAMP,
            data_fim TIMESTAMP,
            id_pais INTEGER,
            FOREIGN KEY (id_pais) REFERENCES PAIS_ORIGEM (id_pais)  
        );
    """,
        'UTENSILIO': """ 
            CREATE TABLE UTENSILIO (
            id_utensilio INTEGER PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            tipo VARCHAR(50),
            descricao VARCHAR(50)
        );
    """,
        'TABELA_NUTRICIONAL': """ 
            CREATE TABLE TABELA_NUTRICIONAL (
            id_tabela_nutri INTEGER PRIMARY KEY,
            fibras NUMERIC,
            gorduras NUMERIC,
            carboidratos NUMERIC,
            proteinas NUMERIC,
            calorias NUMERIC,
            id_receita INTEGER,
            FOREIGN KEY (id_receita) REFERENCES RECEITA (id_receita)
        );
    """,
        'INGREDIENTES': """ 
            CREATE TABLE INGREDIENTES (
            id_ingredientes INTEGER PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            id_receita INTEGER,
            FOREIGN KEY (id_receita) REFERENCES RECEITA (id_receita)
        );
    """,
        'ETAPA_RECEITA': """ 
            CREATE TABLE ETAPA_RECEITA (
            id_etapa INTEGER PRIMARY KEY,
            ordem INTEGER,
            instrucoes VARCHAR(100),
            tempo_aprox INTERVAL,
            id_receita INTEGER,
            FOREIGN KEY (id_receita) REFERENCES RECEITA (id_receita)
        );
    """,
        'RECEITA_PAIS': """ 
            CREATE TABLE RECEITA_PAIS (
            id_pais INTEGER,
            id_receita INTEGER,
            FOREIGN KEY (id_pais) REFERENCES PAIS_ORIGEM (id_pais),
            FOREIGN KEY (id_receita) REFERENCES RECEITA (id_receita)
        );
    """,  
        'ETAPA_DA_RECEITA': """ 
            CREATE TABLE ETAPA_DA_RECEITA (
            id_etapa INTEGER,
            id_receita INTEGER,
            FOREIGN KEY (id_etapa) REFERENCES ETAPA_RECEITA (id_etapa),
            FOREIGN KEY (id_receita) REFERENCES RECEITA (id_receita)
        );
    """, 
        'ETAPA_UTENSILIO': """ 
            CREATE TABLE ETAPA_UTENSILIO (
            id_utensilio INTEGER,
            id_etapa INTEGER,
            FOREIGN KEY (id_utensilio) REFERENCES UTENSILIO (id_utensilio),
            FOREIGN KEY (id_etapa) REFERENCES ETAPA_RECEITA (id_etapa)
        );
    """,
        'RECEITA_USUARIO': """ 
            CREATE TABLE RECEITA_USUARIO (
            id_receita INTEGER,
            id_usuario INTEGER,
            FOREIGN KEY (id_receita) REFERENCES RECEITA (id_receita),
            FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario)
        );
    """,
        'RECEITA_CATEGORIA': """ 
            CREATE TABLE RECEITA_CATEGORIA (
            id_receita INTEGER,
            id_categoria INTEGER,
            FOREIGN KEY (id_receita) REFERENCES RECEITA (id_receita),
            FOREIGN KEY (id_categoria) REFERENCES CATEGORIA (id_categoria)
        );
    """,
        'INGREDIENTES_TABELA': """ 
            CREATE TABLE INGREDIENTES_TABELA (
            id_tabela_nutri INTEGER,
            id_ingredientes INTEGER,
            FOREIGN KEY (id_tabela_nutri) REFERENCES TABELA_NUTRICIONAL (id_tabela_nutri),
            FOREIGN KEY (id_ingredientes) REFERENCES INGREDIENTES (id_ingredientes)
        );
    """,
        'RECEITA_INGREDIENTES': """ 
            CREATE TABLE RECEITA_INGREDIENTES (
            id_ingredientes INTEGER,
            id_receita INTEGER,
            FOREIGN KEY (id_ingredientes) REFERENCES INGREDIENTES (id_ingredientes),
            FOREIGN KEY (id_receita) REFERENCES RECEITA (id_receita)
        );
    """,
        'USUARIO_META': """ 
            CREATE TABLE USUARIO_META (
            id_usuario INTEGER,
            id_meta INTEGER,
            FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario),
            FOREIGN KEY (id_meta) REFERENCES META_NUTRICIONAL (id_meta)
        );
    """,
        'INTOLERANCIA': """ 
            CREATE TABLE INTOLERANCIA (
            id_ingredientes INTEGER,
            id_usuario INTEGER,
            FOREIGN KEY (id_ingredientes) REFERENCES INGREDIENTES (id_ingredientes),
            FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario)
        );
    """,
        'AVALIACAO': """ 
            CREATE TABLE AVALIACAO (
            estrelas INTEGER,
            id_usuario INTEGER,
            id_receita INTEGER,
            FOREIGN KEY (id_usuario) REFERENCES USUARIO (id_usuario),
            FOREIGN KEY (id_receita) REFERENCES RECEITA (id_receita)
        );
    """
}

inserts = { 
        'INSERT_RECEITA': """
            INSERT INTO RECEITA (id_receita, nome, descricao, porcoes, tempo_duracao) VALUES 
            (1000, 'Ratatouille', 'Receita saudável', 1, '50 min'),
            (1001, 'Feijoada', 'Receita forte', 1, '2h'),
            (1002, 'Yakisoba Vegan', 'Receita vegana', 1, '40 min'),
            (1003, 'Camarão com caldo de moqueca', 'Receita bahiana', 1, '40 min'),
            (1004, 'Ravioli de Camarão com Massa Caseira', 'Receita mais demorada', 1, '1h20min'),
            (1005, 'Brownie de Limão', 'Receita com limão', 1, '45min'),
            (1006, 'Boeuf Bourguignon', 'Receita regional francesa', 1, '3h'),
            (1007, 'Pavlova', 'Receita doce', 1, '1h40min'),
            (1008, 'Berinjela Mediterrânea', 'Receita saudável', 1, '40min'),
            (1009, 'Nhoque à Bolonhesa', 'Receita familiar', 1, '1h20min'),
            (1010, 'Bacalhau com Natas', 'Receita familiar', 1, '1h20min')
            """,
        'INSERT_CATEGORIA': """
            INSERT INTO CATEGORIA (id_categoria, nome, descricao) VALUES 
            (1011, 'Vegana', 'Sem derivados de animais'),
            (1012, 'Vegetariana', 'Sem carne animal'),
            (1013, 'Zero lactose', 'Sem derivados de leite'),
            (1014, 'Zero glúten', 'Sem derivados de trigo'),
            (1015, 'Halal', 'Permitido pela lei islâmica')
            """,
        'INSERT_USUARIO': """
            INSERT INTO USUARIO (id_usuario, nome, cpf) VALUES 
            (1016, 'João', '00000000000'),
            (1017, 'Joana', '00000000001'),
            (1018, 'Alice', '00000000002'),
            (1102, 'Alexandre', '00000000003'),
            (1103, 'Eliete', '00000000004'),
            (1104, 'Fabriane', '00000000005'),
            (1105, 'Juliano', '00000000006'),
            (1106, 'Patrick', '00000000007'),
            (1107, 'Celso', '00000000008')
            """,
        'INSERT_META_NUTRICIONAL': """
            INSERT INTO META_NUTRICIONAL (id_meta, proteina_dia, calorias_dia, carboidratos_dia, id_usuario) VALUES 
            (1031, '61.6', '2000', '200', 1016),
            (1032, '50', '1500', '140', 1017),
            (1033, '52', '1550', '150', 1018),
            (1108, '68', '2000', '200', 1102),
            (1109, '59', '1500', '140', 1103),
            (1110, '56', '1550', '150', 1104),
            (1111, '68', '2000', '200', 1105),
            (1112, '59', '1500', '140', 1106),
            (1113, '56', '1550', '150', 1107)
            """,
        'INSERT_PAIS_ORIGEM': """
            INSERT INTO PAIS_ORIGEM (id_pais, nome, caracteristicas, sigla) VALUES 
            (1019, 'França', 'Europeu', 'FR'),
            (1020, 'Brasil', 'Americano', 'BR'),
            (1021, 'Japão', 'Asiático', 'JP'),
            (1022, 'Italia', 'Europeu', 'ITA'),
            (1023, 'Estados Unidos', 'Americano', 'EUA'),
            (1024, 'Grecia', 'Europeu', 'GR'),
            (1025, 'Australia', 'Oceania', 'AUS'),
            (1026, 'Portugal', 'Europeu', 'PT')
            """,
         'INSERT_EVENTO_CULINARIO': """
            INSERT INTO EVENTO_CULINARIO (id_evento, nome, descricao, data_inicio, data_fim, id_pais) VALUES 
            (1027, 'Sabores do Cerrado', 'Festival com ingedientes do Cerrado', '15/08/2025', '18/08/2025', 1020),
            (1028, 'Noite das massas', 'Festival das massas', '04/10/2025', '06/10/2025', 1022),
            (1029, 'Fusão Oriental', 'Festival asiático', '20/07/2025', '22/07/2025', 1021),
            (1030, 'Doces do mundo', 'Festival Internacional', '12/09/2025', '15/09/2025', 1023)
            """,
        'INSERT_UTENSILIO': """
            INSERT INTO UTENSILIO (id_utensilio, nome, tipo, descricao) VALUES 
            (1034, 'Fouet', 'Arame', 'Misturar ingredientes'),
            (1035, 'Espátula', 'Silicone', 'Mexer'),
            (1036, 'Tábua', 'Madeira', 'Base para cortar'),
            (1037, 'Panela', 'Ferro', 'Para o preparo')
            """,
        'INSERT_TABELA_NUTRICIONAL': """
            INSERT INTO TABELA_NUTRICIONAL (id_tabela_nutri, fibras, gorduras, carboidratos, proteinas, calorias, id_receita) VALUES 
            (1038, '4', '6', '18', '2', '130', 1000),
            (1039, '10', '28', '40', '30', '550', 1001),
            (1040, '6', '10', '45', '8', '300', 1002),
            (1041, '4', '25', '25', '25', '400', 1003),
            (1042, '2', '20', '50', '25', '500', 1004),
            (1043, '2', '22', '48', '5', '375', 1005),
            (1044, '3', '35', '15', '45', '550', 1006),
            (1045, '2', '10', '60', '6', '350', 1007),
            (1046, '7', '12', '15', '5', '180', 1008),
            (1047, '4', '20', '70', '30', '600', 1009),
            (1048, '3', '25', '30', '35', '450', 1010)
            """,
        'INSERT_INGREDIENTES': """
            INSERT INTO INGREDIENTES (id_ingredientes, nome, id_receita) VALUES 
            (1114, 'berinjela', 1000),
            (1115, 'abobrinha', 1000),
            (1116, 'tomate', 1000),
            (1117, 'pimentão', 1000),
            (1118, 'cebola', 1000),
            (1119, 'feijão preto', 1001),
            (1120, 'linguiça calabresa', 1001),
            (1121, 'carne seca', 1001),
            (1122, 'louro', 1001),
            (1123, 'alho', 1001),
            (1124, 'macarrão para yakisoba', 1002),
            (1125, 'repolho', 1002),
            (1126, 'cenoura', 1002),
            (1127, 'molho shoyu', 1002),
            (1128, 'brócolis', 1002),
            (1129, 'camarão', 1003),
            (1130, 'leite de coco', 1003),
            (1131, 'azeite de dendê', 1003),
            (1132, 'pimentão', 1003),
            (1133, 'coentro', 1003),
            (1134, 'camarão', 1004),
            (1135, 'farinha de trigo', 1004),
            (1136, 'ovo', 1004),
            (1137, 'cebola', 1004),
            (1138, 'creme de leite', 1004),
            (1139, 'limão siciliano', 1005),
            (1140, 'chocolate branco', 1005),
            (1141, 'farinha de trigo', 1005),
            (1142, 'ovo', 1005),
            (1143, 'açúcar', 1005),
            (1144, 'carne bovina', 1006),
            (1145, 'vinho tinto', 1006),
            (1146, 'cenoura', 1006),
            (1147, 'cebola', 1006),
            (1148, 'tomilho', 1006),
            (1149, 'claras de ovo', 1007),
            (1150, 'açúcar', 1007),
            (1151, 'amido de milho', 1007),
            (1152, 'creme de leite', 1007),
            (1153, 'frutas vermelhas', 1007),
            (1154, 'berinjela', 1008),
            (1155, 'tomate seco', 1008),
            (1156, 'azeitonas pretas', 1008),
            (1157, 'manjericão', 1008),
            (1158, 'alho', 1008),
            (1159, 'batata', 1009),
            (1160, 'farinha de trigo', 1009),
            (1161, 'carne moída', 1009),
            (1162, 'molho de tomate', 1009),
            (1163, 'parmesão', 1009),
            (1164, 'bacalhau dessalgado', 1010),
            (1165, 'batata', 1010),
            (1166, 'cebola', 1010),
            (1167, 'creme de leite', 1010),
            (1168, 'azeite', 1010)
            """,
        'INSERT_ETAPA_RECEITA': """
            INSERT INTO ETAPA_RECEITA (id_etapa, ordem, instrucoes, tempo_aprox, id_receita) VALUES 
            (1065, 1, 'Corte os vegetais em cubos uniformes', '15 minutes', 1000),
            (1066, 2, 'Refogue os vegetais em azeite em fogo médio', '20 minutes', 1000),
            (1067, 3, 'Tempere com ervas e deixe cozinhar até ficarem macios', '15 minutes', 1000),

            (1068, 1, 'Deixe o feijão de molho por 8 horas', '8 hours', 1001),
            (1069, 2, 'Cozinhe o feijão com as carnes em panela de pressão', '1 hour 30 minutes', 1001),
            (1070, 3, 'Prepare o acompanhamento (arroz, couve e farofa)', '30 minutes', 1001),

            (1071, 1, 'Corte os legumes em tiras finas', '10 minutes', 1002),
            (1072, 2, 'Cozinhe o macarrão conforme instruções da embalagem', '8 minutes', 1002),
            (1073, 3, 'Refogue os legumes e misture com o macarrão', '15 minutes', 1002),
            (1074, 4, 'Adicione o molho e temperos a gosto', '7 minutes', 1002),

            (1075, 1, 'Tempere o camarão com limão e pimenta', '10 minutes', 1003),
            (1076, 2, 'Prepare o caldo com leite de coco e dendê', '20 minutes', 1003),
            (1077, 3, 'Cozinhe o camarão no calho por 10 minutos', '10 minutes', 1003),

            (1078, 1, 'Prepare a massa do ravioli', '30 minutes', 1004),
            (1079, 2, 'Prepare o recheio de camarão', '20 minutes', 1004),
            (1080, 3, 'Monte os raviolis e cozinhe em água fervente', '10 minutes', 1004),
            (1081, 4, 'Prepare o molho de acompanhamento', '20 minutes', 1004),

            (1082, 1, 'Misture os ingredientes secos', '10 minutes', 1005),
            (1083, 2, 'Adicione os ingredientes líquidos e misture bem', '10 minutes', 1005),
            (1084, 3, 'Asse em forno pré-aquecido a 180°C', '25 minutes', 1005),

            (1085, 1, 'Marine a carne por 12 horas', '12 hours', 1006),
            (1086, 2, 'Doure a carne em fogo alto', '15 minutes', 1006),
            (1087, 3, 'Cozinhe lentamente com os vegetais e vinho', '2 hours 30 minutes', 1006),

            (1088, 1, 'Bata as claras em neve', '15 minutes', 1007),
            (1089, 2, 'Adicione o açúcar gradualmente', '10 minutes', 1007),
            (1090, 3, 'Asse em forno baixo por 1h15min', '1 hour 15 minutes', 1007),
            (1091, 4, 'Decore com frutas e creme', '10 minutes', 1007),

            (1092, 1, 'Corte as berinjelas em rodelas', '10 minutes', 1008),
            (1093, 2, 'Asse as berinjelas com azeite e temperos', '20 minutes', 1008),
            (1094, 3, 'Prepare o molho de tomate mediterrâneo', '10 minutes', 1008),

            (1095, 1, 'Prepare a massa do nhoque', '30 minutes', 1009),
            (1096, 2, 'Cozinhe os nhoques em água fervente', '10 minutes', 1009),
            (1097, 3, 'Prepare o molho bolonhesa', '40 minutes', 1009),

            (1098, 1, 'Dessalgue o bacalhau por 24 horas', '24 hours', 1010),
            (1099, 2, 'Cozinhe e desfie o bacalhau', '30 minutes', 1010),
            (1100, 3, 'Prepare o creme de natas', '20 minutes', 1010),
            (1101, 4, 'Monte as camadas e leve ao forno', '30 minutes', 1010)
            """,

        'INSERT_AVALIACAO': """
            INSERT INTO AVALIACAO (estrelas, id_usuario, id_receita) VALUES 
            (5, 1016, 1001),
            (5, 1017, 1002),
            (4, 1018, 1004),
            (3, 1017, 1005),
            (4, 1016, 1002),
            (5, 1017, 1007),
            (3, 1018, 1004),
            (2, 1102, 1001),
            (5, 1103, 1003),
            (4, 1104, 1005),
            (1, 1105, 1000),
            (3, 1106, 1006),
            (4, 1107, 1010),
            (2, 1016, 1009),
            (5, 1102, 1008),
            (3, 1017, 1002),
            (4, 1103, 1007),
            (5, 1104, 1003),
            (2, 1018, 1006),
            (3, 1107, 1006),
            (4, 1102, 1008),
            (1, 1103, 1003),
            (5, 1104, 1010),
            (2, 1105, 1004),
            (3, 1106, 1009),
            (4, 1107, 1001),
            (2, 1102, 1006),
            (5, 1103, 1002),
            (3, 1105, 1000)
            """
}

drop = {
    'AVALIACAO': "DROP TABLE IF EXISTS AVALIACAO CASCADE",
    'INTOLERANCIA': "DROP TABLE IF EXISTS INTOLERANCIA CASCADE",
    'USUARIO_META': "DROP TABLE IF EXISTS USUARIO_META CASCADE",
    'RECEITA_INGREDIENTES': "DROP TABLE IF EXISTS RECEITA_INGREDIENTES CASCADE",
    'INGREDIENTES_TABELA': "DROP TABLE IF EXISTS INGREDIENTES_TABELA CASCADE",
    'RECEITA_CATEGORIA': "DROP TABLE IF EXISTS RECEITA_CATEGORIA CASCADE",
    'RECEITA_USUARIO': "DROP TABLE IF EXISTS RECEITA_USUARIO CASCADE",
    'ETAPA_UTENSILIO': "DROP TABLE IF EXISTS ETAPA_UTENSILIO CASCADE",
    'ETAPA_DA_RECEITA': "DROP TABLE IF EXISTS ETAPA_DA_RECEITA CASCADE",
    'RECEITA_PAIS': "DROP TABLE IF EXISTS RECEITA_PAIS CASCADE",
    'ETAPA_RECEITA': "DROP TABLE IF EXISTS ETAPA_RECEITA CASCADE",
    'INGREDIENTES': "DROP TABLE IF EXISTS INGREDIENTES CASCADE",
    'TABELA_NUTRICIONAL': "DROP TABLE IF EXISTS TABELA_NUTRICIONAL CASCADE",
    'UTENSILIO': "DROP TABLE IF EXISTS UTENSILIO CASCADE",
    'EVENTO_CULINARIO': "DROP TABLE IF EXISTS EVENTO_CULINARIO CASCADE",
    'PAIS_ORIGEM': "DROP TABLE IF EXISTS PAIS_ORIGEM CASCADE",
    'META_NUTRICIONAL': "DROP TABLE IF EXISTS META_NUTRICIONAL CASCADE",
    'USUARIO': "DROP TABLE IF EXISTS USUARIO CASCADE",
    'CATEGORIA': "DROP TABLE IF EXISTS CATEGORIA CASCADE",
    'RECEITA': "DROP TABLE IF EXISTS RECEITA CASCADE"
}
update = {
    'update_receita': """
        UPDATE RECEITA
        SET nome='Ratatouille',
            descricao='Prato muito saboroso e saudavel',
            porcoes='1 prato',
            tempo_duracao='1h',
        WHERE id_receita=1;
    """
}

delete = {
    'USUARIO': """
        DELETE FROM USUARIO
        WHERE id_usuario = 1017 OR id_usuario = 1018
    """
}

def drop_all_tables(connect):
    print("\n---DROP DB---")
    cursor = connect.cursor()
    for drop_name in drop:
        print(f"Tentando dropar {drop_name}...")  # Debug
        drop_description = drop[drop_name]
        try:
            print(f"Drop {drop_name}: ", end='')
            cursor.execute(drop_description)
        except psycopg2.Error as err:
            print(err.pgerror)  
        else:
            print("OK")
    connect.commit()
    cursor.close()

def create_all_tables(connect):
    print("\n---CREATE ALL TABLES---")
    cursor = connect.cursor()
    for table_name, create_query in tables.items():
        try:
            print(f"Criando tabela {table_name}: ", end='', flush=True)
            cursor.execute(create_query)
        except Exception as err:  
            print(f"Erro: {str(err)}")
        else:
            print("OK")
    connect.commit()
    cursor.close()

def show_table(connect):
    print("\n---SELECIONAR TABELA---")
    cursor = connect.cursor()
    print("Tabelas disponíveis:")
    for table_name in tables:
        print(f"- {table_name}")
    try:
        name = input("\nDigite o nome da tabela que deseja consultar: ").upper()
        if name not in tables:
            print(f"Erro: Tabela '{name}' não encontrada!")
            return
        select_query = f"SELECT * FROM {name}"
        cursor.execute(select_query)
        print(f"\nTABELA {name}:")
        print("-" * 50)
        colnames = [desc[0] for desc in cursor.description]
        print(" | ".join(colnames))
        print("-" * 50)
        rows = cursor.fetchall()
        for row in rows:
            print(" | ".join(str(item) for item in row))
    except Error as err:
        print(f"\nErro ao consultar tabela: {err.pgerror}")
    finally:
        cursor.close()

def update_value(connect):
    print("\n---SELECIONAR TABELA PARA ATUALIZAÇÃO---")
    cursor = connect.cursor()

    for table_name in tables:
        print("Nome: {}".format(table_name))

    try:
        name = input("\nDigite o nome da tabela que deseja consultar: ").upper()

        if name not in tables:
            print("Tabela não encontrada.")
            return

        print(f"Para criar a tabela {name}, foi utilizado o seguinte código:")
        print(tables[name])

        atributo = input("Digite o atributo a ser alterado: ")
        valor = input("Digite o valor a ser atribuído: ")
        codigo_f = input("Digite a coluna da chave primária: ")
        codigo = input("Digite o valor do campo da chave primária: ")

        sql = f'UPDATE {name} SET {atributo} = %s WHERE {codigo_f} = %s'
        cursor.execute(sql, (valor, codigo))

    except psycopg2.Error as err:
        print(f"Erro ao atualizar: {err.pgerror}")
    else:
        print("Atributo atualizado com sucesso.")
        connect.commit()
    cursor.close()

def insert_test(connect):
    print("\n---INSERT TEST---")
    cursor = connect.cursor()

    for insert_name in inserts:
        insert_description = inserts[insert_name]
        try:
            print("Inserindo valores para {}: ".format(insert_name), end='')
            cursor.execute(insert_description)
        except psycopg2.Error as err:
            print(f"\nErro ao inserir: {err.pgerror}")
        else:
            print("OK")
    
    connect.commit()
    cursor.close()

def update_test(connect):
    print("\n---UPDATE TEST---")
    
    cursor = connect.cursor()
    for update_name in update:
        update_description = update[update_name]
        try:
            print(f"Teste de atualização de valores para {update_name}: ", end='')
            cursor.execute(update_description)
        except psycopg2.Error as err:
            print(err.pgerror)  
        else:
            print("OK")
    connect.commit()
    cursor.close()

def delete_test(connect):
    print("\n---DELETE TEST---")
    
    cursor = connect.cursor()
    for delete_name in delete:
        delete_description = delete[delete_name]
        try:
            print(f"Teste de exclusão de valores para {delete_name}: ", end='')
            cursor.execute(delete_description)
        except psycopg2.Error as err:
            print(err.pgerror) 
        else:
            print("OK")
    connect.commit()
    cursor.close()

def consulta1(connect):
    select_query = """
    SELECT 
        R.nome AS receita,
        COUNT(A.estrelas) AS num_avaliacoes,
        ROUND(AVG(A.estrelas), 2) AS media_avaliacao
    FROM AVALIACAO A
    JOIN RECEITA R ON A.id_receita = R.id_receita
    JOIN USUARIO U ON A.id_usuario = U.id_usuario
    GROUP BY R.nome
    ORDER BY num_avaliacoes DESC;
    """
    
    print("Consulta: Número de avaliações e média por receita.")
    print("--------------------------------------------------")
    
    cursor = connect.cursor()
    cursor.execute(select_query)
    resultados = cursor.fetchall()

    print(f"{'Receita':<40} | {'Número de Avaliações':>20} | {'Média de Avaliação':>18}")
    print("-" * 85)
    for row in resultados:
        receita, num_avaliacoes, media = row
        print(f"{receita:<40} | {num_avaliacoes:>20} | {media:>18.2f}")

def consulta2(connect):
    select_query = """
    SELECT 
        r.nome AS receita,
        COUNT(DISTINCT i.nome) AS quantidade_ingredientes,
        ROUND(AVG(t.calorias), 2) AS media_calorias
    FROM 
        RECEITA r
    JOIN 
        INGREDIENTES i ON r.id_receita = i.id_receita
    JOIN 
        TABELA_NUTRICIONAL t ON r.id_receita = t.id_receita
    GROUP BY 
        r.nome
    ORDER BY 
        media_calorias DESC;
    """

    print("Consulta: Quantidade de ingredientes e média de calorias por receita.")
    print("----------------------------------------------------------------------")

    cursor = connect.cursor()
    cursor.execute(select_query)
    resultados = cursor.fetchall()

    print(f"{'Receita':<40} | {'Quantidade de Ingredientes':>26} | {'Média de Calorias':>18}")
    print("-" * 90)
    for row in resultados:
        receita, qtd_ingredientes, media_calorias = row
        print(f"{receita:<40} | {qtd_ingredientes:>26} | {media_calorias:>18.2f}")

def consulta3(connect):
    select_query = """
    SELECT
        U.nome AS usuario,
        COUNT(DISTINCT A.id_receita) AS receitas_avaliadas,
        ROUND(AVG(A.estrelas), 2) AS media_estrelas
    FROM
        USUARIO U
    JOIN
        AVALIACAO A ON U.id_usuario = A.id_usuario
    JOIN
        RECEITA R ON A.id_receita = R.id_receita
    GROUP BY
        U.nome
    ORDER BY
        receitas_avaliadas DESC;
    """

    print("Consulta: Quantidade de receitas avaliadas e média de estrelas por usuário.")
    print("---------------------------------------------------------------------------")

    cursor = connect.cursor()
    cursor.execute(select_query)
    resultados = cursor.fetchall()

    print(f"{'Usuário':<30} | {'Receitas Avaliadas':>20} | {'Média de Estrelas':>18}")
    print("-" * 75)
    for row in resultados:
        usuario, qtd_receitas, media = row
        print(f"{usuario:<30} | {qtd_receitas:>20} | {media:>18.2f}")

def crud_operacoes(connect):
    """Executa o fluxo completo de operações CRUD"""
    try:
        drop_all_tables(connect)
        create_all_tables(connect)
        insert_test(connect)
    except psycopg2.Error as e:
        print(f"\nERRO durante as operações CRUD: {e.pgerror}")
        connect.rollback()  
    except Exception as e:
        print(f"\nErro inesperado: {str(e)}")
    finally:
       
        if connect and not connect.closed:
            connect.commit()

def exit_db(connect):
    """Encerra a conexão com o banco de dados de forma segura"""
    print("\n---EXIT DB---")
    try:
        if connect and not connect.closed:
            connect.close()
            print("Conexão com o banco de dados foi encerrada com sucesso!")
    except psycopg2.Error as e:
        print(f"Erro ao fechar conexão: {e.pgerror}")

# Main
try:
    # Estabelece Conexão com o DB
    con = connect_SmartCook()

    while True:
        interface = """\n       ---MENU---
        1.  CRUD SMARTCOOK
        2.  TESTE - Create all tables
        3.  TESTE - Insert all values
        4.  TESTE - Update
        5.  TESTE - Delete
        6.  CONSULTA 01
        7.  CONSULTA 02
        8.  CONSULTA 03
        9. CONSULTA TABELAS INDIVIDUAIS
        10. UPDATE VALUES
        11. CLEAR ALL SMARTCOOK
        0.  DISCONNECT BD\n"""
        print(interface)

        try:
            choice = int(input("Opção: "))
            if choice < 0 or choice > 12:
                print("Opção inválida! Tente novamente.")
                continue
        except ValueError:
            print("Entrada inválida! Digite um número.")
            continue

        if choice == 0:
            exit_db(con)
            print("Muito obrigada(o).")
            break

        try:
            if choice == 1:
                crud_operacoes(con)

            elif choice == 2:
                create_all_tables(con)

            elif choice == 3:
                insert_test(con)

            elif choice == 4:
                update_test(con)

            elif choice == 5:
                delete_test(con)
            
            elif choice == 6:
                consulta1(con)
            
            elif choice == 7:
                consulta2(con)
            
            elif choice == 8:
                consulta3(con)

            elif choice == 9:
                show_table(con)

            elif choice == 10:
                update_value(con)

            elif choice == 11:
                drop_all_tables(con)

        except psycopg2.Error as err:
            print(f"Erro no banco de dados: {err.pgerror}")
            con.rollback()
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")

except psycopg2.Error as err:
    print(f"Erro na conexão com o banco de dados! {err.pgerror}")
except Exception as e:
    print(f"Erro inesperado: {str(e)}")
finally:
    if 'con' in locals() and con and not con.closed:
        con.close()
