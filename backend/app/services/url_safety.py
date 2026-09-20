import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from dotenv import load_dotenv


load_dotenv()


SAFE_BROWSING_API_URL = (
    "https://safebrowsing.googleapis.com/v4/threatMatches:find"
)

TRUSTED_MARKETPLACE_DOMAINS = {
    "daangn.com",
    "bunjang.co.kr",
    "joongna.com",
    "joonggonara.co.kr",
}

URL_PATTERN = re.compile(
    r"https?://[^\s<>'\"]+|www\.[^\s<>'\"]+",
    re.IGNORECASE,
)


def extract_urls(text: str) -> list[str]:
    urls = URL_PATTERN.findall(text or "")
    cleaned_urls = []

    for url in urls:
        url = url.rstrip(".,!?;:)]}")

        if url.startswith("www."):
            url = f"https://{url}"

        if url not in cleaned_urls:
            cleaned_urls.append(url)

    return cleaned_urls


def get_domain(url: str) -> str:
    try:
        return (urlparse(url).hostname or "").lower()
    except ValueError:
        return ""


def is_trusted_marketplace(domain: str) -> bool:
    return any(
        domain == trusted_domain
        or domain.endswith(f".{trusted_domain}")
        for trusted_domain in TRUSTED_MARKETPLACE_DOMAINS
    )


def check_url_safety(listing: str, chat: str) -> list[dict]:
    urls = extract_urls(f"{listing}\n{chat}")

    if not urls:
        return []

    results = []
    external_urls = []

    for url in urls:
        domain = get_domain(url)

        if is_trusted_marketplace(domain):
            results.append(
                {
                    "url": url,
                    "domain": domain,
                    "status": "TRUSTED_MARKETPLACE",
                    "threat_types": [],
                }
            )
        else:
            external_urls.append(url)

    if not external_urls:
        return results

    api_key = os.getenv("SAFE_BROWSING_API_KEY")

    if not api_key:
        for url in external_urls:
            results.append(
                {
                    "url": url,
                    "domain": get_domain(url),
                    "status": "UNAVAILABLE",
                    "threat_types": [],
                }
            )

        return results

    request_body = {
        "client": {
            "clientId": "trust404",
            "clientVersion": "1.0.0",
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
            ],
            "platformTypes": [
                "ANY_PLATFORM",
            ],
            "threatEntryTypes": [
                "URL",
            ],
            "threatEntries": [
                {"url": url}
                for url in external_urls[:50]
            ],
        },
    }

    request = Request(
        f"{SAFE_BROWSING_API_URL}?key={api_key}",
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=5) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        matches = data.get("matches", [])

        for url in external_urls:
            matched_threats = []

            for match in matches:
                threat = match.get("threat", {})

                if threat.get("url") == url:
                    threat_type = match.get("threatType")

                    if threat_type:
                        matched_threats.append(threat_type)

            results.append(
                {
                    "url": url,
                    "domain": get_domain(url),
                    "status": (
                        "THREAT_FOUND"
                        if matched_threats
                        else "NO_KNOWN_THREAT"
                    ),
                    "threat_types": matched_threats,
                }
            )

    except (
        HTTPError,
        URLError,
        TimeoutError,
        json.JSONDecodeError,
        UnicodeDecodeError,
    ):
        for url in external_urls:
            results.append(
                {
                    "url": url,
                    "domain": get_domain(url),
                    "status": "UNAVAILABLE",
                    "threat_types": [],
                }
            )

    return results