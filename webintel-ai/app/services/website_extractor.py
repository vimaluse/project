import httpx
from bs4 import BeautifulSoup
from app.config import settings
from app.utils.validators import normalize_and_validate_url, validate_resolved_host

HEADERS = {"User-Agent": "WebIntelAI/1.0 (+website analysis; contact: admin@example.invalid)"}

async def fetch_website(url: str) -> dict:
    current = normalize_and_validate_url(url)
    async with httpx.AsyncClient(timeout=settings.request_timeout, headers=HEADERS,
                                 follow_redirects=False, verify=True) as client:
        for _ in range(settings.max_redirects + 1):
            validate_resolved_host(current)
            async with client.stream("GET", current) as response:
                if response.status_code in {301, 302, 303, 307, 308}:
                    location = response.headers.get("location")
                    if not location:
                        raise RuntimeError("Website returned a redirect without a destination.")
                    current = str(response.url.join(location))
                    continue
                if response.status_code >= 400:
                    raise RuntimeError(f"Website returned HTTP {response.status_code}.")
                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
                    raise RuntimeError("The supplied URL did not return an HTML page.")
                chunks, total = [], 0
                async for chunk in response.aiter_bytes():
                    total += len(chunk)
                    if total > settings.max_html_bytes:
                        raise RuntimeError("Website HTML exceeds the configured size limit.")
                    chunks.append(chunk)
                html = b"".join(chunks)
                final_url = str(response.url)
                break
        else:
            raise RuntimeError("Website exceeded the redirect limit.")

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe", "nav", "footer"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag.get("content", "").strip() if description_tag else ""
    canonical_tag = soup.find("link", rel="canonical")
    canonical = canonical_tag.get("href", "") if canonical_tag else ""
    headings = {f"h{i}": [h.get_text(" ", strip=True) for h in soup.find_all(f"h{i}")[:15]] for i in range(1, 4)}
    text = " ".join(soup.stripped_strings)
    text = " ".join(text.split())[:settings.max_text_chars]
    links = []
    for a in soup.find_all("a", href=True)[:30]:
        label = a.get_text(" ", strip=True)
        if label:
            links.append({"text": label[:120], "href": a["href"][:500]})
    return {
        "final_url": final_url, "title": title, "meta_description": description,
        "canonical": canonical, "headings": headings, "text": text,
        "links": links, "html_bytes": len(html),
        "extracted_characters": len(text),
    }
