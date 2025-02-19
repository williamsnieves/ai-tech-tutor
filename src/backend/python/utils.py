def format_code_block(code, language="python"):
    return f"```{language}\n{code}\n```"

def markdown_response(response):
    return response.replace("```", "").replace("markdown", "").strip()