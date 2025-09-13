import ipaddress
import re
from urllib.parse import urlparse
import whois
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Funções de utilidade
def get_domain_from_url(url):
    try:
        return urlparse(url).netloc
    except:
        return None

# Funções de extração de features
def havingIP(url):
    try:
        ipaddress.ip_address(urlparse(url).netloc)
        return 1
    except:
        return 0

def haveAtSign(url):
    return 1 if "@" in url else 0

def getLength(url):
    return len(url)

def getDepth(url):
    try:
        s = urlparse(url).path.split('/')
        depth = sum(1 for part in s if len(part) != 0)
        return depth
    except:
        return 0

def redirection(url):
    try:
        pos = url.rfind('//')
        if pos > 6:
            return 1
        return 0
    except:
        return 0

def httpDomain(url):
    try:
        domain = urlparse(url).netloc
        if 'https' in domain:
            return 1
        return 0
    except:
        return 0

def tinyURL(url):
    try:
        shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                            r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                            r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                            r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                            r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                            r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                            r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                            r"tr\.im|link\.zip\.net"
        match = re.search(shortening_services, url)
        return 1 if match else 0
    except:
        return 0

def prefixSuffix(url):
    try:
        return 1 if '-' in urlparse(url).netloc else 0
    except:
        return 0

def webTraffic(url):
    # A API do Alexa foi descontinuada, mas a feature original no dataset era numérica.
    # O valor 1.000.000 é um valor de fallback que a maioria dos modelos consideraria 'ruim'
    return 1000000

def domainAge(domain_name):
    try:
        whois_info = whois.whois(domain_name)
        creation_date = whois_info.creation_date
        
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if not creation_date:
            return 0 # Idade indeterminada
            
        age_in_days = (datetime.now() - creation_date).days
        return age_in_days
    except:
        return 0

def domainEnd(domain_name):
    try:
        whois_info = whois.whois(domain_name)
        expiration_date = whois_info.expiration_date

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        if not expiration_date:
            return 0 # Data de expiração indeterminada
        
        end_in_days = (expiration_date - datetime.now()).days
        return end_in_days
    except:
        return 0

def iframe(response_text):
    return 0 if re.findall(r"[<iframe>|<frameBorder>]", response_text) else 1

def mouseOver(response_text):
    return 1 if re.findall("<script>.+onmouseover.+</script>", response_text) else 0

def rightClick(response_text):
    return 0 if re.findall(r"event.button ?== ?2", response_text) else 1

def forwarding(response):
    return 1 if response and len(response.history) > 2 else 0

def dnsRecord(domain_name):
    try:
        whois.whois(domain_name)
        return 0
    except Exception:
        return 1

# Função unificada para extrair todas as features
def extract_all_features(url):
    features = {}
    
    domain = get_domain_from_url(url)
    if not domain:
        # Vetor de features padrão para URL inválida
        return {
            "Have_IP": 0, "Have_At": 0, "URL_Length": 0, "URL_Depth": 0,
            "Redirection": 0, "https_Domain": 0, "TinyURL": 0, "Prefix/Suffix": 0,
            "DNS_Record": 1, "Web_Traffic": 1000000, "Domain_Age": 0, "Domain_End": 0,
            "iFrame": 1, "Mouse_Over": 1, "Right_Click": 1, "Web_Forwards": 1
        }
        
    # Extração de features que não dependem da resposta HTTP
    features['Have_IP'] = havingIP(url)
    features['Have_At'] = haveAtSign(url)
    features['URL_Length'] = getLength(url)
    features['URL_Depth'] = getDepth(url)
    features['Redirection'] = redirection(url)
    features['https_Domain'] = 1 if url.startswith('https') else 0
    features['TinyURL'] = tinyURL(url)
    features['Prefix/Suffix'] = prefixSuffix(url)
    features['DNS_Record'] = dnsRecord(domain)
    
    # Extração de features que dependem da resposta HTTP
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        response_text = response.text
        
        features['Web_Traffic'] = webTraffic(url)
        features['Domain_Age'] = domainAge(domain)
        features['Domain_End'] = domainEnd(domain)
        
        features['iFrame'] = iframe(response_text)
        features['Mouse_Over'] = mouseOver(response_text)
        features['Right_Click'] = rightClick(response_text)
        features['Web_Forwards'] = forwarding(response)
        
    except Exception as e:
        print(f"Erro na requisição HTTP para {url}: {e}")
        # Valores padrão de phishing para as features que falharam
        features['Web_Traffic'] = 1000000
        features['Domain_Age'] = 0
        features['Domain_End'] = 0
        features['iFrame'] = 1
        features['Mouse_Over'] = 1
        features['Right_Click'] = 1
        features['Web_Forwards'] = 1
    
    return features