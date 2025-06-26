import re
import markdown

def fix_bidi_in_code(html):
    """
    Post-process HTML to properly handle Arabic and mixed-language content inside <code> blocks.
    It wraps Arabic words in <span dir="rtl"> and English text in <span dir="ltr"> while preserving formatting.
    """
    def process_code_block(match):
        code_content = match.group(1)

        def wrap_text(line):
            # This regex detects Arabic characters
            arabic_pattern = re.compile(r'[\u0600-\u06FF]+')
            if arabic_pattern.search(line):
                return f'<span dir="rtl">{line}</span>'
            return f'<span dir="ltr">{line}</span>'

        # Process each line separately
        wrapped_lines = [wrap_text(line) if line.strip() else line for line in code_content.splitlines()]
        fixed_code = "\n".join(wrapped_lines)

        return f"<code>{fixed_code}</code>"

    return re.sub(r'<code>(.*?)</code>', process_code_block, html, flags=re.DOTALL)

def md_to_html(md_text):
    """
    Convert Markdown to HTML with proper handling for Arabic and English text inside code blocks.
    """
    html = markdown.markdown(
        md_text,
        extensions=['fenced_code', 'codehilite'],
        extension_configs={
            'codehilite': {
                'guess_lang': False,
                'noclasses': True
            }
        }
    )

    # Fix Arabic word reversal issue
    html = fix_bidi_in_code(html)
    return html