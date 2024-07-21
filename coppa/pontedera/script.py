#In questo script genero il documento interattivo, devo recuperare dal file excel il link
#al video e la posizione in cui inserire il pallone con il numero e cliccabile col link
#allegato
from typing import TypedDict, List
import pandas as pd
class Ball(TypedDict):
    Link: str
    Top: int
    Left: int
i = 0

df = pd.read_excel('/Users/reus3111/Clip_Pianese/sito_web/coppa/pontedera/Rigori_Pontedera.xlsx')
balls_data = df.to_dict(orient='records')



balls_html = ""
for ball in balls_data:
    i+=1
    balls_html += f"""
    <a href="{ball['Link']}" class="ball-link{i}">
        <div class="ball" style="position: absolute; top: {ball['Top']}px; left: {ball['Left']}px;">
            <img src="../../images/football.png" alt="Football">
            <span class="ball-number">{i}</span>
        </div>
    </a>
    """

with open("sito_web/coppa/pontedera/pontedera.html", "r") as file:
    html_content = file.read()

with open('sito_web/coppa/pontedera/relazione.txt', 'r') as file:
    text_content = file.read()
# Trova il punto di inserimento
insert_point = html_content.find('<div id="balls-container" class="balls-container">') + len('<div id="balls-container" class="balls-container">')

# Inserisci il codice HTML generato
new_html_content = html_content[:insert_point] + balls_html + html_content[insert_point:]

# Trova il punto di inserimento per il testo
insert_point_text = new_html_content.find('<div class="relazione">') + len('<div class="relazione">')

# Inserisci il contenuto del file di testo
new_html_content = new_html_content[:insert_point_text] + "<p>" + text_content + "</p>" + new_html_content[insert_point_text:]

# Scrivi il nuovo contenuto HTML in un file
with open("sito_web/coppa/pontedera/pontedera.html", "w") as file:
    file.write(new_html_content)