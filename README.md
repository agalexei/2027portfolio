# Ara Giulambarian portfolio

`index.html` is the homepage. `about/` and `resume/` contain the About and Résumé pages. `work/` contains the work index and six case studies, with the CIANSW redesign first. `assets/` contains stylesheets, the font, illustrations, screenshots, full comparison SVGs and the résumé PDF.

## Run locally

1. Extract the ZIP into a folder.
2. Open a terminal in the folder containing `index.html` and run:

   ```sh
   python3 -m http.server 8000 --bind 127.0.0.1
   ```

3. Open http://127.0.0.1:8000/ in a browser. Use Ctrl+C in the terminal to stop the server.

The included HTML and CSS are both the editable source and the runnable site. This command uses Python 3. The site needs no build, package installation, environment variables or backend. It can also be served by any static web server that uses `index.html` as its directory index.

Internal links and assets are relative. External links and absolute canonical and social metadata retain their original destinations. The archive includes the preview's search-indexing directives. Access control is provided by the host when deployed separately.
