from openai import OpenAI
import tiktoken

client = OpenAI(api_key="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")
enc = tiktoken.encoding_for_model("gpt-4o")
THRESHOLD = 10000

sysInstructions = """
### Task Overview

Your task is to convert **raw, unformatted legal judgment text** into **structured, grammatically correct HTML**. The output must maintain the original content's integrity while being visually organized using appropriate HTML tags. Additionally, expand abbreviations and short forms where appropriate.

### Detailed Instructions

1. **Remove Unnecessary Ellipses**: Identify and remove random ellipses (".......") that do not serve as proper punctuation.

2. **Preserve Numbering**: For numbered lists, ensure that numbering remains in a separate HTML tag. Wrap the associated text in a tag with the class `text`. You may add spacing after the number tags, but not after the tags containing the actual text.

3. **Correct Grammar**: Correct any grammatical errors without changing the original meaning or altering the intent of the content.

4. **Expand Short Forms**: Explicitly expand abbreviations and short forms, such as:
   - "v." to "versus"
   - "anr." to "another"
   - "etc." to "etcetera" Be careful not to expand explicitly marked short forms (e.g., "short form argp"). If a short form is expanded, do not capitalize all letters.

5. **Capitalize Short Forms**: If the word is a short form and is not expanded, all the letters in the word should be capitalized. Otherwise, the word should not have all letters uppercase.

6. **Add Spacer Tag for Gaps**: If there is some space to be left between two items, use a separate `<span>` with the class `non-text` to represent the space instead of using plain spaces within the text.

7. **HTML Structuring**: Structure the cleaned text into valid HTML:
   - Convert key sections, such as court titles (e.g., "IN THE SUPREME COURT OF INDIA"), into headings (`<h1>`, `<h2>`, etc.), and center-align them where appropriate. Wrap English text in a `text` class.
   - Use appropriate tags (`<p>`, `<span>`, etc.) for paragraphs, subtitles, lists, and other sections, ensuring all content is wrapped in a `text` class.
   - Justify paragraphs (`<p>` elements) using CSS (`text-align: justify`).

8. **Font Specification**: Use Google Noto Sans as the primary font by including the link to Google Fonts:
   - Apply the font to all textual content, but do not style the `text` class as it will be used for post-processing.
   - **Do not attach any CSS properties to the class `text`**. You may use CSS properties with tags or other custom classes as needed.

### Workflow Steps

1. **Text Parsing**: Break down the raw text into key sections like titles, parties involved, and the judgment body. Identify and handle repeated patterns, such as dates and case numbers.

2. **Remove Excessive Ellipses**: Remove any unnecessary ellipses or replace them with appropriate punctuation where needed.

3. **Maintain Numbering**: Ensure numbered items retain their numbering. Separate numbers into their own tags (e.g., `<span class="number">`), while wrapping the related text in a separate tag (e.g., `<span class="text">`). You may add spacing after the number tags using the spacer tag.

4. **Grammar Correction**: Correct grammatical mistakes to ensure clarity and readability without changing the substance of the content.

5. **Expand Short Forms**: Expand abbreviations such as "v." to "versus" while ensuring explicitly marked short forms remain unchanged. If expanded, do not capitalize all letters.

6. **Capitalize Short Forms**: Ensure that short forms are fully capitalized (e.g., "ANR" should remain uppercase) if they are not expanded, while non-short form words should not be in full uppercase.

7. **Add Spacer Tag**: Use `<span class="text non-text"> </span>` to represent spacing between items instead of using plain spaces within the text. This helps in maintaining consistent formatting.

8. **Transform into HTML**:
   - Use headings (`<h1 class="text">`, `<h2 class="text">`) for court titles and key sections.
   - Wrap paragraphs in `<p class="text">` and justify them with CSS (`text-align: justify`).
   - Center-align titles or headers where appropriate using inline styles or CSS classes (e.g., `.center-align`).
   - For numbered lists, place numbers in one tag and the accompanying text in a separate `<span class="text">` tag.

9. **Output as Valid HTML**: Ensure the output is a well-formed HTML5 document:
   - Properly close all tags.
   - Include a complete `<head>` section for metadata and styling.
   - Use correct nesting for tags to maintain structural integrity and accessibility.

### Output Requirements

- The final output must be a valid HTML document using proper HTML5 syntax.
- Include a `<head>` section with metadata and a link to Google Fonts for Noto Sans.

### Input Sample

**Input**:

```
2024 INSC 750
1   
REPORTABLE     
    
IN THE SUPREME COURT OF INDIA  
CRIMINAL APPELLATE JURISDICTION  
 
CRIMINAL APPEAL NO . ________ OF 2024  
[Arising out of Special Leave Petition (Criminal) No.4353 of 
2018]  
 
  
K. BHARTHI DEVI AND ANOTHER.                         …APPELLANT(S)  
 
VERSUS  
 
 
STATE OF TELANGANA & ANOTHER.        …RESPONDENT(S)  
 
 
 
J U D G M E N T  
 
 
B.R. GAVAI , Justice 
 
1. Leave granted.  
………………………………….J.
[M.R. SHAH]
………………………………….J.
[C.T. RAVIKUMAR]
```

**Output**:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Judgment Document</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans', sans-serif; }
        .center-align { text-align: center; }
        p { text-align: justify; }
    </style>
</head>
<body>
    <h1 class="text center-align">In the Supreme Court of India</h1>
    <h2 class="text center-align">Criminal Appellate Jurisdiction</h2>
    <h3 class="text center-align">Criminal Appeal Number ________ of 2024</h3>
    <p class="text center-align">[Arising out of Special Leave Petition (Criminal) No.4353 of 2018]</p>
    <h3 class="text center-align"><strong>K. Bharthi Devi and Another</strong><span class="text non-text"> </span>Appellant(s)</h3>
    <h3 class="text center-align">Versus</h3>
    <h3 class="text center-align"><strong>State of Telangana and Another</strong><span class="text non-text"> </span>Respondent(s)</h3>
    <h2 class="text center-align">Judgment</h2>
    <h3 class="text center-align">Justice B.R. Gavai</h3>
    <p><span class="number">1.</span><span class="text non-text"> </span><span class="text">Leave granted.</span></p>
    <p class="text center-align">Justice M.R. Shah</p>
    <p class="text center-align">Justice C.T. Ravikumar</p>
</body>
</html>
```

### Additional Notes

- Handle sections with non-textual elements (e.g., tables, figures, legal citations) using suitable tags (`<table>`, `<blockquote>`, etc.).
- Ensure consistency in formatting dates, case numbers, and party names.
- Handle incomplete or irregular input gracefully, ensuring structural consistency.
"""

def getCleanText(rawText):
    tokens = len(enc.encode(rawText))
    if tokens>THRESHOLD:
        print("Input tokens exceeded the limit")
        input("Press Enter to continue anyway")
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sysInstructions},
            {"role": "user", "content": rawText},
        ],
    )
    print("Input Tokens Used:", completion.usage.prompt_tokens)
    print("Output Tokens Used:", completion.usage.completion_tokens)
    return completion.choices[0].message.content