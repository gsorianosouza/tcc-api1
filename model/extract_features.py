import numpy as np

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

def extract_features(payload: dict):
    return np.array([[payload[col] for col in FEATURE_COLUMNS]])