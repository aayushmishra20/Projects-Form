from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import pandas as pd
import os

app = Flask(__name__)

# ✅ Allow CORS for Vercel Frontend
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

EXCEL_FILE = "form_data.xlsx"

# ✅ Route to Check if Server is Running
@app.route("/")
def home():
    return "Flask server running on Vercel!"

# ✅ Function to Send Email
def send_email(form_data):
    sender_email = "ngatsolutions01@gmail.com"  # Your Gmail
    receiver_email = "aayushmishra82017@gmail.com"  # Recipient Email
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

# ✅ Function to Save Data to Excel
def save_to_excel(form_data):
    new_data = pd.DataFrame([form_data])

    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    df.to_excel(EXCEL_FILE, index=False)

# ✅ Route to Handle Form Submissions
@app.route("/submit-form", methods=["POST", "OPTIONS"])
def submit_form():
    try:
        # ✅ Handle CORS Preflight Requests
        if request.method == "OPTIONS":
            return jsonify({"message": "CORS preflight request success"}), 200
        
        data = request.json
        save_to_excel(data)
        email_status = send_email(data)
        return jsonify({"message": "Form submitted successfully", "email_status": email_status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Required for Vercel Deployment
def handler(event, context):
    return app(event, context)
