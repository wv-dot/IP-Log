from telegraph import Telegraph
from email.mime.text import MIMEText
from email.utils import make_msgid, formatdate 
from pystyle import *
from concurrent.futures import ThreadPoolExecutor
import os, time, pyshorteners, smtplib, ssl, requests, urllib.request, json, socket

banner = """██╗░░░░░░█████╗░░██████╗
██║░░░░░██╔══██╗██╔════╝
██║░░░░░██║░░██║██║░░██╗
██║░░░░░██║░░██║██║░░╚██╗
███████╗╚█████╔╝╚██████╔╝
╚══════╝░╚════╝░░╚═════
	╔═══════════════╗
     	 MENU
	  1. Telegraph
	  2. Short link
	  3. Spoofer
	  4. Search IP
	  5. config
	╚═══════════════╝
"""

config = {}

def load_config():
    global config
    config = {}
    if os.path.exists("config.txt"):
        with open("config.txt", 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()

def pc(st):
    print(Colorate.Horizontal(Colors.cyan_to_blue, st))
    
def inp(st):
    return input(Colorate.Horizontal(Colors.cyan_to_blue, st, 1, True))

def send(message):
    try:
        if not config:
            load_config()
            
        bot_token = config.get('BOT_TOKEN')
        chat_id = config.get('CHAT_ID')
        
        if not bot_token or not chat_id:
            print("Ошибка: отсутствуют BOT_TOKEN или CHAT_ID")
            return
            
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={
                'chat_id': chat_id,
                'text': message,
                'disable_web_page_preview': True,
                'parse_mode': 'HTML'
            },
            timeout=5
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def update(key, value):
    global config
    config[key] = value
    
    with open("config.txt", 'w') as f:
        for param in ["BOT_TOKEN", "CHAT_ID", "EMAIL", "PASSWORD"]:
            if param in config:
                f.write(f"{param}={config[param]}\n")

def cfg():
    ban = """██╗░░░░░░█████╗░░██████╗
██║░░░░░██╔══██╗██╔════╝
██║░░░░░██║░░██║██║░░██╗
██║░░░░░██║░░██║██║░░╚██╗
███████╗╚█████╔╝╚██████╔╝
╚══════╝░╚════╝░░╚═════
	╔═══════════════╗
      CONFIG
	  1. BOT_TOKEN
	  2. CHAT_ID
	  3. EMAIL
	  4. PASSWORD
	╚═══════════════╝
"""
    os.system('clear')
    pc(Center.XCenter(ban))
    c = inp("[?] Выберите опцию: ")
    if c == '1':
        update("BOT_TOKEN", inp("[?] Введите новый токен: "))
    elif c == '2':
        update("CHAT_ID", inp("[?] Введите новый айди: "))
    elif c == '3':
        update("EMAIL", inp("[?] Введите новую почту [gmail]: "))
    elif c == '4':
        update("PASSWORD", inp("[?] Введите новый пароль: "))
    pc("[+] Данные обновлены!")
    time.sleep(2)
    os.system('clear')
    pc(Center.XCenter(banner))

load_config()

os.system('clear')
pc(Center.XCenter(banner))

def create_telegraph(title, text, image_url):
    telegraph = Telegraph()
    telegraph.create_account(short_name='ㅤ')
    
    html_content = f"<p>{text}</p><img src='{image_url}'/>"
    
    response = telegraph.create_page(
        title=title,
        html_content=html_content
    )
    
    return response['url']

def telegraph():
    ban = """██╗░░░░░░█████╗░░██████╗
██║░░░░░██╔══██╗██╔════╝
██║░░░░░██║░░██║██║░░██╗
██║░░░░░██║░░██║██║░░╚██╗
███████╗╚█████╔╝╚██████╔╝
╚══════╝░╚════╝░░╚═════
	╔═══════════════╗
     Telegraph
	  1. Default
	  2. Text link
	╚═══════════════╝
"""
    os.system('clear')
    pc(Center.XCenter(ban))
    c = inp("[?] Выберите опцию: ")
    os.system('clear')
    pc(Center.XCenter(ban))
    if c == '1':
    	title = inp("[?] Введите заголовок статьи: ")
    	text = inp("[+] Введите текст статьи: ")
    	img_url = inp("[+] Введите ссылку на логгер: ")
    	article_url = create_telegraph(title, text, img_url)
    	pc("\n[!] Статья успешно создана по ссылке:")
    	print(f"\033[01;38;05;15m{article_url}")
    	send(f"<b>💠 Ваша статья успешно создана</b>\n\n<b>📃 Ссылка:</b>\n<blockquote><code>{article_url}</code>\n[нажмите, чтобы скопировать]</blockquote>") 	

    elif c == '2':
    	type = ''
    	st = inp("[?] Введите текст: ")
    	img_url = inp("[+] Введите ссылку на логгер: ")
    	pc("[+] Текст успешно создан, проверьте TG бота")
    	if st[:1] == '@':
    		type = 'username'
    	else:
    		type = 'custom'
    	send(f"<b>💠 Текст с логгером успешно создан!\n</b><blockquote><b>Тип: {type}\nИсходный текст: {st}\nПрямая ссылка на логгер: {img_url}</b></blockquote>\n\n<b>Текст будет отправлен ниже ⬇️</b>")
    	send(f'<a href="{create_telegraph("ㅤ", "ㅤ", img_url)}">{st}</a>')
    else:
    	pc("[!] Ошибка ввода")
    time.sleep(2)
    os.system('clear')
    pc(Center.XCenter(banner))

def short_link():
    ban = """██╗░░░░░░█████╗░░██████╗
██║░░░░░██╔══██╗██╔════╝
██║░░░░░██║░░██║██║░░██╗
██║░░░░░██║░░██║██║░░╚██╗
███████╗╚█████╔╝╚██████╔╝
╚══════╝░╚════╝░░╚═════
	╔═══════════════╗
      SERVICE
	  1. clck.ru
	  2. da.gd
	╚═══════════════╝
"""
    os.system('clear')
    pc(Center.XCenter(ban))
    choice = inp("[?] Выберите сервис: ")
    long_url = inp("[+] Введите ссылку для сокращения: ")
    
    shortener = pyshorteners.Shortener(timeout=3)
    short_url = ""
    
    try:
        if choice == "1":
            short_url = shortener.clckru.short(long_url)
        elif choice == "2":
            short_url = shortener.dagd.short(long_url)
        pc(f"\n[!] Сокращённая ссылка:")
        print(f"\033[01;38;05;15m{short_url}")
        send(f"<b>💠 Ваша ссылка успешно создана</b>\n\n<b>📃 Сокращённая ссылка:</b>\n<blockquote><code>{short_url}</code>\n[нажмите, чтобы скопировать]</blockquote>")
    except Exception as e:
        print(f"Ошибка: {e}")
    time.sleep(3)
    os.system('clear')
    pc(Center.XCenter(banner))
    
def spoofer():
    load_config()
    
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = config.get("EMAIL", "")
    SENDER_PASSWORD = config.get("PASSWORD", "")
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Ошибка: email или пароль не настроены!")
        time.sleep(2)
        return
    
    os.system('clear')
    pc(Center.XCenter(banner))
    recipient = inp("[?] Введите email получателя: ").strip()
    subject = inp("[+] Введите тему письма: ").strip()
    body = inp("[+] Введите текст письма: ")
    
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject
    msg['Date'] = formatdate()
    msg['Message-ID'] = make_msgid(domain='gmail.com')
    msg['X-Mailer'] = "My account"
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        pc(f"[+] Письмо успешно отправлено на {recipient}")
    except smtplib.SMTPAuthenticationError:
        print("Ошибка авторизации. Проверьте пароль")
    except Exception as e:
        print(f"Ошибка отправки: {e}")
    time.sleep(2)

def check_port(ip, port):
    ports_info = {
        80: "HTTP",
        443: "HTTPS",
        8080: "HTTP-Alt",
        1024: "Custom"
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            service = ports_info.get(port, "Unknown")
            return f"Порт {port} [{service}]: OPEN"
        return f"Порт {port}: CLOSED"
    except:
        return f"Порт {port}: ERROR"

def check_ports_parallel(ip, ports):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda p: check_port(ip, p), ports))
    return results

def check_vpn(ip):
    try:
        with ThreadPoolExecutor() as executor:
            dns_future = executor.submit(check_vpn_dns, ip)
            tor_future = executor.submit(check_tor_exit, ip)
            hosting_future = executor.submit(check_hosting, ip)
            
            results = []
            if (dns_result := dns_future.result()):
                results.append(dns_result)
            if (tor_result := tor_future.result()):
                results.append(tor_result)
            if (hosting_result := hosting_future.result()):
                results.append(hosting_result)
            
            return "\n".join(results) if results else "Прямое соединение"
    except:
        return "Не удалось проверить"

def check_vpn_dns(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0].lower()
        if any(kw in hostname for kw in ['vpn', 'proxy', 'tor', 'exit', 'relay']):
            return f"Обнаружен VPN/прокси/Tor [DNS: {hostname}]"
    except:
        return None

def check_tor_exit(ip):
    try:
        tor_nodes = requests.get('https://check.torproject.org/torbulkexitlist', timeout=3).text.split('\n')
        if ip in tor_nodes:
            return "Обнаружен Tor exit node"
    except:
        return None

def check_hosting(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        if data.get('hosting', False) or data.get('proxy', False):
            return "Обнаружен хостинг/VPN [ip-api.com]"
    except:
        return None

def search_by_ip(ip):
    try:
        with urllib.request.urlopen(f"https://ipinfo.io/{ip}/json", timeout=3) as response:
            ip_info = json.load(response)
    except:
        return None

    result = {
        "query": ip_info.get('ip', 'Неизвестно'),
        "city": ip_info.get('city', 'Неизвестно'),
        "region": ip_info.get('region', 'Неизвестно'),
        "country": ip_info.get('country', 'Неизвестно'),
        "org": ip_info.get('org', 'Неизвестно'),
        "loc": ip_info.get('loc', '')
    }

    if result["loc"]:
        try:
            latitude, longitude = result["loc"].split(",")
            with urllib.request.urlopen(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}", timeout=3) as response:
                address_data = json.load(response)
                result["address"] = address_data.get("address", {})
        except:
            result["address"] = None
    else:
        result["address"] = None

    return result

def get_ip_info(ip):
    result = {
        "basic_info": "",
        "address_info": "",
        "ports_info": ""
    }
    
    with ThreadPoolExecutor() as executor:
        ip_data_future = executor.submit(search_by_ip, ip)
        vpn_future = executor.submit(check_vpn, ip)
        
        ip_data = ip_data_future.result()
        if not ip_data or isinstance(ip_data, str):
            return {"error": "Информация по IP не найдена"}
        
        basic_info = []
        basic_info.append(f"IP: {ip_data.get('query', 'Неизвестно')}")
        basic_info.append(f"Страна: {ip_data.get('country', 'Неизвестно')}")
        basic_info.append(f"Регион: {ip_data.get('region', 'Неизвестно')}")
        basic_info.append(f"Город: {ip_data.get('city', 'Неизвестно')}")
        
        if ip_data.get('loc'):
            lat, lon = ip_data['loc'].split(',')
            basic_info.append(f"Координаты: {lat}, {lon}")
        
        basic_info.append(f"Организация: {ip_data.get('org', 'Неизвестно')}")
        basic_info.append(f"Статус подключения: {vpn_future.result()}")
        result["basic_info"] = "\n".join(basic_info)
        
        address_info = []
        if isinstance(ip_data.get("address"), dict):
            for key, value in ip_data["address"].items():
                address_info.append(f"{key.capitalize()}: {value}")
        else:
            address_info.append("Адресная информация недоступна")
        result["address_info"] = "\n".join(address_info)
        
        ports_info = check_ports_parallel(ip, [80, 443, 8080, 1024])
        result["ports_info"] = "\n".join(ports_info)
    
    return result

def ip():
    os.system('clear')
    pc(Center.XCenter(banner))
    while True:
        ip_ad = inp("[?] Введите IP для анализа: ")
        if ip_ad == "0":
            break
            
        info = get_ip_info(ip_ad)
        
        if "error" in info:
            pc(f"\n{info['error']}")
        else:
            pc("\n[+] Основная информация:")
            pc(info["basic_info"])
            
            pc("\n[+] Адрес:")
            pc(info["address_info"])
            
            pc("\n[+] Порты:")
            pc(info["ports_info"])
            print()
                     
            send(f'💠 <b>Получен новый IP!</b>\n\n📃 <b>Основная информация:</b>\n<blockquote>{info["basic_info"]}</blockquote>\n\n🌐 <b>Адрес:</b>\n<blockquote>{info["address_info"]}</blockquote>\n\n🔌 <b>Порты:</b>\n<blockquote>{info["ports_info"]}</blockquote>')
            time.sleep(3)
            os.system('clear')
            pc(Center.XCenter(banner))
                            
def main():
    c = inp("[?] Выберите опцию: ")
    if c == '1':        
        telegraph()
    elif c == '2':
        short_link()
    elif c == '3':
        spoofer()
    elif c == '4':
    	ip()
    elif c == '5':
        cfg()


while True:
	main()
