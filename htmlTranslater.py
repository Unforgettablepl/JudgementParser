from translater import translateParagraph
from bs4 import BeautifulSoup, Comment

def translateHTML(html_text, tgt_lang):
    soup = BeautifulSoup(html_text, 'html.parser')
    for element in soup.find_all(string=True):
        if (element.parent.name not in ['script', 'style']
                and not isinstance(element, Comment)):
            classes = element.parent.get('class', [])
            if 'text' in classes:
                originalText = element.strip()
                if originalText:
                    translatedText = translateParagraph(originalText, tgt_lang)
                    element.replace_with(translatedText)
    return str(soup)
