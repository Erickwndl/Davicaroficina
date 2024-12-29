from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for
    
)
from waitress import serve
import os
from datetime import date
from connection_handler import connection_handler

app = Flask(__name__)


@app.route('/')
def servicos_por_dia():
    data = request.args.get('data', date.today().strftime('%Y-%m-%d'))
    servico = connection_handler.listar_por_data(data)
    total_dia = connection_handler.calcular_total_dia(data)
    return render_template('servicos_dia.html', servico=servico, data=data, total_dia=total_dia)



@app.route('/servico')
def list_servicos():
    servico = connection_handler.listar_todos()
    return render_template('servicos.html', servico=servico)


@app.route('/add-servico', methods=['GET', 'POST'])
def add_servico():
    if request.method == 'POST':
        carro = request.form.get('carro')
        placa = request.form.get('placa')
        horario = request.form.get('horario')
        dia = request.form.get('dia')
        tipo = request.form.get('tipo_servico')
        peca = request.form.get('peca_usada')
        valor_peca = request.form.get('valor_peca')
        valor_servico = request.form.get('valor_servico')
        connection_handler.insert(
            carro, placa, horario, dia, tipo, peca, valor_peca, valor_servico)
        return redirect(url_for('list_servicos'))
    return render_template('add-servico.html')


@app.route('/deletar-servico/<id>')
def deletar_servico(id: int):
    connection_handler.delete(id)
    return redirect(url_for('list_servicos'))


@app.route('/atualizar-servico/<id>', methods=['GET', 'POST'])
def update_servico(id: int):
    servico = connection_handler.buscar_por_id(id)
    if request.method == 'POST':
        carro = request.form.get('carro')
        placa = request.form.get('placa')
        horario = request.form.get('horario')
        dia = request.form.get('dia')
        tipo = request.form.get('tipo_servico')
        peca = request.form.get('peca_usada')
        valor_peca = request.form.get('valor_peca')
        valor_servico = request.form.get('valor_servico')
        connection_handler.update(
            carro, placa, horario, dia, tipo, peca, valor_peca, valor_servico, id)
        return redirect(url_for('list_servicos'))
    return render_template('update-servico.html', servico=servico)

@app.route('/buscar', methods=['GET'])
def buscar_servico():
    tipo_servico = request.args.get('tipo_servico')
    servicos = []
    if tipo_servico:
        # Use a função de busca no connection handler
        servicos = connection_handler.buscar_por_tipo(tipo_servico)
    return render_template('resultados_busca.html', servicos=servicos, tipo_servico=tipo_servico)




@app.route('/buscar/<id>')
def buscar_servico_id(id: int):
    servico = connection_handler.buscar_por_id(id)
    if request.method == 'POST':
        carro = request.form.get('carro')
        placa = request.form.get('placa')
        horario = request.form.get('horario')
        dia = request.form.get('dia')
        tipo = request.form.get('tipo_servico')
        peca = request.form.get('peca_usada')
        valor_peca = request.form.get('valor_peca')
        valor_servico = request.form.get('valor_servico')
        connection_handler.update(
            carro, placa, horario, dia, tipo, peca, valor_peca, valor_servico, id)
        return redirect(url_for('list_servicos'))
    return render_template('servico.html', servico=servico)

@app.route('/estoque')
def estoque_pecas():
    pecas = connection_handler.listar_pecas()
    return render_template('estoque.html', pecas=pecas)

@app.route('/adicionar-peca', methods=['GET', 'POST'])
def adicionar_peca():
    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])
        connection_handler.adicionar_peca(nome, tipo, quantidade, preco)
        return redirect(url_for('estoque_pecas'))
    return render_template('adicionar_peca.html')

@app.route('/editar-peca/<int:id>', methods=['GET', 'POST'])
def editar_peca(id):
    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])
        connection_handler.atualizar_peca(id, nome, tipo, quantidade, preco)
        return redirect(url_for('estoque_pecas'))
    pecas = connection_handler.listar_pecas()
    peca = next((p for p in pecas if p['id'] == id), None)
    return render_template('editar_peca.html', peca=peca)

@app.route('/pecas-em-falta')
def pecas_em_falta():
    pecas_faltando = [peca for peca in connection_handler.listar_pecas() if peca['quantidade'] == 0]
    return render_template('pecas_em_falta.html', pecas=pecas_faltando)

@app.route('/buscar-peca', methods=['GET', 'POST'])
def buscar_peca():
    peca = None
    if request.method == 'POST':
        id_peca = int(request.form['id'])
        pecas = connection_handler.listar_pecas()
        peca = next((p for p in pecas if p['id'] == id_peca), None)
    return render_template('buscar_peca.html', peca=peca)






if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Usa PORT se definido, senão usa 5001
    serve(app, host='0.0.0.0', port=port)
    # connection_handler.close_connection()
    # connection_handler.create_table()
    # connection_handler.insert_sample_data()
    # print(connection_handler.listar_todos())
    # connection_handler.atualizar(1, 'Maria', 25, 'Python', 9.5)
    # print(connection_handler.buscar_por_id(1))
    # connection_handler.excluir(1)
