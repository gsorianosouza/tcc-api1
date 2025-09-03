import numpy as np
import re
from urllib.parse import urlparse
import tldextract

FEATURE_COLUMNS = [
    'NumDots','SubdomainLevel','PathLevel','UrlLength','NumDash','NumDashInHostname',
    'AtSymbol','TildeSymbol','NumUnderscore','NumPercent','NumQueryComponents','NumAmpersand',
    'NumHash','NumNumericChars','NoHttps','RandomString','IpAddress','DomainInSubdomains',
    'DomainInPaths','HttpsInHostname','HostnameLength','PathLength','QueryLength','DoubleSlashInPath',
    'NumSensitiveWords','EmbeddedBrandName','PctExtHyperlinks','PctExtResourceUrls','ExtFavicon',
    'InsecureForms','RelativeFormAction','ExtFormAction','AbnormalFormAction','PctNullSelfRedirectHyperlinks',
    'FrequentDomainNameMismatch','FakeLinkInStatusBar','RightClickDisabled','PopUpWindow','SubmitInfoToEmail',
    'IframeOrFrame','MissingTitle','ImagesOnlyInForm','SubdomainLevelRT','UrlLengthRT','PctExtResourceUrlsRT',
    'AbnormalExtFormActionR','ExtMetaScriptLinkRT','PctExtNullSelfRedirectHyperlinksRT'
]

def extract_features(url_text: str):
    parsed_url = urlparse(url_text)
    
    features = {}
    
    features['NumDots'] = url_text.count('.')
    features['SubdomainLevel'] = len(tldextract.extract(parsed_url.netloc).subdomain.split('.')) -1 if tldextract.extract(parsed_url.netloc).subdomain else 0
    features['PathLevel'] = parsed_url.path.count('/')
    features['UrlLength'] = len(url_text)
    features['NumDash'] = url_text.count('-')
    features['NumDashInHostname'] = parsed_url.netloc.count('-')
    features['AtSymbol'] = 1 if '@' in url_text else 0
    features['TildeSymbol'] = 1 if '~' in url_text else 0
    features['NumUnderscore'] = url_text.count('_')
    features['NumPercent'] = url_text.count('%')
    features['NumQueryComponents'] = len(parsed_url.query.split('&')) if parsed_url.query else 0
    features['NumAmpersand'] = parsed_url.query.count('&')
    features['NumHash'] = 1 if '#' in url_text else 0
    features['NumNumericChars'] = sum(c.isdigit() for c in url_text)
    features['NoHttps'] = 0 if parsed_url.scheme == 'https' else 1
    features['RandomString'] = 0  
    features['IpAddress'] = 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", parsed_url.hostname or '') else 0
    features['DomainInSubdomains'] = 0 
    features['DomainInPaths'] = 0 
    features['HttpsInHostname'] = 1 if 'https' in parsed_url.netloc else 0
    features['HostnameLength'] = len(parsed_url.hostname or '')
    features['PathLength'] = len(parsed_url.path)
    features['QueryLength'] = len(parsed_url.query)
    features['DoubleSlashInPath'] = 1 if '//' in parsed_url.path else 0
    
    features['NumSensitiveWords'] = 0
    features['EmbeddedBrandName'] = 0
    features['PctExtHyperlinks'] = 0
    features['PctExtResourceUrls'] = 0
    features['ExtFavicon'] = 0
    features['InsecureForms'] = 0
    features['RelativeFormAction'] = 0
    features['ExtFormAction'] = 0
    features['AbnormalFormAction'] = 0
    features['PctNullSelfRedirectHyperlinks'] = 0
    features['FrequentDomainNameMismatch'] = 0
    features['FakeLinkInStatusBar'] = 0
    features['RightClickDisabled'] = 0
    features['PopUpWindow'] = 0
    features['SubmitInfoToEmail'] = 0
    features['IframeOrFrame'] = 0
    features['MissingTitle'] = 0
    features['ImagesOnlyInForm'] = 0
    features['SubdomainLevelRT'] = 0
    features['UrlLengthRT'] = 0
    features['PctExtResourceUrlsRT'] = 0
    features['AbnormalExtFormActionR'] = 0
    features['ExtMetaScriptLinkRT'] = 0
    features['PctExtNullSelfRedirectHyperlinksRT'] = 0

    try:
        extracted_features = [features[col] for col in FEATURE_COLUMNS]
    except KeyError as e:
        raise ValueError(f"Característica ausente: {e}. Verifique se todas as colunas do seu modelo foram extraídas.")
    
    return extracted_features