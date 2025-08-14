import pypdf 
import os 

# read the pdf file
pdf_path = "data/Backlog-DS-Giam_sat_dich_vu.xlsx - Trao đổi FO IP.pdf"
pdf_reader = pypdf.PdfReader(pdf_path)
# extract text from each page
text = ""
for page in pdf_reader.pages:
    text += page.extract_text() + "\n"

# save to a txt file 
output = "data/backlog.txt"
with open(output, "w", encoding="utf-8") as f:
    f.write(text)