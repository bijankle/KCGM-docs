# KCGM docs

Project Library Downloader. A single HTML page that lists the project document register so you can search it, filter it, tick files and download them in a batch from SharePoint.

Open `index.html` in a browser. Nothing needs installing.

## Files

`index.html` is the built page with the register inside it.

`template.html` is the page without data. The register goes in at the `__DATA__` placeholder.

`build_data.py` reads the register workbook and builds `index.html` from `template.html`.

## Rebuilding with a newer register

Run this with the latest `2000 Project Document Register.xlsm`:

```
python build_data.py "2000 Project Document Register.xlsm"
```

It reads each document from the Doc Register sheet and finds its SharePoint folder by file name in the Team Site Export and Overflow sheets, taking the first match, the same rule the register uses. It writes `data.json` and a new `index.html` with the register inside. Only `index.html` needs committing.

## Ticking

The tick box in the column header unticks everything shown when anything shown is ticked. When nothing shown is ticked, it ticks everything shown.
