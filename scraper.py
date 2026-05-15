import asyncio
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

URL_BASE = os.getenv(
  "BOOKING_URL",
  "https://www.booking.com/"
)

async def extrair_dados_booking():
    print("Starting...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        print("Accessing Booking...")
        await page.goto(URL_BASE, timeout=60000)
        
        print("Waiting...")
        await page.wait_for_selector('div[data-testid="property-card"]', timeout=15000)
        
        html = await page.content()
        await browser.close()
        
    return html

def parsear_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    hoteis = []
    
    cards = soup.find_all('div', {'data-testid': 'property-card'})
    print(f"Encontrados {len(cards)} hotéis na página.")
    
    for card in cards:
        # Dentro do seu loop for card in cards:
        hoteis.append({
            "Data_Coleta": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Nome": nome,
            "Preco": preco,
            "Nota": card.find('div', {'data-testid': 'review-score-badge'}).text.strip() if card.find('div', {'data-testid': 'review-score-badge'}) else "N/A",
            "Localizacao": card.find('span', {'data-testid': 'address'}).text.strip() if card.find('span', {'data-testid': 'address'}) else "N/A"
        })
        nome_elem = card.find('div', {'data-testid': 'title'})
        nome = nome_elem.text.strip() if nome_elem else "N/A"
        
        preco_elem = card.find('span', {'data-testid': 'price-and-discounted-price'})
        preco = preco_elem.text.strip() if preco_elem else "N/A"
        
        hoteis.append({
            "Data_Coleta": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Nome": nome,
            "Preco": preco
        })
        
    return hoteis

async def main():
    try:
        html = await extrair_dados_booking()
        lista_hoteis = parsear_html(html)
        
        if lista_hoteis:
            df = pd.DataFrame(lista_hoteis)
            df.to_csv("dados_hoteis.csv", index=False, encoding="utf-8-sig")
            print("Dados salvos com sucesso em 'dados_hoteis.csv'!")
        else:
            print("Nothing was found.")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())