from typing import TypedDict, List
import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader

class Ball(TypedDict):
    Link: str
    Top: int
    Left: int

script_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = script_dir

# Se il template è in una sottocartella 'templates' dello script
# template_dir = os.path.join(script_dir, 'templates')

# Inizializza l'ambiente Jinja2 con il percorso corretto
env = Environment(loader=FileSystemLoader(template_dir))

# Carica il template
template = env.get_template('template.html')

template_squadra = env.get_template('template_squadra.html')

squadra_df = pd.read_csv('/Users/reus3111/Clip_Pianese/sito_web/campionato/squadre/spal/squadra.csv')
for _, row in squadra_df.iterrows():
    nome_squadra = row['squadra']
    nome_squadra_completo = row['nome_squadra']

    # Filtra i giocatori della squadra corrente
    #giocatori_squadra = [player for player in players_data if nome_squadra in player['link']]

    # Renderizza il template della squadra con i dati dei giocatori
    output_squadra = template_squadra.render(
        nome_squadra_completo=nome_squadra_completo,
        nome_squadra=nome_squadra,
        #players=giocatori_squadra
    )

    # Salvare l'output HTML per la squadra
    nome_file_squadra_html = f'./{nome_squadra}.html'
    with open(nome_file_squadra_html, 'w', encoding='utf-8') as f:
        f.write(output_squadra)

    print(f'Pagina HTML generata per la squadra {nome_squadra_completo}: {nome_file_squadra_html}')

# Leggere la lista dei giocatori
giocatori_df = pd.read_csv('/Users/reus3111/Clip_Pianese/sito_web/campionato/squadre/spal/giocatori.csv')
players_html = ""
# Per ogni giocatore, generare la pagina HTML
for _, row in giocatori_df.iterrows():
    giocatore = row['nome_giocatore']
    cognome = row['cognome']
    numero = row['numero']
    nome_completo = row['nome'] + " " + row['cognome']
    nome_squadra = row['squadra']  # Aggiungi un attributo per il nome della squadra
    piede = row['piede']
    
    players_html = players_html + f'\n\t\t\t<a href="{giocatore}/{giocatore}.html" class="player-button">{cognome} {numero}</a>'
    
    
    
    
    # Leggere il file Excel del giocatore
    nome_file_excel = f'{giocatore}.xlsx'
    try:
        df = pd.read_excel(f'/Users/reus3111/Clip_Pianese/sito_web/campionato/squadre/spal/{giocatore}/{nome_file_excel}')
        # Convertire i dati in un dizionario (ad esempio, prima riga come dati)
        dati_giocatore = df.iloc[0].to_dict()
    except FileNotFoundError:
        print(f'File Excel per {giocatore} non trovato.')
        continue
    nome_squadra = dati_giocatore['Squadra'];
    # Renderizzare il template con i dati del giocatore
    output = template.render(nome_giocatore=giocatore, nome_completo=nome_completo,nome_squadra=dati_giocatore['Squadra'], piede_giocatore=dati_giocatore['Piede'])
    
    # Salvare l'output HTML
    nome_file_html = f'/Users/reus3111/Clip_Pianese/sito_web/campionato/squadre/{nome_squadra}/{giocatore}/{giocatore.replace(" ", "_")}.html'
    with open(nome_file_html, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f'Pagina HTML generata per {giocatore}: {nome_file_html}')
    i = 0

    df = pd.read_excel(f'/Users/reus3111/Clip_Pianese/sito_web/campionato/squadre/{nome_squadra}/{giocatore}/{giocatore}.xlsx')
    balls_data = df.to_dict(orient='records')



    balls_html = ""
    list_html = """
    <table class="penalty-table" style="width: 100%; border-collapse: collapse; margin-top: 20px;">
        <thead>
            <tr>
                <th style="border: 1px solid #ddd; padding: 8px;">#</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Partita</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Minuto</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Esito</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Risultato</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Video</th>
            </tr>
        </thead>
        <tbody>
    """
    grafici_html = ""
    chiudere = 0
    chiudere_gol = 0
    aprire = 0
    aprire_gol = 0
    for ball in balls_data:
        i+=1
        if ball['Piede']=="Destro":
            if ball['Left']<=15:
                chiudere+=1
                if ball['Esito']==1:
                    chiudere_gol += 1
            else:
                aprire += 1
                if ball['Esito']==1:
                    aprire_gol += 1
        else:
            if ball['Left']<=15:
                aprire+=1
                if ball['Esito']==1:
                    aprire_gol += 1
            else:
                chiudere += 1
                if ball['Esito']==1:
                    chiudere_gol += 1
        
                
        if ball['Esito']==1:
            balls_html += f"""
            <a href="{ball['Link']}" target="_blank" class="ball-link{i}">
                <div class="ball" style="position: absolute; top: {ball['Top']/10*100}%; left: {ball['Left']/30*100}%;">
                    <img src="../../../../images/football.png" alt="Football">
                    <span class="ball-number" style="color: black;">{i}</span>
                </div>
            </a>
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
            
    for i, ball in enumerate(balls_data, start=1):
        esito_color = '#4CAF50' if ball['Esito'] == 1 else '#F44336'
        esito_text = 'Trasformato' if ball['Esito'] == 1 else 'Sbagliato'

        list_html += f"""
        <tr>
            <td data-label="#" style="border: 1px solid #ddd; padding: 8px;">{i}</td>
            <td data-label="Partita" style="border: 1px solid #ddd; padding: 8px;">{ball['Partita']}</td>
            <td data-label="Minuto" style="border: 1px solid #ddd; padding: 8px;">{ball['Minuto']}</td>
            <td data-label="Esito" style="border: 1px solid #ddd; padding: 8px; background-color: {esito_color}; color: #fff;">{esito_text}</td>
            <td data-label="Risultato" style="border: 1px solid #ddd; padding: 8px;">{ball['Risultato']}</td>
            <td data-label="Video" style="border: 1px solid #ddd; padding: 8px;">
                <a href="{ball['Link']}" target="_blank" style="text-decoration: none; color: #000;">link</a>
            </td>
        </tr>
        """

    list_html += "</tbody></table>"
    grafici_aprire_html = ""
    grafici_chiudere_html= ""
    if aprire != 0:
        grafici_aprire_html = f"""
    
            var ctxAprire = document.getElementById('graficoAprire').getContext('2d');
            var graficoAprire = new Chart(ctxAprire, {{
                type: 'pie',
                data: {{
                    labels: ['Gol', 'Sbagliati'],
                    datasets: [{{
                        label: 'Rigori ad Aprire',
                        data: [{aprire_gol}, {aprire - aprire_gol}],
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
                            enabled : false
                        }},
                        datalabels: {{
                            color: '#fff',
                            font: {{
                                size: 18,  // Imposta la dimensione del font delle etichette
                                weight: 'bold' // Puoi anche aggiungere altre proprietà come il peso del font
                            }},
                            formatter: function(value, context) {{
                                var total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                                var percent = Math.round((value / total) * 100);
                                return value + ' (' + percent + '%)';
                            }}
                        }}
                    }}
                }},
                plugins: [ChartDataLabels]
            }});
        """
    if chiudere != 0:
        grafici_chiudere_html = f"""
        var ctxChiudere = document.getElementById('graficoChiudere').getContext('2d');
        var graficoChiudere = new Chart(ctxChiudere, {{
            type: 'pie',
            data: {{
                labels: ['Gol', 'Sbagliati'],
                datasets: [{{
                    label: 'Rigori a Chiudere',
                    data: [{chiudere_gol}, {chiudere - chiudere_gol}],
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
                        enabled : false
                    }},
                    datalabels: {{
                        color: '#fff',
                        font: {{
                            size: 18,  // Imposta la dimensione del font delle etichette
                            weight: 'bold' // Puoi anche aggiungere altre proprietà come il peso del font
                        }},
                        formatter: function(value, context) {{
                            var total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                            var percent = Math.round((value / total) * 100);
                            return value + ' (' + percent + '%)';
                        }}
                    }}
                }}
            }},
            plugins: [ChartDataLabels]
        }});
        """
        
    logica_html = ""
    if aprire != 0 and chiudere != 0:
        logica_html = f"""
        <div class="grafici-container" style="display: flex; justify-content: space-around; margin-top: 50px; margin-bottom: 100px">
            <div>
            <h3> Rigori Calciati </h3>
            <canvas id="graficoTotale"></canvas>
            </div>
        </div>
        <div class="grafici-container" style="display: flex; justify-content: space-around; margin-top: 50px; margin-bottom: 100px">
            <div>
                <h3>Rigori ad Aprire</h3>
                <canvas id="graficoAprire"></canvas>
            </div>
            <div>
                <h3>Rigori a Chiudere</h3>
                <canvas id="graficoChiudere"></canvas>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
        """
    elif aprire ==0 and chiudere!=0:
        logica_html = f"""
        <div class="grafici-container" style="display: flex; justify-content: space-around; margin-top: 50px; margin-bottom: 100px">
            <div>
            <h3> Rigori Calciati </h3>
            <canvas id="graficoTotale"></canvas>
            </div>
        </div>
        <div class="grafici-container" style="display: flex; justify-content: space-around; margin-top: 50px; margin-bottom: 100px">
            <div>
                <h3>Rigori ad Aprire</h3>
                <p style="margin-top:20px;">Non ci sono rigori ad Aprire</p>
            </div>
            <div>
                <h3>Rigori a Chiudere</h3>
                <canvas id="graficoChiudere"></canvas>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
        """
    elif chiudere==0 and aprire!=0:
        logica_html = f"""
        <div class="grafici-container" style="display: flex; justify-content: space-around; margin-top: 50px; margin-bottom: 100px">
            <div>
            <h3> Rigori Calciati </h3>
            <canvas id="graficoTotale"></canvas>
            </div>
        </div>
        <div class="grafici-container" style="display: flex; justify-content: space-around; margin-top: 50px; margin-bottom: 100px">
            <div>
                <h3>Rigori ad Aprire</h3>
                <canvas id="graficoAprire"></canvas>
            </div>
            <div>
                <h3>Rigori a Chiudere</h3>
                <p style="margin-top:20px;">Non ci sono rigori a chiudere</p>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
        """
        



    grafici_html = logica_html + f"""
        <script>
            var ctxTotal = document.getElementById('graficoTotale').getContext('2d');
            var graficoTotal = new Chart(ctxTotal, {{
                type: 'pie',
                data: {{
                    labels: ['Chiudere', 'Aprire'],
                    datasets: [{{
                        label: 'Rigori Calciati',
                        data: [{chiudere}, {aprire}],
                        backgroundColor: ['#4CAF50', '#0000FF'],
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'top',
                        }},
                        tooltip: {{
                            enabled : false
                        }},
                        datalabels: {{
                            color: '#fff',
                            font: {{
                                size: 18,  // Imposta la dimensione del font delle etichette
                                weight: 'bold' // Puoi anche aggiungere altre proprietà come il peso del font
                            }},
                            formatter: function(value, context) {{
                                var total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                                var percent = Math.round((value / total) * 100);
                                return value + ' (' + percent + '%)';
                            }}
                        }}
                    }}
                }},
                plugins: [ChartDataLabels]
            }});
        """
    grafici_html+=grafici_aprire_html + grafici_chiudere_html +"</script>" 

    with open(f'./{giocatore}/{giocatore}.html', "r") as file:
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
    with open(f"./{giocatore}/{giocatore}.html", "w") as file:
        file.write(new_html_content)

with open(f'./{nome_squadra}.html',"r") as file:
     html_content = file.read()
insert_point = html_content.find('<div class="players-container">') + len('<div class="players-container">')

new_html_content = html_content[:insert_point] + players_html + html_content[insert_point:]

with open(f'./{nome_squadra}.html',"w") as file:
    file.write(new_html_content)
    