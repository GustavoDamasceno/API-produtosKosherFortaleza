import pandas as pd
from flask import Flask
from pyluach import dates, hebrewcal, parshios
from datetime import date

app = Flask(__name__)

# Routes
@app.route('/')
def homepage():
  return 'API rest - produtos kosher em fortaleza'

@app.route('/produtos')
def produtos():
  table = pd.read_csv('kosherProducts.csv')
  jtable = table.to_json(orient = 'index')
  return jtable

@app.route('/date')
def hdate():
  # Identificar ano bissexto para o mês de ADAR
  def hebrew_leap(year):
    if ((((year*7)+1) % 19) < 7):
      return True
    else:
      return False
  
  # Nome do mês judaico incluindo ADAR II
  def hebrew_month(htoday):
    if htoday.month == 1:
      return("Nisan")
    elif htoday.month == 2:
      return("Iyyar")
    elif htoday.month == 3:
      return("Sivan")
    elif htoday.month == 4:
      return("Tammuz")
    elif htoday.month == 5:
      return("Av")
    elif htoday.month == 6:
      return("Elul")
    elif htoday.month == 7:
      return("Tishri")
    elif htoday.month == 8:
      return("Heshvan")
    elif htoday.month == 9:
      return("Kislev")
    elif htoday.month == 10:
      return("Teveth")
    elif htoday == 11:
      return("Shevat")
    elif htoday == 12:
      if htoday.hebrew_leap(htoday.year):
        return("Adar I")
      else:
        return("Adar")
      
    elif htoday == 13:
      return("Adar II")
  
  
  # Nome do mês gregoriano
  def greg_month(mes):
    if mes == 1:
      return 'janeiro'
    elif mes == 2:
      return 'fevereiro'
    elif mes == 3:
      return 'março'
    elif mes == 4:
      return 'abril'
    elif mes == 5:
      return 'maio'
    elif mes == 6:
      return 'junho'
    elif mes == 7:
      return 'julho'
    elif mes == 8:
      return 'agosto'
    elif mes == 9:
      return 'setembro'
    elif mes == 10:
      return 'outubro'
    elif mes == 11:
      return 'novembro'
    elif mes == 12:
      return 'dezembro'
  
      
  
  
  htoday = dates.HebrewDate.today()
  
  date_atual = date.today()
  
  today = dates.GregorianDate(date_atual.year, date_atual.month, date_atual.day)
  
  # Transformar dados em DataFrame com pandas para ficar fácil a conversão para o JSON
  df = pd.DataFrame(
  {"gregorian_date" : [date_atual.day ,greg_month(date_atual.month), date_atual.year],
  "hebrew_date" : [htoday.day, hebrew_month(htoday), htoday.year]},
  index = ['dia', 'mes', 'ano'])

  return df.to_json()

@app.route('/parashat')
def parashat():
  date_atual = date.today()
  
  today = dates.GregorianDate(date_atual.year, date_atual.month, date_atual.day)  

  df = pd.DataFrame(
  {"parashatHashavua" : [parshios.getparsha_string(today), parshios.getparsha_string(today, hebrew=True)]},
  index = ['parashat_br', 'parashat_il'])

  return df.to_json()
  

# Rodar a API
app.run(host='0.0.0.0')

