from flask import Blueprint, render_template, jsonify

landing_bp = Blueprint("landing", __name__)

# Rotas que renderizam páginas de cunho "Landing Page" (Demonstração)
@landing_bp.route('/main', methods=['GET'])
def main_page():
    return render_template('areadeagendamento.html')

@landing_bp.route('/billing', methods=['GET'])
def billing_page():
    return render_template('faturamento.html')

@landing_bp.route('/press', methods=['GET'])
def press_page():
    return render_template('imprensa.html')

@landing_bp.route('/doctor', methods=['GET'])
def doctor_page():
    return render_template('medico.html')

@landing_bp.route('/associate', methods=['GET'])
def associate_page():
    return render_template('parceiro.html')

@landing_bp.route('/privacy', methods=['GET'])
def privacy_page():
    return render_template('privacidade.html')

@landing_bp.route('/records', methods=['GET'])
def records_page():
    return render_template('prontuario.html')

@landing_bp.route('/services', methods=['GET'])
def services_page():
    return render_template('servicos.html')

@landing_bp.route('/aboutus', methods=['GET'])
def aboutus_page():
    return render_template('sobrenos.html')

@landing_bp.route('/telemedicine', methods=['GET'])
def telemedicine_page():
    return render_template('telemedicina.html')
