from flask import Blueprint, render_template, session, redirect, url_for, current_app
import os
import json

homeBP = Blueprint('home', __name__)

def _load_reports():
    data_dir = os.path.join(current_app.root_path, "data")
    path = os.path.join(data_dir, "reports.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@homeBP.route('/')
def home():
    if 'user_id' in session:
        user_name = session.get('user_name', 'Preeti Shrestha')
        
        all_reports = _load_reports()
        
        recent_reports = all_reports[-5:]
        recent_reports.reverse()
        
        total_count = len(all_reports)
        pending_count = sum(1 for r in all_reports if r.get('status', 'Pending') == 'Pending')
        resolved_count = sum(1 for r in all_reports if r.get('status') == 'Resolved')
        
        summary = {
            'total': total_count,
            'pending': pending_count,
            'resolved': resolved_count
        }
        
        return render_template(
            "user/dashboard.html", 
            name=user_name, 
            summary=summary, 
            recent_reports=recent_reports
        )
        
    return render_template("home.html")