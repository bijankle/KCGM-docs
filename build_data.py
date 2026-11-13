"""Build the app's register from the 2000 Project Document Register workbook.

Usage: python build_data.py "2000 Project Document Register.xlsm"

Reads the "Doc Register" sheet for each document (file name, doc number, rev,
status, title) and the "Team Site Export" and "Overflow" sheets for where each
file lives on SharePoint and its size in bytes. A document's link is the first file in the export
with the same name, the same rule the register itself uses. Writes data.json,
then builds index.html from template.html with the data inside it.
"""
import json
import os
import sys

import openpyxl

SITE = "https://nsrltd.sharepoint.com/"


def text(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip()


def sheet_rows(wb, name, stop_after_blank=2000):
    """Rows of a sheet, stopping after a long run of blank rows (the sheets are formatted far past the data)."""
    blank = 0
    for r in wb[name].iter_rows(values_only=True):
        if all(v in (None, "") for v in r):
            blank += 1
            if blank > stop_after_blank:
                return
            continue
        blank = 0
        yield r


def main(src):
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)

    # SharePoint export: column A is the file name (sometimes a full link), column K the folder path.
    where = {}
    for sheet in ("Team Site Export", "Overflow"):
        for i, r in enumerate(sheet_rows(wb, sheet)):
            if sheet == "Team Site Export" and i == 0:
                continue  # header row
            name, path = text(r[0]), text(r[10] if len(r) > 10 else "")
            if not name or not path:
                continue
            if name.startswith("http"):
                name = name.rsplit("/", 1)[1].replace("%20", " ")
            try:
                size = int(float(text(r[3]) or 0))
            except ValueError:
                size = 0
            where.setdefault(name.lower(), (path, size))  # first match wins

    folders, F, out = {}, [], []
    for i, r in enumerate(sheet_rows(wb, "Doc Register")):
        if i == 0:
            continue  # header row
        name, num, rev, st, title = text(r[0]), text(r[2]), text(r[3]), text(r[4]), text(r[5])
        if not (name or num):
            continue
        fi = -1
        path, size = where.get(name.lower(), (None, 0)) if name else (None, 0)
        if path:
            folder = SITE + path
            if folder not in folders:
                folders[folder] = len(F)
                F.append(folder)
            fi = folders[folder]
        out.append([name, fi, "", num, rev, st, title, size])

    data = {"folders": F, "rows": out, "source": os.path.basename(src)}
    packed = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(packed)
    with open("template.html", encoding="utf-8") as f:
        page = f.read()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(page.replace("__DATA__", packed.replace("</", "<\\/"), 1))
    linked = sum(1 for x in out if x[1] >= 0)
    print(f"{len(out)} rows, {linked} with a link, {len(F)} folders, data.json {os.path.getsize('data.json'):,} bytes")


if __name__ == "__main__":
    main(sys.argv[1])
