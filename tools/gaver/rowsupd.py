#!/usr/bin/env python3
"""Laver batchUpdate-forespørgsler til kommunearket. Input: JSON-liste med
[række, Kanal, Organisation, Modtagere, Hilsen, Rolle, Til, Cc, Noter, Kilde] (valgfrit: Status, Næste skridt).
Skriver aldrig i M, N, S eller T (formler). Udskriver JSON til Google Sheets update_spreadsheet (requests)."""
import json, sys
rows = json.load(open(sys.argv[1])); req = []
def cell(r, c, vals): req.append({'updateCells': {'start': {'sheetId': 0, 'rowIndex': r - 1, 'columnIndex': c}, 'rows': [{'values': [{'userEnteredValue': {'stringValue': v}} for v in vals]}], 'fields': 'userEnteredValue'}})
for r in rows:
    row = r[0]; cell(row, 0, r[1:8] + ['nej']); cell(row, 16, [r[10] if len(r) > 10 else 'Venter på side'])
    cell(row, 21, [r[11] if len(r) > 11 else 'Byg siden', '', r[8], r[9]])
print(json.dumps(req, ensure_ascii=False))
