"""Write static search and social metadata from site-config.json."""
import json
import re
import sys
from html import escape, unescape
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
BEGIN = "<!-- BEGIN GENERATED SEARCH AND SOCIAL METADATA -->"
END = "<!-- END GENERATED SEARCH AND SOCIAL METADATA -->"
BLOCK = re.compile(re.escape(BEGIN) + ".*?" + re.escape(END), re.DOTALL)
PREVIEW = "images/social-preview.png"
PREVIEW_ALT = "White Armenian eternity mark above Ara Giulambarian and Senior Experience Designer on a black background."
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


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


def page_metadata(page, text, base_url):
    title = single(r"<title>([^<]+)</title>", text, "page title")
    description = single(r'<meta name="description" content="([^"]+)">', text, "description")
    page_type = "website"
    if page.parent == ROOT / "about":
        page_type = "profile"
    elif page.parent.parent == ROOT / "case-studies":
        page_type = "article"

    lines = [
        meta("property", "og:title", title),
        meta("property", "og:description", description),
        meta("property", "og:type", page_type),
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

    if page == ROOT / "index.html":
        person = {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": "Ara Giulambarian",
            "jobTitle": "Senior Experience Designer",
            "worksFor": {"@type": "Organization", "name": "Westpac"},
            "sameAs": ["https://www.linkedin.com/in/arglm/"],
        }
        if canonical:
            person.update({"@id": canonical + "#ara-giulambarian", "url": canonical})
        lines.append('<script type="application/ld+json">')
        lines.append(json.dumps(person, ensure_ascii=False, indent=2))
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
