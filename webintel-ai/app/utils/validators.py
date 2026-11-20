import ipaddress
import socket
from urllib.parse import urlparse, urlunparse
from pydantic import HttpUrl

def normalize_and_validate_url(value: str | HttpUrl) -> str:
    url = str(value).strip()
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are supported.")
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("URL must contain a hostname and cannot contain credentials.")
    host = parsed.hostname.rstrip(".").lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".localhost"):
        raise ValueError("Localhost and local domains are not allowed.")
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80))}
    except socket.gaierror:
        raise ValueError("The website hostname could not be resolved.")
    if not addresses:
        raise ValueError("The website hostname has no resolved IP addresses.")
    for address in addresses:
        ip = ipaddress.ip_address(address)
        if not ip.is_global:
            raise ValueError("Private, loopback, link-local and reserved network addresses are not allowed.")
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", parsed.query, ""))

def validate_resolved_host(url: str) -> None:
    # Re-check every redirect destination. DNS rebinding protection in a high-risk
    # production deployment should additionally pin the validated IP at connection time.
    normalize_and_validate_url(url)
