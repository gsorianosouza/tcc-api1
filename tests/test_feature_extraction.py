from model import feature_extractor

def test_get_domain_from_url(fake):
    url = fake.url()
    domain = feature_extractor.get_domain_from_url(url)
    assert domain in url


def test_haveAtSign(fake):
    url = fake.url()
    assert feature_extractor.haveAtSign(url) == 0
    url_at = url.replace("://", "://user@")
    assert feature_extractor.haveAtSign(url_at) == 1


def test_getLength(fake):
    url = fake.url()
    assert feature_extractor.getLength(url) == len(url)


def test_getDepth_simple():
    url = "http://example.com/a/b/c"
    depth = feature_extractor.getDepth(url)
    assert depth == 3


def test_redirection():
    url = "http://example.com//redirect"
    assert feature_extractor.redirection(url) == 1
    url2 = "http://example.com"
    assert feature_extractor.redirection(url2) == 0


def test_tinyURL_known():
    url = "http://bit.ly/teste"
    assert feature_extractor.tinyURL(url) == 1
    url2 = "http://example.com"
    assert feature_extractor.tinyURL(url2) == 0


def test_prefixSuffix():
    url = "http://sub-domain.example.com"
    assert feature_extractor.prefixSuffix(url) == 1
    url2 = "http://example.com"
    assert feature_extractor.prefixSuffix(url2) == 0


def test_iframe_mouseover_rightclick():
    html = """
    <html>
      <body>
        <iframe src="test"></iframe>
        <div onmouseover="alert('x')"></div>
        <script>if(event.button == 2) {}</script>
      </body>
    </html>
    """
    assert feature_extractor.iframe(html) == 1
    assert feature_extractor.mouseOver(html) == 1
    assert feature_extractor.rightClick(html) == 1


def test_has_login_form_detects_form():
    html = """
    <form action="/login">
      <input type="email" name="email"/>
      <input type="password" name="password"/>
    </form>
    """
    assert feature_extractor.has_login_form(html) == 1

def test_get_form_action_url_suspect():
    base_url = "http://example.com"
    html = """
    <form action="http://malicious.com/login">
      <input type="text" name="test"/>
    </form>
    """
    result = feature_extractor.get_form_action_url(html, base_url)
    assert result == 1
    
def test_get_suspicious_keywords():
    html = "Please verify your account urgently!"
    assert feature_extractor.get_suspicious_keywords(html) == 1
    html2 = "Hello world"
    assert feature_extractor.get_suspicious_keywords(html2) == 0


def test_extract_all_features(monkeypatch, fake):

    url = fake.url()

    monkeypatch.setattr(feature_extractor, "get_whois_info", lambda x: "mock_whois")
    monkeypatch.setattr(feature_extractor, "dnsRecord", lambda x: 0)
    monkeypatch.setattr(feature_extractor, "domainAge", lambda x: 365)
    monkeypatch.setattr(feature_extractor, "domainEnd", lambda x: 100)

    class DummyResponse:
        text = "<iframe></iframe><form action='http://malicious.com/login'><input type='password'/></form>"
        history = [1,2,3]
    monkeypatch.setattr(feature_extractor, "get_url_response", lambda x: DummyResponse())

    features = feature_extractor.extract_all_features(url)

    expected_keys = [
        "Have_IP", "Have_At", "URL_Length", "URL_Depth",
        "Redirection", "https_Domain", "TinyURL", "Prefix/Suffix",
        "DNS_Record", "Web_Traffic", "Domain_Age", "Domain_End",
        "iFrame", "Mouse_Over", "Right_Click", "Web_Forwards",
        "Has_LoginForm", "Form_Action_Suspect", "Suspicious_Keywords"
    ]
    for k in expected_keys:
        assert k in features

    assert features["Domain_Age"] == 365
    assert features["Domain_End"] == 100
    assert features["DNS_Record"] == 0
