from translater import translateParagraph,flores_codes
from pdfParser import extractRawText
from gptCleaner import getCleanText
import os

inp = input("Enter the path to the pdf file: ")
rawText = extractRawText(inp)
cleanText = getCleanText(rawText)
translatedText = translateParagraph(cleanText, "hin_Deva")
print(translatedText)