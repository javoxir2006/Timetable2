import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timezone, timedelta



def show_svg():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    
    service = Service(executable_path="/usr/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://iut.edupage.org/timetable/")

    wait = WebDriverWait(driver, 15)
    element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span[title='Classes']"))
    )

    element.click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dropDownPanel")))

    full = driver.find_element(By.CLASS_NAME, "dropDownPanel")
    lists = full.find_elements(By.CSS_SELECTOR, "li")
    lists[23].click()
    time.sleep(5)

    print("5 seconds")
    html_source = driver.page_source

    driver.quit()

    soup = bs(html_source, 'lxml')

    svg_tag = soup.find('svg')
    if svg_tag:
        svg_tag['height'] = '600'
        svg_tag['width'] = '900'

        g_tag = svg_tag.find('g')
        if g_tag:
            g_tag['transform'] = 'scale(0.3)'

        svg_str = str(svg_tag)
    else:
        svg_str = ""
   
    svg_str = svg_str.replace(
        'style="position: absolute; left: 0px; top: 0px; direction: ltr; stroke: rgb(0, 0, 0); stroke-width: 0; fill: rgb(0, 0, 0);"',
        'style="position: relative; direction: ltr; stroke: rgb(0, 0, 0); stroke-width: 0; fill: rgb(0, 0, 0);"'
    )

    svg_str = svg_str.replace('height="509.0909090909091"', 'height="600"')
    svg_str = svg_str.replace('width="720"', 'width="900"')
    svg_str = svg_str.replace('transform="scale(0.24242424242424243)"', 'transform="scale(0.3)"')

    html_content = f"""
    <!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Timetable</title>
    <style>
      body{{
          margin: 0;
          padding: 0;
          width: 100vw;
          box-sizing: border-box;
      }}

      .svg-container {{
          display: flex;
          align-items: center;
          flex-direction: column;
          gap: 8px;
          width: 100%;
          height: 100vh;
        }}

        .last-updated {{
            text-align: center;
            color: #666;
            margin-top: 10px;
            font-size: 20px;
        }}
    </style>
  </head>

  <body>
    <div class="svg-container">
      { svg_str }
<div class="last-updated">Last updated: {datetime.now(timezone(timedelta(hours=5))).strftime("%H:%M / %Y-%m-%d")}</div>
    </div>
  </body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        

if __name__ == "__main__":
    show_svg()



