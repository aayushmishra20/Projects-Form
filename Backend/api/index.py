from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import pandas as pd
import os

app = Flask(__name__)

# ✅ Allow CORS for your Vercel frontend
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from any origin

EXCEL_FILE = "form_data.xlsx"

@app.route("/")
def home():
    return "Flask server running on Vercel!"

@app.route("/submit-form", methods=["POST", "OPTIONS"])
def submit_form():
    try:
        if request.method == "OPTIONS":
            return jsonify({"message": "CORS preflight request success"}), 200
        
        data = request.json
        save_to_excel(data)
        email_status = send_email(data)
        return jsonify({"message": "Form submitted successfully", "email_status": email_status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_email(form_data):
    sender_email = "ngatsolutions01@gmail.com"
    receiver_email = "aayushmishra82017@gmail.com"
    subject = "New Project Requirement Form Submission"

    body = f"""
    Name: {form_data['name']}
    Email: {form_data['email']}
    Company: {form_data['company']}
    Phone: {form_data['phone']}
    Projects: {form_data['projects']}
    Other Requirements: {form_data['customRequest']}
    """
    
    message = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, os.environ.get("EMAIL_PASSWORD"))  # ✅ Secure App Password
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        return "Email sent successfully"
    except Exception as e:
        return f"Error sending email: {str(e)}"

def save_to_excel(form_data):
    new_data = pd.DataFrame([form_data])
    
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    df.to_excel(EXCEL_FILE, index=False)

# ✅ Required for Vercel Deployment
def handler(event, context):
    return app(event, context)
