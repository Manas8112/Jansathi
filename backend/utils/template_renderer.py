import os
from jinja2 import Environment, FileSystemLoader
try:
    from weasyprint import HTML
except ImportError:
    HTML = None

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

def render_template(template_name: str, data: dict) -> str:
    """
    Renders a Jinja2 template with the provided data and returns the HTML string.
    """
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(template_name)
    return template.render(**data)

def render_to_pdf(template_name: str, data: dict) -> bytes:
    """
    Renders a Jinja2 template to HTML, then converts it to PDF bytes using WeasyPrint.
    """
    if HTML is None:
        raise RuntimeError("WeasyPrint is not installed or configured correctly.")
        
    html_string = render_template(template_name, data)
    pdf_bytes = HTML(string=html_string).write_pdf()
    return pdf_bytes
