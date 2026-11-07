"""Write static search and social metadata from site-config.json."""
import json
import re
import sys
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
BEGIN = "<!-- BEGIN GENERATED SEARCH AND SOCIAL METADATA -->"
END = "<!-- END GENERATED SEARCH AND SOCIAL METADATA -->"
BLOCK = re.compile(re.escape(BEGIN) + ".*?" + re.escape(END), re.DOTALL)
PREVIEW = "images/social-preview.png"
PREVIEW_ALT = "White Armenian eternity mark above Ara Giulambarian and Senior Experience Designer on a black background."
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
AUTHOR_NAME = "Ara Giulambarian"


class CaseMetadata(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.headline = ""
        self.image = None
        self.in_headline = False
        self.in_cover = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1" and attrs.get("id") == "case-title":
            self.in_headline = True
        if tag == "figure" and "case-cover" in (attrs.get("class") or "").split():
            self.in_cover = True
        if tag == "img" and self.in_cover:
            self.image = attrs.get("src")

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_headline = False
        if tag == "figure":
            self.in_cover = False

    def handle_data(self, text):
        if self.in_headline:
            self.headline += text


def read_base_url():
    value = json.loads((ROOT / "site-config.json").read_text(encoding="utf-8"))["base_url"]
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Set base_url to the exact public HTTPS site URL, or null for local preview.")
    value = value.strip()
    parsed = urlsplit(value)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or "." not in parsed.hostname
        or parsed.username is not None
        or parsed.query
        or parsed.fragment
        or any(char.isspace() or char in '<>"\\' for char in value)
        or not re.fullmatch(r"(?:/[A-Za-z0-9._~-]+)*/?", parsed.path)
        or any(part in (".", "..") for part in parsed.path.split("/"))
    ):
        raise ValueError("Set base_url to the public HTTPS site URL, including any repository subpath.")
    return value.rstrip("/") + "/"


def single(pattern, source, label):
    values = re.findall(pattern, source)
    if len(values) != 1:
        raise ValueError(f"Expected exactly one {label}.")
    return unescape(values[0])


def meta(attribute, name, value):
    return f'<meta {attribute}="{name}" content="{escape(value, quote=True)}">'


def structured_data(page_type, source, base_url, canonical, description):
    profile_url = base_url + "about/" if base_url else None
    author = {"@type": "Person", "name": AUTHOR_NAME}
    if profile_url:
        author.update({"@id": profile_url + "#ara-giulambarian", "url": profile_url})
    context = {"@context": "https://schema.org"}

    if page_type == "profile":
        author.update({
            "jobTitle": "Senior Experience Designer",
            "worksFor": {"@type": "Organization", "name": "Westpac"},
            "workLocation": {"@type": "Place", "name": "Sydney, Australia"},
            "sameAs": ["https://www.linkedin.com/in/arglm/"],
        })
        profile = {**context, "@type": "ProfilePage", "mainEntity": author}
        if profile_url:
            profile["url"] = profile_url
            author["image"] = base_url + "images/ara-about.webp"
        return profile

    if page_type == "article":
        case = CaseMetadata(source)
        if not case.headline.strip() or not case.image:
            raise ValueError("Case study requires a main headline and cover image.")
        article = {
            **context,
            "@type": "Article",
            "headline": " ".join(case.headline.split()),
            "description": description,
            "inLanguage": "en-AU",
            "author": author,
        }
        if canonical:
            article.update({
                "url": canonical,
                "mainEntityOfPage": {"@id": canonical},
                "image": urljoin(canonical, case.image),
            })
        return article

    if page_type == "website" and canonical == base_url and base_url:
        return {
            **context,
            "@type": "WebSite",
            "name": AUTHOR_NAME,
            "url": base_url,
            "inLanguage": "en-AU",
            "publisher": author,
        }
    return None


def page_metadata(page, text, base_url):
    title = single(r"<title>([^<]+)</title>", text, "page title")
    description = single(r'<meta\s+name="description"\s+content="([^"]+)"\s*/?>', text, "description")
    page_type = "website"
    if page.parent == ROOT / "about":
        page_type = "profile"
    elif page.parent.parent == ROOT / "case-studies":
        page_type = "article"

    lines = [
        meta("property", "og:title", title),
        meta("property", "og:description", description),
        meta("property", "og:type", page_type),
        meta("property", "og:site_name", AUTHOR_NAME),
        meta("name", "twitter:card", "summary_large_image"),
        meta("name", "twitter:title", title),
        meta("name", "twitter:description", description),
    ]
    canonical = None
    if base_url:
        route = page.relative_to(ROOT).as_posix().removesuffix("index.html")
        canonical = base_url + route
        image = base_url + PREVIEW
        lines.extend([
            f'<link rel="canonical" href="{escape(canonical, quote=True)}">',
            meta("property", "og:url", canonical),
            meta("property", "og:image", image),
            meta("property", "og:image:type", "image/png"),
            meta("property", "og:image:width", "1200"),
            meta("property", "og:image:height", "630"),
            meta("property", "og:image:alt", PREVIEW_ALT),
            meta("name", "twitter:image", image),
            meta("name", "twitter:image:alt", PREVIEW_ALT),
        ])

    schema = structured_data(page_type, text, base_url, canonical, description)
    if schema:
        lines.append('<script type="application/ld+json">')
        lines.append(json.dumps(schema, ensure_ascii=False, indent=2).replace("<", "\\u003c"))
        lines.append("</script>")

    block = "\n".join([BEGIN, *lines, END])
    updated, count = BLOCK.subn(lambda _: block, text)
    if count != 1:
        raise ValueError(f"Expected one metadata block in {page.relative_to(ROOT)}.")
    return updated, canonical


def main():
    base_url = read_base_url()
    pages = [
        ROOT / "index.html",
        ROOT / "about/index.html",
        ROOT / "case-studies/index.html",
        *sorted((ROOT / "case-studies").glob("*/index.html")),
    ]
    results = [page_metadata(page, page.read_text(encoding="utf-8"), base_url) for page in pages]
    robots = "User-agent: *\nAllow: /\n"
    sitemap_file = ROOT / "sitemap.xml"
    if base_url:
        ET.register_namespace("", SITEMAP_NS)
        urlset = ET.Element(f"{{{SITEMAP_NS}}}urlset")
        for _, canonical in results:
            item = ET.SubElement(urlset, f"{{{SITEMAP_NS}}}url")
            ET.SubElement(item, f"{{{SITEMAP_NS}}}loc").text = canonical
        ET.indent(urlset)
        ET.ElementTree(urlset).write(sitemap_file, encoding="utf-8", xml_declaration=True)
        robots += f"\nSitemap: {base_url}sitemap.xml\n"
    else:
        sitemap_file.unlink(missing_ok=True)

    for page, (updated, _) in zip(pages, results):
        page.write_text(updated, encoding="utf-8")
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    if base_url:
        print(f"Generated metadata and sitemap for {len(pages)} pages at {base_url}")
    else:
        print("Set site-config.json base_url and rerun to generate canonicals, social image URLs and the sitemap.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyError, ValueError) as error:
        sys.exit(f"Configuration error: {error}")
