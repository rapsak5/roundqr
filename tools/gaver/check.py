import sys, asyncio
from playwright.async_api import async_playwright
async def main(files):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for f in files:
            pg = await b.new_page(viewport={'width':390,'height':900}, device_scale_factor=1)
            errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('file://'+f); await pg.wait_for_timeout(2500)
            sw = await pg.evaluate('document.documentElement.scrollWidth')
            txt = await pg.evaluate('document.body.innerText')
            ok = 'Kan scannes' in txt
            name=f.split('/')[-1]
            await pg.screenshot(path='/home/claude/gaver/test/'+name.replace('.html','.png'), full_page=False)
            print(name, 'scrollW', sw, 'scan', ok, 'errs', errs[:2])
            await pg.close()
        await b.close()
asyncio.run(main(sys.argv[1:]))
