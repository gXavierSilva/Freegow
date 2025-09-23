from flask import Blueprint, request, jsonify
from db import get_db_connection

clinic_bp = Blueprint("clinic", __name__)

@clinic_bp.route('/clinics', methods=['GET'])
def get_clinics():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT clinic_id, name, cnpj, street, number, city, created_at, is_active FROM clinics ORDER BY created_at DESC")
        clinics = cur.fetchall()
        return jsonify([
            {
                "clinic_id": clinic[0],
                "name": clinic[1],
                "cnpj": clinic[2],
                "street": clinic[3],
                "number": clinic[4],
                "city": clinic[5],
                "created_at": clinic[6].isoformat(),
                "is_active": clinic[7]
            } for clinic in clinics
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@clinic_bp.route('/clinics', methods=['POST'])
def create_clinics():
    data = request.get_json()
    # Verificação (otimizar)
    # if not data or 'name' not in data or 'plan' not in data or 'exam' not in data or 'value' not in data:
    #     return jsonify({"error": "As credenciais são obrigatórias."}), 400

    name, cnpj, street, number, city = data["name"], data["cnpj"], data["street"], data["number"], data["city"]
    conn = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO clinics (name, cnpj, street, number, city)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING clinic_id, name, cnpj, street, number, city, created_at, is_active""",
            (name, cnpj, street, number, city)
        )
        new_item = cur.fetchone()
        conn.commit()
        return jsonify({
            "clinic_id": new_item[0],
            "name": new_item[1],
            "cnpj": new_item[2],
            "street": new_item[3],
            "number": new_item[4],
            "city": new_item[5],
            "created_at": new_item[6].isoformat(),
            "is_active": new_item[7]
        }), 201
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@clinic_bp.route('/clinics/<int:clinic_id>', methods=['PUT'])
def update_clinics(clinic_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados para atualização são obrigatórios."}), 400
    
    name = data.get('name')
    cnpj = data.get('cnpj')
    street = data.get('street')
    number = data.get('number')
    city = data.get('city')
    is_active = data.get('is_active')
    # name, access, is_active = data["name"], data["access"], data["is_active"]

    if name is None and cnpj is None and street is None and number is None and city is None and is_active is None:
        return jsonify({"error": "Pelo menos um campo (name, cnpj, street, number, city ou is_active) deve ser fornecido para atualização."}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        update_fields = []
        values = []

        if name is not None:
            update_fields.append("name = %s")
            values.append(name)
        if cnpj is not None:
            update_fields.append("cnpj = %s")
            values.append(cnpj)
        if street is not None:
            update_fields.append("street = %s")
            values.append(street)
        if number is not None:
            update_fields.append("number = %s")
            values.append(number)
        if city is not None:
            update_fields.append("city = %s")
            values.append(city)
        if is_active is not None:
            update_fields.append("is_active = %s")
            values.append(is_active)
        
        values.append(clinic_id)

        query = f"UPDATE clinics SET {', '.join(update_fields)} WHERE clinic_id = %s RETURNING clinic_id, name, cnpj, street, number, city, created_at, is_active"
        
        cur.execute(query, values)
        updated_clinic = cur.fetchone()

        if updated_clinic is None:
            return jsonify({"error": "Clinica não encontrada."}), 404
        
        conn.commit()
        return jsonify({
            "clinic_id": updated_clinic[0],
            "name": updated_clinic[1],
            "cnpj": updated_clinic[2],
            "street": updated_clinic[3],
            "number": updated_clinic[4],
            "city": updated_clinic[5],
            "created_at": updated_clinic[6].isoformat(),
            "is_active": updated_clinic[7]
        }), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@clinic_bp.route('/clinics/<int:clinic_id>', methods=['DELETE'])
def delete_clinics(clinic_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT clinic_id FROM clinics WHERE clinic_id = %s", (clinic_id,))
        companie = cur.fetchone()

        if companie is None:
            return jsonify({"error": "Clinica não encontrada."}), 404
        
        cur.execute("DELETE FROM clinics WHERE clinic_id = %s", (clinic_id,))
        conn.commit()

        return jsonify({"message": "Clinica deletada com sucesso."}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()