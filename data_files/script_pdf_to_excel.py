import fitz  # PyMuPDF
import re
import pandas as pd

pdf_path = "Schritte_plus_Neu_1_2_Glossar_Deutsch_Russisch.pdf"  # путь к твоему файлу
doc = fitz.open(pdf_path)

all_data = []

for page in doc:
    blocks = page.get_text("blocks")
    print(blocks)
    for b in blocks:
        text = b[4].strip()
        if text:
            parts = re.split(r"\s{3,}", text)
            if len(parts) == 2:
                german, russian = parts
                all_data.append({
                    "Немецкое слово": german.strip(),
                    "Перевод на русский": russian.strip()
                })

df = pd.DataFrame(all_data)
df.to_excel("all_words.xlsx", index=False)

print(f"Сохранено {len(df)} слов в all_words.xlsx")
