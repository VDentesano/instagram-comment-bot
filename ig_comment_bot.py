"""
Bot de Comentarios para Instagram (Versión Educativa)
----------------------------------------------------
Este script automatiza comentarios en publicaciones de Instagram usando técnicas avanzadas
de navegación humana simulada. Solo para fines educativos.
"""

import os
import time
import random
import requests
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np

# Inicialización de Colorama
init(autoreset=True)

# Configuración de User-Agents
MOBILE_AGENTS = [
    # iOS
    "Mozilla/5.0 (iPhone15,3; U; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    
    # Android
    "Mozilla/5.0 (Linux; Android 14; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.143 Mobile Safari/537.36",
    
    # Samsung
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/120.0.6099.210 Mobile Safari/537.36",
    
    # Xiaomi
    "Mozilla/5.0 (Linux; Android 14; 2203121G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36",
    
    # Huawei
    "Mozilla/5.0 (Linux; Android 12; LIO-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.178 Mobile Safari/537.36",
    
    # Firefox Mobile
    "Mozilla/5.0 (Android 14; Mobile; rv:122.0) Gecko/122.0 Firefox/122.0",
    
    # Opera Mobile
    "Mozilla/5.0 (Linux; Android 13; RMX2202) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.178 Mobile Safari/537.36 OPR/75.3.4011.58674",
    
    # iPad
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    
    # Surface Duo
    "Mozilla/5.0 (Linux; Android 12; Surface Duo) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.178 Mobile Safari/537.36",
    
    # Otros
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; 2109119DG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.178 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; CPH2581) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
]
DESKTOP_AGENTS = [
    # Windows - Chrome
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.204 Safari/537.36",
    
    # Mac - Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    
    # Linux - Firefox
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    
    # ChromeOS
    "Mozilla/5.0 (X11; CrOS x86_64 15633.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.184 Safari/537.36",
    
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.128",
    
    # Brave
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Brave/1.61.114",
    
    # Opera
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/106.0.0.0",
    
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    
    # Safari Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    
    # Legacy Browsers
    "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
    
    # Otros
    "Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.184 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Vivaldi/6.5.3206.63"
]

class HumanizedDelay:
    """
    Genera retardos variables que imitan patrones humanos de navegación
    Utiliza distribución log-normal para tiempos entre acciones
    """
    def __init__(self):
        self.last_action = time.time()
        
    def wait(self):
        delay = np.random.lognormal(mean=0.8, sigma=0.6) * 4 
        time.sleep(delay)
        self.last_action = time.time()
        return delay

class InstagramBot:
    """
    Clase principal del bot de Instagram
    """
    def __init__(self):
        self.session = requests.Session()
        self.driver = self.setup_driver()
        self.delay_manager = HumanizedDelay()
    
    def setup_driver(self):
        """Configura el driver de Chrome con opciones anti-detección"""
        chrome_options = Options()
        
        # Configuración básica
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Configuración de perfil
        profile_path = os.path.join(os.environ.get('APPDATA', ''), 'InstagramBot', 'ChromeProfile')
        chrome_options.add_argument(f"user-data-dir={profile_path}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        self.human_browsing_simulation(driver)
        return driver

    def human_browsing_simulation(self, driver):
        """Simula interacciones humanas aleatorias"""
        # Simula scroll vertical aleatorio
        scroll_script = f"window.scrollBy(0, {random.randint(200, 800)});"
        driver.execute_script(scroll_script)
        time.sleep(random.uniform(0.5, 1.5))
        
        # Simula scroll horizontal ocasional
        if random.random() < 0.2:
            scroll_h_script = f"window.scrollBy({random.randint(-200, 200)}, 0);"
            driver.execute_script(scroll_h_script)
            time.sleep(random.uniform(0.5, 1.5))
        
        # Simula hover sobre enlaces o imágenes
        elements = driver.find_elements(By.XPATH, "//a | //img")
        if elements and random.random() < 0.5:
            element = random.choice(elements)
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                time.sleep(random.uniform(1, 3))
            except Exception:
                pass
        
        # Clic aleatorio en botones
        if random.random() < 0.3:
            try:
                buttons = driver.find_elements(By.TAG_NAME, 'button')
                if buttons:
                    random.choice(buttons).click()
                    time.sleep(random.uniform(1, 3))
            except Exception:
                pass
        
        # Simula movimientos de mouse aleatorios en el cuerpo de la página
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            body = driver.find_element(By.TAG_NAME, 'body')
            actions = ActionChains(driver)
            x_offset = random.randint(0, 300)
            y_offset = random.randint(0, 300)
            actions.move_to_element_with_offset(body, x_offset, y_offset).perform()
            time.sleep(random.uniform(0.5, 1.5))
        except Exception:
            pass

    def authenticate(self):
        try:
            print(f"{Fore.YELLOW}[*] Cargando Instagram...")
            self.driver.get("https://www.instagram.com/")
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/direct/inbox/')]"))
                )
            except Exception:
                print(f"{Fore.YELLOW}[!] Se requiere autenticación manual (15 minutos timeout)")
                WebDriverWait(self.driver, 900).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/direct/inbox/')]"))
                )
            for cookie in self.driver.get_cookies():
                self.session.cookies.set(cookie['name'], cookie['value'])
            self.session.headers.update({
                'User-Agent': self.driver.execute_script("return navigator.userAgent;"),
                'X-Requested-With': 'XMLHttpRequest'
            })
        except Exception as e:
            print(f"{Fore.RED}[!] Error de autenticación: {str(e)}")
            self.safe_shutdown()
            raise

    def get_post_id(self):
        try:
            meta_tags = self.driver.find_elements(By.XPATH, '//meta[@property="al:ios:url"]')
            for tag in meta_tags:
                content = tag.get_attribute('content')
                if 'instagram://media?id=' in content:
                    post_id = content.split('=')[-1].strip('"')
                    if post_id.isdigit():
                        return post_id
            graphql_data = self.driver.execute_script(
                "return window._sharedData?.entry_data?.PostPage?.[0]?.graphql?.shortcode_media?.id || ''"
            )
            if graphql_data and graphql_data.isdigit():
                return graphql_data
            article = self.driver.find_element(By.TAG_NAME, 'article')
            post_id = article.get_attribute('id').split('-')[-1]
            if post_id.isdigit():
                return post_id
            raise ValueError("No se pudo obtener el ID del post")
        except Exception as e:
            print(f"{Fore.RED}[!] Error al obtener el ID del post: {str(e)}")
            return None

    def rotate_user_agent(self):
        mobile = random.choice([True, False])
        return random.choice(MOBILE_AGENTS if mobile else DESKTOP_AGENTS)

    def get_dynamic_headers(self, url):
        return {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': url,
            'X-Instagram-AJAX': str(random.randint(10**9, 10**10)),
            'Accept-Language': f'en-US,en;q=0.{random.randint(5,9)}',
            'User-Agent': self.rotate_user_agent()
        }

    def generate_unique_comment(self, base_msg):
        patterns = [
            f"{base_msg} {random.choice(['💯','🍔','⚡'])}",
            f"{random.choice(['god','dalee','tremendo'])} {base_msg}",
        ]
        return random.choice(patterns)

    def handle_rate_limit(self, response):
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 300))
            print(f"{Fore.RED}[!] Rate limit: Pausa de {retry_after}s")
            time.sleep(retry_after + 30)
            return True
        return False

    def handle_error(self, response):
        if self.handle_rate_limit(response):
            return
        if response.status_code == 403:
            new_csrf = self.get_csrf_from_browser()
            self.session.headers.update({
                'X-CSRFToken': new_csrf,
            })
            print(f"{Fore.YELLOW}[↻] Tokens de seguridad actualizados")
        else:
            print(f"{Fore.RED}[✗] Error {response.status_code}: {response.text[:200]}")

    def get_csrf_from_browser(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                lambda d: d.get_cookie("csrftoken")["value"]
            )
        except Exception:
            cookie_str = self.driver.execute_script("return document.cookie")
            for part in cookie_str.split('; '):
                if part.startswith("csrftoken="):
                    return part.split('=')[1]
            return ""

    def spam_comments(self, url, message, count):
        try:
            print(f"{Fore.MAGENTA}[*] Cargando publicación...")
            self.driver.get(url)
            WebDriverWait(self.driver, 15).until(
                lambda d: self.driver.execute_script("return document.readyState === 'complete'")
            )
            post_id = self.get_post_id()
            if not post_id:
                print(f"{Fore.RED}[!] No se pudo obtener el ID del post")
                return
            api_url = f"https://www.instagram.com/api/v1/web/comments/{post_id}/add/"
            for i in range(count):
                if i % 3 == 0:
                    self.human_browsing_simulation(self.driver)
                try:
                    delay = self.delay_manager.wait()
                    dynamic_headers = self.get_dynamic_headers(url)
                    self.session.headers.update(dynamic_headers)
                    comment = self.generate_unique_comment(message)
                    response = self.session.post(api_url, data={'comment_text': comment})
                    if response.status_code == 200:
                        try:
                            json_response = response.json()
                            if json_response.get("status") == "ok":
                                print(f"{Fore.GREEN}[✓] Comment {i+1}/{count} | {comment} | Delay: {delay:.1f}s")
                            else:
                                print(f"{Fore.RED}[✗] Error en la respuesta JSON: {json_response}")
                        except Exception as json_e:
                            print(f"{Fore.RED}[!] Error al parsear JSON: {str(json_e)}")
                    else:
                        self.handle_error(response)
                except Exception as e:
                    print(f"{Fore.RED}[!] Error en comentario {i+1}: {str(e)}")
        finally:
            self.safe_shutdown()
    def safe_shutdown(self):
        """Cierre seguro de los recursos"""
        try:
            self.safe_shutdown()
        except Exception:
            pass

def main():
    logo = r"""
                      _..-'(                       )`-.._
                   ./'. '||\\.       (\_/)       .//||` .`\.
                ./'.|'.'||||\\|..    )O O(    ..|//||||`.`|.`\.
             ./'..|'.|| |||||\`````` '`"'` ''''''/||||| ||.`|..`\.
           ./'.||'.|||| ||||||||||||.     .|||||||||||| |||||.`||.`\.
          /'|||'.|||||| ||||||||||||{     }|||||||||||| ||||||.`|||`\
         '.|||'.||||||| ||||||||||||{     }|||||||||||| |||||||.`|||.`
        '.||| ||||||||| |/'   ``\||``     ''||/''   `\| ||||||||| |||.`
        |/' \./'     `\./         \!|\   /|!/         \./'     `\./ `\|
        V    V         V          }' `\ /' `{          V         V    V
        `    `         `               V               '         '    '
    """
    print(f"{Fore.RED}{logo}{Fore.RESET}")  # Opcional: añadir color
    name = f"""
    
  ░▒▓████████▓▒░▒▓█▓▒░             ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░  
  ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓██████▓▒░ ░▒▓█▓▒░             ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓████████▓▒░▒▓████████▓▒░      ░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  
    
    """
    print(f"{Fore.RED}{name}{Fore.RESET}")
    print(f"{Fore.RED}                **************************************************")
    print(f"{Fore.RED}                         INSTAGRAM COMMENT BOT - EL PORO v1.0")
    print(f"{Fore.RED}                **************************************************\n")
    
    bot = InstagramBot()
    try:
        bot.authenticate()
    except Exception:
        print(f"{Fore.RED}[!] Fallo en la autenticación. Terminando ejecución.")
        return
    try:
        new_csrf = bot.get_csrf_from_browser()
        bot.session.headers.update({
            'X-CSRFToken': new_csrf,
        })
        print(f"{Fore.YELLOW}[↻] Tokens de seguridad actualizados")
        post_url = input(f"{Fore.YELLOW}[?] Post URL: {Fore.WHITE}")
        message = input(f"{Fore.YELLOW}[?] Mensaje base: {Fore.WHITE}")
        count = int(input(f"{Fore.YELLOW}[?] Número de comentarios: {Fore.WHITE}"))
        bot.spam_comments(post_url, message, count)
        print(f"\n{Fore.GREEN}[✔] Operation completed!")
    except Exception as e:
        print(f"{Fore.RED}[!] Error en la ejecución: {str(e)}")
    finally:
        bot.safe_shutdown()

if __name__ == "__main__":
    main()
