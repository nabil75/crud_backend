from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import subprocess
import io
import os
import time
import tempfile

def generate_and_open_pdf():

    pdf_buffer = io.BytesIO()
    # Définir le format de la page
    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4

    # Ajouter du texte
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 50, "Rapport d'Analyse")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 100, "Voici un exemple de PDF généré avec des tableaux, des images et du texte.")

    # Ajouter une image
    pdf.drawImage("example_image.png", 50, height - 200, width=200, height=100)

    # Ajouter un tableau
    data = [
        ["Niveau", "Nombre de réponses", "Pourcentage"],
        ["Très satisfait", 45, "45%"],
        ["Satisfait", 30, "30%"],
        ["Neutre", 15, "15%"],
        ["Insatisfait", 10, "10%"],
    ]

    table = Table(data, colWidths=[150, 150, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    # Positionner le tableau
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 50, height - 300)

    # Ajouter une page supplémentaire
    pdf.showPage()

    # Finaliser le fichier PDF
    pdf.save()

 # Se positionner au début du flux mémoire
    pdf_buffer.seek(0)

     # Créer un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(pdf_buffer.read())
        temp_file_path = temp_file.name  # Conserver le chemin

    # Ouvrir le fichier temporaire avec l'application par défaut
    try:
        if os.name == 'nt':  # Windows
            os.startfile(temp_file_path)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.run(['open', temp_file_path], check=True)  # macOS
            # subprocess.run(['xdg-open', temp_file_path], check=True)  # Linux
    finally:
        # Introduire un délai avant suppression
        time.sleep(5)  # Temps d'ouverture de l'application PDF
        # os.remove(temp_file_path)  # Supprimer le fichier temporaire

# Appeler la fonction
generate_and_open_pdf()