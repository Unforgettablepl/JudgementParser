from translater import translateParagraph
from bs4 import BeautifulSoup, Comment

def translateHTML(html_text, tgt_lang):
    soup = BeautifulSoup(html_text, 'html.parser')
    for element in soup.find_all(string=True):
        if not isinstance(element, Comment):
            skip_element = False
            process_element = False

            for parent in element.parents:
                if parent.name in ['script', 'style']:
                    skip_element = True
                    break
                if 'non-text' in parent.get('class', []) or 'number' in parent.get('class', []):
                    skip_element = True
                    break
                if 'text' in parent.get('class', []):
                    process_element = True

            if skip_element:
                continue

            if process_element:
                originalText = element.strip()
                if originalText:
                    translatedText = translateParagraph(originalText, tgt_lang)
                    element.replace_with(translatedText)

    return str(soup)
