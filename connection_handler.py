from dataclasses import dataclass
import pymysql.cursors
from pymysql.cursors import DictCursor
from pymysql import Connection


@dataclass(kw_only=True)
class connectionHandler:
    host: str
    username: str
    password: str
    database: str
    cursor: DictCursor = None
    conn: Connection = None

    def __post_init__(self):
        self.conn = self.criar_conexao()
        self.cursor = self.conn.cursor()

    def criar_conexao(self):
        try:
            conexao = pymysql.connect(
                host=self.host,
                port=46440,  # Adicione a porta explicitamente
                user=self.username,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Conexão estabelecida com sucesso!")
            return conexao
        except pymysql.MySQLError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def insert(self, carro, placa, horario, dia, tipo_servico, peca_usada, valor_peca, valor_servico):
        sql = "INSERT INTO servico (carro, placa, horario, dia, tipo_servico, peca_usada, valor_peca, valor_servico) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (carro, placa, horario, dia,
                            tipo_servico, peca_usada, valor_peca, valor_servico))
        self.conn.commit()

    def listar_todos(self):
        sql = "SELECT * FROM servico"
        self.cursor.execute(sql)
        servicos = self.cursor.fetchall()
        return servicos

    def buscar_por_id(self, id):
        sql = "SELECT * FROM servico WHERE id = %s"
        self.cursor.execute(sql, id)
        servico = self.cursor.fetchone()
        return servico
    
    def buscar_por_tipo(self, tipo_servico):
        sql = "SELECT * FROM servico WHERE tipo_servico = %s"
        self.cursor.execute(sql, tipo_servico)
        servicos = self.cursor.fetchall()
        return servicos


    def buscar_por_carro(self, carro):
        sql = "SELECT * FROM servico WHERE carro = %s"
        self.cursor.execute(sql, carro)
        servicos = self.cursor.fetchall()
        return servicos
    
    def listar_por_data(self, data):
        sql = "SELECT * FROM servico WHERE dia = %s"
        self.cursor.execute(sql, (data,))
        servicos = self.cursor.fetchall()
        return servicos

    def update(self, carro, placa, horario, dia, tipo_servico, peca_usada, valor_peca, valor_servico, id):
        sql = "UPDATE servico SET carro = %s, placa =  %s, horario = %s, dia = %s, tipo_servico = %s, peca_usada = %s, valor_peca = %s, valor_servico = %s WHERE id = %s"
        self.cursor.execute(sql, (carro, placa, horario, dia,
                            tipo_servico, peca_usada, valor_peca, valor_servico, id))
        self.conn.commit()

    def delete(self, id):
        sql = "DELETE FROM servico WHERE id = %s"
        self.cursor.execute(sql, id)
        self.conn.commit()

    def calcular_total_dia(self, dia):
        sql = "SELECT SUM(valor_servico) AS total_dia FROM servico WHERE dia = %s"
        self.cursor.execute(sql, (dia,))
        total = self.cursor.fetchone()
        return total['total_dia'] if total['total_dia'] else 0

    def listar_pecas(self):
        sql = "SELECT * FROM pecas"
        self.cursor.execute(sql)
        pecas = self.cursor.fetchall()
        return pecas

    def adicionar_peca(self, nome, tipo, quantidade, preco):
        sql = "INSERT INTO pecas (nome, tipo, quantidade, preco) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (nome, tipo, quantidade, preco))
        self.conn.commit()

    def atualizar_peca(self, id, nome, tipo, quantidade, preco):
        sql = "UPDATE pecas SET nome = %s, tipo = %s, quantidade = %s, preco = %s WHERE id = %s"
        self.cursor.execute(sql, (nome, tipo, quantidade, preco, id))
        self.conn.commit()

    # Remove uma peça
    def remover_peca(self, id):
        sql = "DELETE FROM pecas WHERE id = %s"
        self.cursor.execute(sql, (id,))
        self.conn.commit()


connection_handler = connectionHandler(
    host='autorack.proxy.rlwy.net',
    username='root',
    password='rCMuDIDgqqbEKubpBcdcfyDjasMGBVxN',
    database='railway'
)


