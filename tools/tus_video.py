"""Video üstüne tuş görseli bindirir.
Kullanım: python3 tus_video.py giris.mp4 cikis.mp4 segmentler.json [platform]
segmentler.json: [{"t0":9.4,"t1":12.9,"spec":"triangle@2","label":"MOTOR AÇIK KALIR","dim":[],"fi":true,"fo":true,"y":1070}, ...]
"""
import sys, json, subprocess, asyncio, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tus import overlay_html
from playwright.async_api import async_playwright

async def render(segs, platform, d):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(viewport={'width': 1080, 'height': 700}, device_scale_factor=1.2)
        for i, s in enumerate(segs):
            html = ('<html><body style="margin:0;background:transparent">'
                    + overlay_html(s['spec'], s.get('label'), platform, tuple(s.get('dim', []))) + '</body></html>')
            await pg.set_content(html)
            await pg.wait_for_timeout(150)
            await pg.locator('#ov').screenshot(path=f'{d}/o{i}.png', omit_background=True)
        await b.close()

def main():
    src, dst, jf = sys.argv[1:4]
    platform = sys.argv[4] if len(sys.argv) > 4 else 'ps'
    segs = json.load(open(jf))
    d = tempfile.mkdtemp()
    asyncio.run(render(segs, platform, d))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', src]
    for i, s in enumerate(segs):
        cmd += ['-loop', '1', '-framerate', '60', '-t', str(s['t1'] - s['t0']), '-i', f'{d}/o{i}.png']
    fc, last = [], '0:v'
    for i, s in enumerate(segs):
        dur = s['t1'] - s['t0']
        f = f'[{i+1}:v]format=rgba'
        if s.get('fi', True): f += ',fade=t=in:st=0:d=0.2:alpha=1'
        if s.get('fo', True): f += f',fade=t=out:st={dur-0.2:.2f}:d=0.2:alpha=1'
        f += f',setpts=PTS+{s["t0"]}/TB[o{i}]'
        fc.append(f)
        fc.append(f'[{last}][o{i}]overlay=x=(W-w)/2:y={s.get("y",1070)}:eof_action=pass[v{i}]')
        last = f'v{i}'
    cmd += ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-map', '0:a?', '-c:v', 'libx264', '-preset', 'veryfast',
            '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy', dst]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    main()
