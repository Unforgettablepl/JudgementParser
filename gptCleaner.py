from openai import OpenAI
import tiktoken

client = OpenAI(api_key="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")
enc = tiktoken.encoding_for_model("gpt-4o")
THRESHOLD = 10000

sysInstructions = """
### Task Overview

Convert **raw, unformatted legal judgment text**, including any tables, into a **structured, grammatically correct HTML document**. Maintain the original content's integrity while organizing it visually using appropriate HTML tags. Expand abbreviations and short forms where appropriate. **Do not summarize, shorten, omit, or add any paragraphs, sentences, or information that is not present in the original text**.

### Detailed Instructions

1. **Clean Up Unnecessary Symbols**

   - **Remove Unnecessary Ellipses**: Eliminate random ellipses (".......") that do not serve as proper punctuation.
   - **Remove Excessive Symbols**: Delete any excessive use of symbols, such as "……………………", from the content entirely.

2. **Correct Grammar and Expand Short Forms**

   - **Correct Grammar**: Fix any grammatical errors without changing the original meaning or intent of the content.
   - **Expand Short Forms**: Explicitly expand abbreviations and short forms where appropriate, such as:
     - "v." to "versus"
     - "anr." to "another"
     - "etc." to "etcetera"
   - **Do Not Expand Explicit Short Forms**: Do not expand short forms that are explicitly marked as not to be expanded (e.g., "short form argp").
   - **Capitalization**:
     - If a short form is expanded, do not capitalize all letters.
     - If a short form is not expanded, capitalize all letters (e.g., "CRPC").

3. **Maintain Numbering**

   - **Numbered Lists**: Ensure that numbering remains in a separate HTML tag (e.g., `<span class="number">`).
   - **Text Wrapping**: Wrap the associated text in a `<span class="text">` tag.
   - **Spacing**: Add spacing after the number tags by including it directly within the number tag. Do not use a spacer tag for this purpose.

4. **Add Spacer Tags for Gaps**

   - **Spacer Tags**: Use `<span class="text non-text"> </span>` to represent intentional spaces between items instead of using plain spaces within the text.

5. **HTML Structuring**

   - **Headings**: Convert key sections, such as court titles (e.g., "IN THE SUPREME COURT OF INDIA"), into headings using the `<h3>` tag. **All headings should use the `<h3>` tag; do not use `<h1>` or `<h2>`.** Center-align headings where appropriate.
   - **Paragraphs**: Use `<p class="text">` for paragraphs and justify them using CSS (`text-align: justify`).
   - **Text Class**: Wrap all textual content in a `text` class for post-processing. **Do not attach any CSS properties to the `text` class**.
   - **Font Specification**: Use Google Noto Sans as the primary font by including the link to Google Fonts in the `<head>`. Apply the font to all textual content via CSS, but do not style the `text` class directly.

6. **Handle Tables**

   - **Table Detection**: Identify any tabular data or sections formatted as tables within the text.
   - **Table Structure**: Use appropriate HTML table tags to represent the table data:
     - Enclose the entire table in `<table>` tags.
     - Use `<thead>` for the table header, if applicable.
     - Use `<tbody>` for the table body.
     - Use `<tr>` for each table row.
     - Use `<th>` for header cells and `<td>` for standard cells.
   - **Text Wrapping in Tables**: Wrap all textual content within table cells (`<th>` and `<td>`) in a `<span class="text">` tag.
   - **Table Styling**: Apply minimal styling to ensure readability, such as borders or padding, using CSS in the `<style>` section. Do not attach styles directly to the `text` class.
   - **Accessibility**: Include appropriate attributes (e.g., `scope`, `colspan`, `rowspan`) to enhance table accessibility.

7. **Do Not Summarize, Omit, or Add Content**

   - **Full Inclusion**: Include all paragraphs, sentences, and sections from the original text. **Do not summarize, shorten, omit, or add any part of the content that is not present in the original text**.

8. **Output as Valid HTML**

   - **HTML5 Document**: The final output must be a valid HTML5 document.
   - **Head Section**: Include a `<head>` section with metadata and a link to Google Fonts for Noto Sans.
   - **CSS Styling**: Include appropriate CSS styling within `<style>` tags.
   - **Tag Closure**: Ensure all HTML tags are properly closed.
   - **Tag Nesting**: Use correct nesting for tags to maintain structural integrity and accessibility.

### Workflow Steps

1. **Text Parsing**: Break down the raw text into key sections like titles, parties involved, tables, and the judgment body. Identify and handle repeated patterns such as dates and case numbers.

2. **Cleaning Symbols**: Remove unnecessary ellipses and excessive symbols from the content.

3. **Grammar and Short Forms**: Correct grammatical mistakes and expand abbreviations as per the instructions.

4. **Numbering**: Maintain numbering in lists, separating numbers into their own tags.

5. **Handle Tables**: Identify and properly structure any tables using HTML table tags, wrapping textual content in a `text` class.

6. **Spacer Tags**: Use `<span class="text non-text"> </span>` to represent intentional spaces.

7. **Ensure Full Content Inclusion**: Include every paragraph and section from the input text without summarizing or omitting any parts.

8. **HTML Transformation**

   - Structure the content into HTML using appropriate tags and classes.
   - **Use `<h3>` for all headings** and do not use `<h1>` or `<h2>`.

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

The following is the table of contents:

Sl. No. Section Page No.
1 Introduction 1th page
2 Background 2th page
3 Arguments 3th page
4 Conclusion 4th page

This appeal raises important questions about the application of criminal law.

………………………………….J.
[M.R. SHAH]
………………………………….J.
[C.T. RAVIKUMAR]
```

### Output Sample

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Judgment Document</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans', sans-serif; }
        .center-align { text-align: center; }
        p { text-align: justify; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #000; padding: 8px; text-align: left; }
        .number { font-weight: bold; }
    </style>
</head>
<body>
    <h3 class="text center-align">In the Supreme Court of India</h3>
    <h3 class="text center-align">Criminal Appellate Jurisdiction</h3>
    <h3 class="text center-align">Criminal Appeal No. ________ of 2024</h3>
    <p class="text center-align">[Arising out of Special Leave Petition (Criminal) No.4353 of 2018]</p>
    <h3 class="text center-align"><strong>K. Bharthi Devi and Another</strong><span class="text non-text">      </span>Appellant(s)</h3>
    <h3 class="text center-align">Versus</h3>
    <h3 class="text center-align"><strong>State of Telangana and Another</strong><span class="text non-text">     </span>Respondent(s)</h3>
    <h3 class="text center-align">Judgment</h3>
    <h3 class="text center-align">B.R. Gavai, Justice</h3>
    <p><span class="number">1. </span><span class="text">Leave granted.</span></p>
    <p class="text">The following is the table of contents:</p>
    <table>
        <thead>
            <tr>
                <th><span class="text">Serial Number</span></th>
                <th><span class="text">Section</span></th>
                <th><span class="text">Page Number</span></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="text">1</span></td>
                <td><span class="text">Introduction</span></td>
                <td><span class="text">1st page</span></td>
            </tr>
            <tr>
                <td><span class="text">2</span></td>
                <td><span class="text">Background</span></td>
                <td><span class="text">2nd page</span></td>
            </tr>
            <tr>
                <td><span class="text">3</span></td>
                <td><span class="text">Arguments</span></td>
                <td><span class="text">3rd page</span></td>
            </tr>
            <tr>
                <td><span class="text">4</span></td>
                <td><span class="text">Conclusion</span></td>
                <td><span class="text">4th page</span></td>
            </tr>
        </tbody>
    </table>
    <p class="text">This appeal raises important questions about the application of criminal law.</p>
    <p class="text center-align">Justice M.R. Shah</p>
    <p class="text center-align">Justice C.T. Ravikumar</p>
</body>
</html>
```

### Additional Notes

- **Heading Tags**: **Use `<h3>` for all headings**. Do not use `<h1>` or `<h2>`.
- **Non-Textual Elements**: Handle sections with non-textual elements (e.g., tables, figures, legal citations) using suitable HTML tags like `<table>` or `<blockquote>`.
- **Consistency**: Ensure consistency in formatting dates, case numbers, and party names.
- **Accessibility**: Enhance accessibility by using semantic HTML and appropriate attributes.
- **Do Not Summarize or Omit Content**: Include all content from the input text in the output. Do not summarize, shorten, or omit any paragraphs or sections.
- **Error Handling**: Gracefully handle incomplete or irregular input to maintain structural consistency.
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