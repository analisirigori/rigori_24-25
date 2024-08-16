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

df = pd.read_excel('/Users/reus3111/Clip_Pianese/sito_web/coppa/squadre/pontedera/ragatzu/rigori_ragatzu.xlsx')
balls_data = df.to_dict(orient='records')



balls_html = ""
list_html = ""
grafici_html = ""
sinistra = 0
sinistra_gol = 0
destra = 0
destra_gol = 0
for ball in balls_data:
    i+=1
    if ball['Left']<=15:
        sinistra+=1
        if ball['Esito']==1:
            sinistra_gol += 1
    else:
        destra += 1
        if ball['Esito']==1:
            destra_gol += 1
            
    if ball['Esito']==1:
        balls_html += f"""
        <a href="{ball['Link']}" target="_blank" class="ball-link{i}">
            <div class="ball" style="position: absolute; top: {ball['Top']/10*100}%; left: {ball['Left']/30*100}%;">
                <img src="../../../../images/football.png" alt="Football">
                <span class="ball-number" style="color: black;">{i}</span>
            </div>
        </a>
        """
        list_html+=f"""
        <div class="relazione" style="flex-wrap: wrap;">
            {i}) Partita: {ball['Partita']}, rigore calciato al minuto: {ball['Minuto']} e trasformato, il risultato della partita al momento del tiro era: {ball['Risultato']}. <a href="{ball['Link']}" target="_blank" class="ball-link{i}" style="text-decoration: none;">Video</a>
        </div>
        """
    else:
        balls_html += f"""
        <a href="{ball['Link']}" target="_blank" class="ball-link{i}">
            <div class="ball" style="position: absolute; top: {ball['Top']/10*100}%; left: {ball['Left']/30*100}%;">
                <img src="../../../../images/missed.png" alt="Football">
                <span class="ball-number" style="color: black;">{i}</span>
            </div>
        </a>
        """
        list_html+=f"""
        <div class="relazione" style="flex-wrap: wrap;">
            {i}) Partita: {ball['Partita']}, rigore calciato al minuto: {ball['Minuto']} e sbagliato, il risultato della partita al momento del tiro era: {ball['Risultato']}. <a href="{ball['Link']}" target="_blank" class="ball-link{i}" style="text-decoration: none;">Video</a>
        </div>
        """

grafici_html = f"""
<div class="grafici-container" style="display: flex; justify-content: space-around; margin-top: 50px; margin-bottom: 100px">
    <div>
    <h3> Rigori Calciati </h3>
    <canvas id=graficoTotale"></canvas>
    </div>
</div>
<div class="grafici-container" style="display: flex; justify-content: space-around; margin-top: 50px; margin-bottom: 100px">
    <div>
        <h3>Rigori a Sinistra</h3>
        <canvas id="graficoSinistra"></canvas>
    </div>
    <div>
        <h3>Rigori a Destra</h3>
        <canvas id="graficoDestra"></canvas>
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    var ctxTotal = document.getElementById('graficoTotale').getContext('2d');
    var graficoTotal = new Chart(ctxTotal, {{
        type: 'pie',
        data: {{
            labels: ['Sinistra', 'Destra'],
            datasets: [{{
                label: 'Rigori Calciati',
                data: [{sinistra}, {destra}],
                backgroundColor: ['#4CAF50', '##0000FF'],
                hoverOffset: 4
            }}]
        }},
        options: {{
            responsive: true,
            plugins: {{
                legend: {{
                    position: 'top',
                }},
                tooltip: {{
                    callbacks: {{
                        label: function(tooltipItem) {{
                            var label = tooltipItem.label || '';
                            var value = tooltipItem.raw || 0;
                            var total = {sinistra+destra};
                            var percent = Math.round((value / total) * 100);
                            return label + ': ' + value + ' (' + percent + '%)';
                        }}
                    }}
                }}
            }}
        }}
    }});
    var ctxSinistra = document.getElementById('graficoSinistra').getContext('2d');
    var graficoSinistra = new Chart(ctxSinistra, {{
        type: 'pie',
        data: {{
            labels: ['Gol', 'Sbagliati'],
            datasets: [{{
                label: 'Rigori a Sinistra',
                data: [{sinistra_gol}, {sinistra - sinistra_gol}],
                backgroundColor: ['#4CAF50', '#F44336'],
                hoverOffset: 4
            }}]
        }},
        options: {{
            responsive: true,
            plugins: {{
                legend: {{
                    position: 'top',
                }},
                tooltip: {{
                    callbacks: {{
                        label: function(tooltipItem) {{
                            var label = tooltipItem.label || '';
                            var value = tooltipItem.raw || 0;
                            var total = {sinistra};
                            var percent = Math.round((value / total) * 100);
                            return label + ': ' + value + ' (' + percent + '%)';
                        }}
                    }}
                }}
            }}
        }}
    }});

    var ctxDestra = document.getElementById('graficoDestra').getContext('2d');
    var graficoDestra = new Chart(ctxDestra, {{
        type: 'pie',
        data: {{
            labels: ['Gol', 'Sbagliati'],
            datasets: [{{
                label: 'Rigori a Destra',
                data: [{destra_gol}, {destra - destra_gol}],
                backgroundColor: ['#4CAF50', '#F44336'],
                hoverOffset: 4
            }}]
        }},
        options: {{
            responsive: true,
            plugins: {{
                legend: {{
                    position: 'top',
                }},
                tooltip: {{
                    callbacks: {{
                        label: function(tooltipItem) {{
                            var label = tooltipItem.label || '';
                            var value = tooltipItem.raw || 0;
                            var total = {destra};
                            var percent = Math.round((value / total) * 100);
                            return label + ': ' + value + ' (' + percent + '%)';
                        }}
                    }}
                }}
            }}
        }}
    }});
</script>
"""
    

with open("coppa/squadre/pontedera/ragatzu/ragatzu.html", "r") as file:
    html_content = file.read()

# Trova il punto di inserimento
insert_point = html_content.find('<div id="balls-container" class="balls-container">') + len('<div id="balls-container" class="balls-container">')

# Inserisci il codice HTML generato
new_html_content = html_content[:insert_point] + balls_html + html_content[insert_point:]

# Trova il punto di inserimento per il testo
insert_point_text = new_html_content.find('<div class="list_of_penalties">') + len('<div class="list_of_penalties">')

# Inserisci il contenuto del file di testo
new_html_content = new_html_content[:insert_point_text] + list_html + new_html_content[insert_point_text:]

insert_point_grafici = new_html_content.find('<div class="grafici">') + len('<div class="grafici">')

# Inserisci i grafici in coda alla lista
new_html_content = new_html_content[:insert_point_grafici] + grafici_html + new_html_content[insert_point_grafici:]

# Scrivi il nuovo contenuto HTML in un file
with open("coppa/squadre/pontedera/ragatzu/ragatzu.html", "w") as file:
    file.write(new_html_content)