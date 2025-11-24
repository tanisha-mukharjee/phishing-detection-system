# app/feature_extraction.py

import re
from urllib.parse import urlparse

def extract_features(url):
    """
    Extracts advanced features from a URL for phishing detection.
    Returns a dictionary that can be converted to a DataFrame.
    """

    # Feature 1: URL length
    url_length = len(url)

    # Feature 2: Presence of '@' symbol (phishing URLs sometimes hide real links after '@')
    has_at_symbol = 1 if "@" in url else 0

    # Feature 3: Uses HTTPS
    has_https = 1 if url.startswith("https") else 0

    # Feature 4: Number of digits
    num_digits = sum(char.isdigit() for char in url)

    # Feature 5: Presence of hyphen (phishing domains often use '-')
    has_hyphen = 1 if "-" in url else 0

    # Feature 6: Count of dots
    num_dots = url.count('.')

    # Feature 7: Suspicious keywords (like "login", "secure", "verify", "update", etc.)
    suspicious_keywords = ['login', 'secure', 'verify', 'update', 'account', 'bank', 'signin', 'payment', 'confirm']
    has_suspicious_words = 1 if any(word in url.lower() for word in suspicious_keywords) else 0

    # Feature 8: Contains IP address instead of domain
    has_ip = 1 if re.match(r"^http[s]?://\d{1,3}(\.\d{1,3}){3}", url) else 0

    # Feature 9: Length of domain name
    domain = urlparse(url).netloc
    domain_length = len(domain)

    # Combine all features
    features = {
        'url_length': url_length,
        'has_at_symbol': has_at_symbol,
        'has_https': has_https,
        'num_digits': num_digits,
        'has_hyphen': has_hyphen,
        'num_dots': num_dots,
        'has_suspicious_words': has_suspicious_words,
        'has_ip': has_ip,
        'domain_length': domain_length
    }

    return features
