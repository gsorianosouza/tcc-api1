import ipaddress
import re
import socket
import ssl
from urllib.parse import urlparse, urljoin
import whois
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_domain_from_url(url):
    try:
        return urlparse(url).netloc
    except:
        return None

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
        return 1 if pos > 6 else 0
    except:
        return 0

def httpDomain(url):
    try:
        domain = urlparse(url).netloc
        return 1 if 'https' in domain else 0
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

def dnsRecord(domain):
    try:
        whois.whois(domain)
        return 0
    except Exception:
        return 1

def webTraffic(url):
    return 1000000

def domainAge(domain_name):
    try:
        whois_info = whois.whois(domain_name)
        creation_date = whois_info.creation_date
        
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if not creation_date:
            return 0
            
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
            return 0
        
        end_in_days = (expiration_date - datetime.now()).days
        return end_in_days
    except:
        return 0

def iframe(response_text):
    return 1 if response_text and re.findall(r"<iframe|<frameBorder>", response_text) else 0

def mouseOver(response_text):
    return 1 if response_text and re.findall(r"onmouseover", response_text) else 0

def rightClick(response_text):
    return 1 if response_text and re.findall(r"event.button ?== ?2", response_text) else 0

def forwarding(response):
    return 1 if response and len(response.history) > 2 else 0

def get_url_response(url):
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        return response
    except Exception:
        return None

def get_whois_info(domain):
    try:
        whois_info = whois.whois(domain)
        return whois_info
    except Exception:
        return None
        
def get_certificate_details(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as sslsock:
                cert = sslsock.getpeercert()
                issuer = dict(x[0] for x in cert['issuer'])
                subject = dict(x[0] for x in cert['subject'])
                return {
                    'issued_to': subject.get('commonName'),
                    'issued_by': issuer.get('organizationName'),
                    'valid_until': cert.get('notAfter')
                }
    except Exception as e:
        return None

def has_login_form(response_text):
    try:
        soup = BeautifulSoup(response_text, 'html.parser')
        form_tags = soup.find_all('form')
        for form in form_tags:
            if any(field.get('type') in ['password', 'email'] for field in form.find_all('input')):
                return 1
        return 0
    except:
        return 0

def get_form_action_url(response_text, base_url):
    try:
        soup = BeautifulSoup(response_text, 'html.parser')
        form_tags = soup.find_all('form')
        for form in form_tags:
            action = form.get('action')
            if action:
                action_url = urljoin(base_url, action)
                if urlparse(action_url).netloc != urlparse(base_url).netloc:
                    return 1
        return 0
    except:
        return 0

def get_suspicious_keywords(response_text):
    try:
        suspicious_words = r'login|account|verify|update|urgent|password|security|billing'
        return 1 if re.search(suspicious_words, response_text, re.IGNORECASE) else 0
    except:
        return 0

def extract_all_features(url):
    features = {}
    
    domain = get_domain_from_url(url)
    
    features = {
        "Have_IP": 0, "Have_At": 0, "URL_Length": 0, "URL_Depth": 0,
        "Redirection": 0, "https_Domain": 0, "TinyURL": 0, "Prefix/Suffix": 0,
        "DNS_Record": 1, "Web_Traffic": 1000000, "Domain_Age": 0, "Domain_End": 0,
        "iFrame": 1, "Mouse_Over": 1, "Right_Click": 1, "Web_Forwards": 1,
        "Has_LoginForm": 0, "Form_Action_Suspect": 0, "Suspicious_Keywords": 0
    }

    if not domain:
        return features

    whois_info = get_whois_info(domain)
    features['Have_IP'] = havingIP(url)
    features['Have_At'] = haveAtSign(url)
    features['URL_Length'] = getLength(url)
    features['URL_Depth'] = getDepth(url)
    features['Redirection'] = redirection(url)
    features['https_Domain'] = 1 if url.startswith('https') else 0
    features['TinyURL'] = tinyURL(url)
    features['Prefix/Suffix'] = prefixSuffix(url)
    
    features['DNS_Record'] = dnsRecord(whois_info)
    features['Domain_Age'] = domainAge(whois_info)
    features['Domain_End'] = domainEnd(whois_info)
    
    response = get_url_response(url)
    if response:
        features['Web_Traffic'] = webTraffic(url)
        features['iFrame'] = iframe(response.text)
        features['Mouse_Over'] = mouseOver(response.text)
        features['Right_Click'] = rightClick(response.text)
        features['Web_Forwards'] = forwarding(response)
        features['Has_LoginForm'] = has_login_form(response.text)
        features['Form_Action_Suspect'] = get_form_action_url(response.text, url)
        features['Suspicious_Keywords'] = get_suspicious_keywords(response.text)
    
    return features