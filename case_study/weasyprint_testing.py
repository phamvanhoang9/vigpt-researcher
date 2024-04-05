
from weasyprint import HTML

# HTML content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Sample PDF</title>
</head>
<body>
    <h1>Hello, WeasyPrint!</h1>
    <p>I solved your problem, you took me over 3 hours. Unfortunately, I didn't give up :))</p>
</body>
</html>
"""

# Create a PDF
pdf_file = "sample.pdf"
HTML(string=html_content).write_pdf(pdf_file)

print(f"PDF saved as: {pdf_file}")