from django.shortcuts import render
from django import forms
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Form class
class SearchForm(forms.Form):
    search_term = forms.CharField(label='Enter Search Term', max_length=100)

# View function
def search_view(request):
    result_text = ""
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            
            chrome_options = Options()
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--headless')
            df = pd.read_excel('/media/FIRST CATALOGUE NEW.xlsx')
            print(df)
            service = Service('/media/chromedriver.exe')  # Update path if necessary
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(f'https://www.fleetguard.com/s/searchResults?propertyVal={search_term}&hybridSearch=false&language=en_US')
            time.sleep(5)
            html = driver.page_source
            driver.quit()

            soup = BeautifulSoup(html, 'html.parser')
            class_name = 'hoverPartSearchLogin'  # Replace with the actual class name you are looking for
            elements = soup.find_all(class_=class_name)

            unique = {}
            for element in elements: 
                unique[element.get_text().split()[0]] = 1

            df = pd.read_excel('/media/FIRST CATALOGUE NEW.xlsx')
            for element, _ in unique.items():
                if str(element) in df['OEM'].to_list():
                    h = ' EXIST'
                else: 
                    h = ' --- X'
                result_text += f"{element}{h}\n"

            if len(elements) < 1:
                result_text = 'No FleetGuard Equivalent or Number is not correct\n'
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form, 'result_text': result_text})
