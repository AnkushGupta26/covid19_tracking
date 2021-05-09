from django.shortcuts import render
import pandas as pd
#selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
# Create your views here.
def index(request):
    s_data = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
    s_data = s_data.loc[:, ['State','Confirmed', 'Recovered', 'Deaths', 'Active','State_code', 'Last_Updated_Time']].set_index('State')
    v_data = pd.read_csv('http://api.covid19india.org/csv/latest/vaccine_doses_statewise.csv')
    v_data = v_data.iloc[:, [0,-1]].set_index('State')
    v_data = v_data.rename(columns={v_data.columns[0]: 'vaccinated'})
    states = pd.concat([s_data, v_data], axis=1, join="inner").reset_index()
    states = states.to_dict('records')
    return render(request, 'covid/home.html', {'states':states})

def states(request, state_code):
    #graph
    state_daily = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
    confirmed = state_daily.loc[state_daily['Status']=="Confirmed",['Date',state_code]].rename(columns = {state_code: "Confirmed"})
    recovered = state_daily.loc[state_daily['Status']=="Recovered",['Date',state_code]].rename(columns = {state_code: "Recovered"})
    deceased = state_daily.loc[state_daily['Status']=="Deceased",['Date',state_code]].rename(columns = {state_code: "Deceased"})
    cr = pd.merge(confirmed, recovered, on="Date",how="inner")
    crd = pd.merge(cr, deceased, on="Date",how="inner")
    crd = crd.set_index('Date')
    crd = crd.tail(90)
    plot = crd.plot(figsize=(10, 6), linewidth=2, fontsize=12,color = ['steelBlue','Green','Red','Orange'])
    fig = plot.get_figure()
    fig.savefig("covid/static/figure.png")
    
    #map
    url = "https://www.covid19india.org/state/" + state_code
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    time.sleep(5)
    map_div = driver.find_element(By.ID,"chart")
    html_code = map_div.get_attribute('outerHTML')
    driver.quit()
    
    #data
    crd = crd.reset_index()
    state = crd.tail(1)
    state = state.to_dict('records')[0]
    
    #state name
    s_name = pd.read_csv('state_code.csv')
    s_name = s_name.loc[s_name['State_code']==state_code, 'State']
    s_name = s_name.to_dict()
    s_name = s_name.values()
    for s_n in s_name:
        s_name = s_n
    
    return render(request, 'covid/state.html', {'map':html_code, 'state':state, 's_name':s_name})