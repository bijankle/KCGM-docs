# KCGM docs

Project Library Downloader. A single HTML page that lists the project document register so you can search it, filter it, tick files and download them in a batch from SharePoint.

Open `index.html` in a browser. Nothing needs installing.

## Files

`index.html` is the built page with the register inside it.

`template.html` is the page without data. The register goes in at the `__DATA__` placeholder.

`build_data.py` packs the register xlsm into compact JSON.

## Rebuilding with a newer register

Run `build_data.py` on the xlsm to make `data.json`. Then replace `__DATA__` in `template.html` with the contents of `data.json`, escaping `</` as `<\/`, and save the result as `index.html`.

You can also load a newer xlsm or csv straight into the page with the Update register button. That copy is kept in your browser only.

## Ticking

The tick box in the column header unticks everything shown when anything shown is ticked. When nothing shown is ticked, it ticks everything shown.
