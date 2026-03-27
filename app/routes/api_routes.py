import os
import json
from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.utils import secure_filename
from app.models import Document, User
from app import db
from app.ai_pipeline import extract_text, audit_contract

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/scan', methods=['POST'])
def scan_document():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized access'}), 401

    file = request.files.get('document')
    if not file or file.filename == '':
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
    # Securely save the file
    filename = secure_filename(file.filename)
    upload_dir = os.path.join(current_app.root_path, '../uploads')
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    try:
        # 1. Get User Context for Personalization
        user = User.query.get(session['user_id'])
        context = f"Name: {user.full_name}, Country: {user.country}, Style: {user.negotiation_style}, Tone: {user.jargon_filter}"
        
        # 2. Run the AI Pipeline
        raw_text = extract_text(filepath)
        if not raw_text.strip():
            return jsonify({'success': False, 'error': 'Could not read document text.'}), 400
            
        analysis_json = audit_contract(raw_text, context)
        analysis_data = json.loads(analysis_json)

        # 3. Calculate Risk & Update Database
        avg_risk = sum(item['risk'] for item in analysis_data) // len(analysis_data) if analysis_data else 0
        
        new_doc = Document(
            user_id=user.id,
            filename=filename,
            risk_score=avg_risk,
            status='completed'
        )
        db.session.add(new_doc)
        db.session.commit()

        # 4. Cache results in session for immediate display on /compare
        session['latest_analysis'] = analysis_data
        session['latest_filename'] = filename
        session['latest_score'] = avg_risk
        session['latest_country'] = user.country
        session['latest_style'] = user.negotiation_style

        return jsonify({'success': True, 'doc_id': new_doc.id})

    except Exception as e:
        print(f"Backend Error: {e}")
        return jsonify({'success': False, 'error': 'The AI engine encountered a processing error.'}), 500
