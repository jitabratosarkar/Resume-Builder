from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()  # Load .env

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def generate_cover_letter(name, job_title, skills, experience):
    prompt = f"""
    Write a personalized, professional cover letter for the role of {job_title}.
    Candidate name: {name}
    Experience: {experience}
    Skills: {skills}

    The letter should sound confident, career-focused, and friendly.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Failed to generate cover letter."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        education = request.form["education"]
        experience = request.form["experience"]
        skills = request.form["skills"]
        job_title = request.form["job_title"]

        cover_letter = generate_cover_letter(name, job_title, skills, experience)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Resume", ln=True, align="C")
        pdf.multi_cell(0, 10, f"""
Name: {name}
Email: {email}
Phone: {phone}

Education:
{education}

Experience:
{experience}

Skills:
{skills}
        """)

        pdf.ln(10)
        pdf.cell(200, 10, txt="Cover Letter", ln=True, align="C")
        pdf.multi_cell(0, 10, cover_letter)

        filename = "resume_cover_letter.pdf"
        pdf.output(filename)

        return send_file(filename, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
