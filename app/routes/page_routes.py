import random
from flask import Blueprint, render_template, session, redirect, url_for
from app.models import Document, User

page_bp = Blueprint('pages', __name__)

@page_bp.route('/')
def index():
    ai_headlines = [
        "AI detects 40% increase in hidden 'Perpetual IP' clauses in design contracts.",
        "New predatory landlord tactic flagged: Non-refundable 'wear and tear' fees.",
        "ContractHawk neutralizes startup NDA containing illegal non-compete radius.",
        "Warning: SaaS lifetime deals burying auto-renewal traps in Terms of Service.",
        "Freelancers losing thousands to 'Net-90' payment terms hidden in small print."
    ]
    current_news = random.sample(ai_headlines, 3)
    return render_template('index.html', dynamic_news=current_news)

@page_bp.route('/login')
def login():
    return render_template('auth.html', mode='login')

@page_bp.route('/register')
def register():
    return render_template('auth.html', mode='register')

@page_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('pages.login'))
    return render_template('dashboard.html')

@page_bp.route('/profile')
def profile():
    if 'user_id' not in session: return redirect(url_for('pages.login'))
    return render_template('profile.html')

@page_bp.route('/vault')
def vault():
    if 'user_id' not in session: return redirect(url_for('pages.login'))
    user_docs = Document.query.filter_by(user_id=session['user_id']).order_by(Document.created_at.desc()).all()
    return render_template('vault.html', docs=user_docs)

@page_bp.route('/compare')
def compare():
    if 'user_id' not in session: return redirect(url_for('pages.login'))
    if 'latest_analysis' not in session: return redirect(url_for('pages.dashboard'))
    return render_template('compare.html')

@page_bp.route('/reviews')
def reviews():
    return render_template('reviews.html')
