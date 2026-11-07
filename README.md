# Ara Giulambarian · Portfolio

This static project includes the resume, About page, case studies index and six detail pages. Pages, styles, scripts, images and fonts are included. Serve the folder directly. The project needs no package installation, hosting build or backend.

## Merge the search update

Extract the ZIP and copy its contents into the existing project folder that contains `index.html`. Let the included files replace their counterparts. This is a changes-only ZIP. Keep the existing images, fonts, scripts and other assets in place.

The included search files are ready for `https://agalexei.github.io/2027portfolio/`. Run the local preview below to check the merged project, then publish it using your existing workflow.

## Change the public URL

1. When the custom domain is ready, set `base_url` in `site-config.json` to the exact public HTTPS URL. Include a subpath only if the site is hosted in one.
2. From the project folder, run `python3 configure-pages.py` with Python 3.9 or newer. This regenerates canonical URLs, structured data, social preview URLs, `robots.txt` and `sitemap.xml`. Rerun it after changing titles, descriptions, case study headings or cover paths.
3. Publish the generated files along with the site. When your host supports it, verify each old page URL permanently redirects to its corresponding new page. Verify the new domain in Google Search Console and Bing Webmaster Tools, then submit the new sitemap in both.

## Check the published site

- Open the site in a signed-out browser and check Home, About, Case studies and a detail page. Open `images/social-preview.png` and `sitemap.xml` under the published site URL to confirm that both are publicly accessible.
- Add and verify a **URL-prefix** property in Google Search Console using the full Pages URL. Submit `sitemap.xml` in **Sitemaps** and use **URL Inspection** on Home and a case study to test the live URLs. You can request indexing there.
- Search crawlers read `robots.txt` from the domain root. When the portfolio is served under a subpath, submit the sitemap directly and check crawl rules on the host’s root `robots.txt`. On the custom domain, make sure the root rules and your host allow `OAI-SearchBot` to reach public pages for ChatGPT Search.
- Check About and a case study in Google’s Rich Results Test. The About page describes Ara’s profile, and each case study points to the same author profile.
- In Search Console, monitor name, role and project queries separately. Use Bing Webmaster Tools’ AI Performance report for citation data when available.
- Paste a published page URL into a social preview checker to confirm that its page title and the shared image render.

## Run locally

Run `python3 -m http.server 8000` from this folder and open `http://localhost:8000/`. All site navigation and bundled assets use relative paths. External references, email and phone links keep their original destinations.

## Files

- `index.html`, `about/index.html`, `case-studies/index.html` and the six project detail pages hold the visible content and metadata.
- `site.css`, `case-studies/cases.css` and `case-studies/cases.js` provide styling and interactions.
- `images/social-preview.png` is the 1200 × 630 PNG used for sharing. Fonts and their licences, portrait, case study imagery, logo and favicons are bundled.
- `site-config.json`, `configure-pages.py`, `robots.txt` and the generated `sitemap.xml` configure indexing and sharing. The Python script runs only when you configure metadata.
