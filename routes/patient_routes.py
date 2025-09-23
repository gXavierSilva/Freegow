from flask import Blueprint, request, jsonify
from db import get_db_connection

patient_bp = Blueprint("patient", __name__)

@patient_bp.route('/patients', methods=['POST'])
def create_patients():
    data = request.get_json()
    if not data or 'name' not in data or 'cpf' not in data:
        return jsonify({"error": "As credenciais são obrigatórias."}), 400

    name, cpf = data["name"], data["cpf"]
    conn = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO patients (name, cpf)
                VALUES (%s, %s)
                RETURNING patient_id, name, cpf, created_at, is_active""",
            (name, cpf)
        )
        new_item = cur.fetchone()
        conn.commit()
        return jsonify({
            "patient_id": new_item[0],
            "name": new_item[1],
            "cpf": new_item[2],
            "created_at": new_item[3].isoformat(),
            "is_active": new_item[4]
        }), 201
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@patient_bp.route('/patients', methods=['GET'])
def get_patients():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT patient_id, name, cpf, created_at, is_active FROM patients ORDER BY created_at DESC")
        patients = cur.fetchall()
        return jsonify([
            {
                "patient_id": patient[0],
                "name": patient[1],
                "cpf": patient[2],
                "created_at": patient[3].isoformat(),
                "is_active": patient[4]
            } for patient in patients
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@patient_bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patients(patient_id):
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "Dados para atualização são obrigatórios."}), 400
    
    name = data.get('name')
    cpf = data.get('cpf')
    is_active = data.get('is_active')
    # name, access, is_active = data["name"], data["access"], data["is_active"]

    if name is None and cpf is None and is_active is None:
        return jsonify({"error": "Pelo menos um campo (name, cpf ou is_active) deve ser fornecido para atualização."}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        update_fields = []
        values = []

        if name is not None:
            update_fields.append("name = %s")
            values.append(name)
        if cpf is not None:
            update_fields.append("cpf = %s")
            values.append(cpf)
        if is_active is not None:
            update_fields.append("is_active = %s")
            values.append(is_active)
        
        values.append(patient_id)

        query = f"UPDATE patients SET {', '.join(update_fields)} WHERE patient_id = %s RETURNING patient_id, name, cpf, created_at, is_active"
        
        cur.execute(query, values)
        updated_patient = cur.fetchone()

        if updated_patient is None:
            return jsonify({"error": "Paciente não encontrado"}), 404
        
        conn.commit()
        return jsonify({
            "patient_id": updated_patient[0],
            "name": updated_patient[1],
            "cpf": updated_patient[2],
            "created_at": updated_patient[3].isoformat(),
            "is_active": updated_patient[4]
        }), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@patient_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patients(patient_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT patient_id FROM patients WHERE patient_id = %s", (patient_id,))
        patient = cur.fetchone()

        if patient is None:
            return jsonify({"error": "Paciente não encontrado."}), 404
        
        cur.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
        conn.commit()

        return jsonify({"message": "Paciente deletado com sucesso."}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()