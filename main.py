from translater import flores_codes
from pdfParser import extractRawText
from gptCleaner import getCleanText
from htmlTranslater import translateHTML
import weasyprint

tgt_lang = "hin_Deva"
start = 103
end = 108

for num in range(start,end+1):
    inp = f"/mnt/c/Users/Samik Goyal/surveyLegalTranslation/English/{num}.pdf"
    out = f"/mnt/c/Users/Samik Goyal/surveyLegalTranslation/Mine/{num}.pdf"
    with open("logs.txt",'a') as f:
        f.write(f"Processing: {num}.pdf\n")
    if tgt_lang not in flores_codes:
        raise "Language code not supported"

    rawText = extractRawText(inp)
    print("Raw text extracted from pdf:")
    print(rawText)
    print("----------------------------")

    cleanText = getCleanText(rawText).strip()
    if not cleanText.startswith("```html") or not cleanText.endswith("```"):
        raise "Invalid output by GPT"
    cleanText = cleanText[7:-3]
    print("Clean text generated by GPT:")
    print(cleanText)
    print("----------------------------")

    # with open("output_en.html", "w") as f:
    #     f.write(cleanText)
    # print("Source HTML generated successfully")

    translatedText = translateHTML(cleanText, tgt_lang)
    print("Translated text:")
    print(translatedText)
    print("----------------------------")

    # with open("output.html", "w") as f:
    #     f.write(translatedText)
    # print("HTML generated successfully")

    weasyprint.HTML(string=translatedText).write_pdf(out)
    print("PDF generated successfully")