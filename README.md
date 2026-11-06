# Ara Giulambarian · GitHub Pages project

This static project includes the resume, About page, case studies index and five detail pages. Pages, styles, scripts, images and fonts are included. Serve the folder directly. The project needs no package installation, hosting build or backend.

## Set the public URL

1. Open `site-config.json`. Replace the `null` value of `base_url` with your exact public HTTPS Pages URL as a JSON string. Include the repository subpath if Pages gives you one. Use the URL shown in the repository's **Settings → Pages**, or the final HTTPS custom domain if you use one.
2. From the project folder, run `python3 configure-pages.py` with Python 3.9 or newer. This writes canonical URLs, absolute social preview URLs and Person identifiers into the HTML, adds the sitemap reference to `robots.txt`, and creates `sitemap.xml`. Rerun after changing the public URL or editing page titles or descriptions.
3. Publish the project files, including `.nojekyll`, from the folder containing `index.html`. In **Settings → Pages**, choose **Deploy from a branch**, select your publishing branch and choose **/ (root)** if you placed the files at the repository root. If you set up Pages before knowing the URL, perform steps 1 and 2 as soon as you have it, then upload the generated files to the publishing source.

Until `base_url` is set, the pages include static title, description and card metadata. The URL-dependent tags and sitemap are generated only after you supply a real URL.

## Check the published site

- Open the site in a signed-out browser and check Home, About, Case studies and a detail page. Open `images/social-preview.png` and `sitemap.xml` under the published site URL to confirm that both are publicly accessible.
- Add and verify a **URL-prefix** property in Google Search Console using the full Pages URL. Submit `sitemap.xml` in **Sitemaps** and use **URL Inspection** on Home and a case study to test the live URLs. You can request indexing there.
- Search crawlers read `robots.txt` from the domain root. For a project at a repository subpath, this project's `robots.txt` still includes its sitemap reference, but it is outside the crawler's standard robots location. If you control the host root, add the sitemap reference to its root robots file. Otherwise, submit the project sitemap directly in Search Console.
- Paste a published page URL into a social preview checker to confirm that its page title and the shared image render.

## Run locally

Run `python3 -m http.server 8000` from this folder and open `http://localhost:8000/`. All site navigation and bundled assets use relative paths. External references, email and phone links keep their original destinations.

## Files

- `index.html`, `about/index.html` and the six HTML files under `case-studies/` hold the visible content and metadata.
- `site.css`, `case-studies/cases.css` and `case-studies/cases.js` provide styling and interactions.
- `images/social-preview.png` is the 1200 × 630 PNG used for sharing. Fonts and their licences, portrait, case study imagery, logo and favicons are bundled.
- `site-config.json`, `configure-pages.py`, `robots.txt` and the generated `sitemap.xml` configure indexing and sharing. The Python script runs only when you configure metadata.
