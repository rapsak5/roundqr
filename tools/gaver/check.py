import sys, asyncio, re
from playwright.async_api import async_playwright
# Tjekker hver side ved 390 px: ingen vandret scroll, og QR-koden kan scannes (pillen har klassen ok, så det virker på alle sprog).
# Sider med sprogvælger tjekkes på hvert sprog, og der meldes, hvis der står danske ord på en side, der ikke er dansk.
DANSK = re.compile(r'\b(Vælg|Kan scannes|Gem |Udseende|Farvesæt|Hent programmet|Udviklet af|Tekst under koden|Fejlkorrektion)\b')
async def main(files):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for f in files:
            pg = await b.new_page(viewport={'width': 390, 'height': 900}, device_scale_factor=1)
            errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('file://' + f); await pg.wait_for_timeout(2500)
            langs = await pg.evaluate('Array.from(document.querySelectorAll(\'input[name="lang"]\')).map(e => e.value)')
            name = f.rstrip('/').split('/')[-2] if f.endswith('index.html') else f.split('/')[-1]
            for i, lg in enumerate(langs or [None]):
                if lg:
                    await pg.evaluate('v => { const e = document.querySelector(\'input[name="lang"][value="\' + v + \'"]\'); e.checked = true; e.dispatchEvent(new Event("change")); }', lg)
                    await pg.wait_for_timeout(1500)
                sw = await pg.evaluate('document.documentElement.scrollWidth')
                ok = await pg.evaluate('document.getElementById("scan").classList.contains("ok")')
                pill = await pg.evaluate('document.getElementById("scan").textContent')
                hl = await pg.evaluate('document.documentElement.lang')
                txt = await pg.evaluate('document.body.innerText')
                da = sorted(set(DANSK.findall(txt))) if hl != 'da' else []
                await pg.screenshot(path='/home/claude/gaver/test/%s-%s.png' % (name, lg or 'da'), full_page=False)
                print(name, lg or '', 'lang', hl, 'scrollW', sw, 'scan', ok, repr(pill), 'dansk', da, 'errs', errs[:2])
            await pg.close()
        await b.close()
asyncio.run(main(sys.argv[1:]))
