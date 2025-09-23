from flask import Blueprint, request, jsonify
from db import get_db_connection

companie_bp = Blueprint("companie", __name__)

@companie_bp.route('/companies', methods=['GET'])
def get_companies():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT companie_id, name, plan, exam, value, created_at, is_active FROM companies ORDER BY created_at DESC")
        companies = cur.fetchall()
        return jsonify([
            {
                "companie_id": companie[0],
                "name": companie[1],
                "plan": companie[2],
                "exam": companie[3],
                "value": companie[4],
                "created_at": companie[5].isoformat(),
                "is_active": companie[6]
            } for companie in companies
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@companie_bp.route('/companies', methods=['POST'])
def create_companies():
    data = request.get_json()
    if not data or 'name' not in data or 'plan' not in data or 'exam' not in data or 'value' not in data:
        return jsonify({"error": "As credenciais são obrigatórias."}), 400

    name, plan, exam, value = data["name"], data["plan"], data["exam"], data["value"]
    conn = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO companies (name, plan, exam, value)
                VALUES (%s, %s, %s, %s)
                RETURNING companie_id, name, plan, exam, value, created_at, is_active""",
            (name, plan, exam, value)
        )
        new_item = cur.fetchone()
        conn.commit()
        return jsonify({
            "companie_id": new_item[0],
            "name": new_item[1],
            "plan": new_item[2],
            "exam": new_item[3],
            "value": new_item[4],
            "created_at": new_item[5].isoformat(),
            "is_active": new_item[6]
        }), 201
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@companie_bp.route('/companies/<int:companie_id>', methods=['PUT'])
def update_companies(companie_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados para atualização são obrigatórios."}), 400
    
    name = data.get('name')
    plan = data.get('plan')
    exam = data.get('exam')
    value = data.get('value')
    is_active = data.get('is_active')
    # name, access, is_active = data["name"], data["access"], data["is_active"]

    if name is None and plan is None and exam is None and value is None and is_active is None:
        return jsonify({"error": "Pelo menos um campo (name, plan, exam, value ou is_active) deve ser fornecido para atualização."}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        update_fields = []
        values = []

        if name is not None:
            update_fields.append("name = %s")
            values.append(name)
        if plan is not None:
            update_fields.append("plan = %s")
            values.append(plan)
        if exam is not None:
            update_fields.append("exam = %s")
            values.append(exam)
        if value is not None:
            update_fields.append("value = %s")
            values.append(value)
        if is_active is not None:
            update_fields.append("is_active = %s")
            values.append(is_active)
        
        values.append(companie_id)

        query = f"UPDATE companies SET {', '.join(update_fields)} WHERE companie_id = %s RETURNING companie_id, name, plan, exam, value, created_at, is_active"
        
        cur.execute(query, values)
        updated_companie = cur.fetchone()

        if updated_companie is None:
            return jsonify({"error": "Empresa não encontrada."}), 404
        
        conn.commit()
        return jsonify({
            "companie_id": updated_companie[0],
            "name": updated_companie[1],
            "plan": updated_companie[2],
            "exam": updated_companie[3],
            "value": updated_companie[4],
            "created_at": updated_companie[5].isoformat(),
            "is_active": updated_companie[6]
        }), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()

@companie_bp.route('/companies/<int:companie_id>', methods=['DELETE'])
def delete_companies(companie_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT companie_id FROM companies WHERE companie_id = %s", (companie_id,))
        companie = cur.fetchone()

        if companie is None:
            return jsonify({"error": "Empresa não encontrada."}), 404
        
        cur.execute("DELETE FROM companies WHERE companie_id = %s", (companie_id,))
        conn.commit()

        return jsonify({"message": "Empresa deletada com sucesso."}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cur.close()
            conn.close()