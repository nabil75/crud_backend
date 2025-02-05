import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt

# Example Matplotlib chart function
def generate_chart_1():
    """Generate a sample chart and return it as a BytesIO object."""
    buffer = io.BytesIO()
    plt.figure(figsize=(5, 3))
    plt.plot([1, 2, 3], [4, 5, 6], label="Chart 1")
    plt.title("Sample Chart 1")
    plt.legend()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)  # Rewind the buffer
    return buffer

def generate_chart_2():
    """Generate another sample chart and return it as a BytesIO object."""
    buffer = io.BytesIO()
    plt.figure(figsize=(5, 3))
    plt.bar([1, 2, 3], [4, 5, 6], label="Chart 2")
    plt.title("Sample Chart 2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)  # Rewind the buffer
    return buffer

# PDF Generation Function
def generate_pdf_with_charts(output_file):
    # Page settings
    pdf = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    margin = 50  # Margin size

    # Add a title to the PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(margin, height - margin, "Charts Report")

    # Space for charts
    current_y = height - 2 * margin  # Start below the title
    chart_height = 200  # Fixed height for each chart

    # Generate and add the first chart
    chart_1_buffer = generate_chart_1()
    chart_1_image = ImageReader(chart_1_buffer)
    pdf.drawImage(chart_1_image, margin, current_y - chart_height, width=width - 2 * margin, height=chart_height, preserveAspectRatio=True)
    current_y -= (chart_height + margin)  # Update Y position

    # Generate and add the second chart
    chart_2_buffer = generate_chart_2()
    chart_2_image = ImageReader(chart_2_buffer)
    pdf.drawImage(chart_2_image, margin, current_y - chart_height, width=width - 2 * margin, height=chart_height, preserveAspectRatio=True)
    current_y -= (chart_height + margin)  # Update Y position

    # Finalize the PDF
    pdf.save()

# Generate the PDF
output_file = "charts_report.pdf"
generate_pdf_with_charts(output_file)