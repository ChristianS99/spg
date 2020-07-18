#!/usr/bin/python
from argparse import ArgumentParser
from pathlib import Path

from aiohttp import web
import aiohttp_jinja2
import jinja2
import magic

parser = ArgumentParser('Serve some folder as image/video gallery')
parser.add_argument('root', nargs='?', help='location, where files should be served from')
parser.add_argument('--host')
parser.add_argument('--port', '-p', type=int)

args = parser.parse_args()
root = Path(args.root) if args.root else Path().absolute()

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(Path(__file__).parent / 'templates'))

# https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types
imagetypes =  ['image/apng', 'image/bmp', 'image/gif', 'image/x-icon', 'image/jpeg', 'image/png', 'image/svg+xml', 'image/webp']

videotypes = ['video/mp4']

@aiohttp_jinja2.template('gallery.html.jinja2')
async def handle(request):
    path = request.match_info.get('path', '')
    is_root = path == ''
    my_path = Path(root / path)
    gallery_name = my_path.name
    try:
        dir_items = my_path.iterdir()
        dir_items = [item for item in dir_items]
        dir_items.sort(key=lambda i: str(i).casefold())
    except FileNotFoundError as e:
        return web.Response(text='no such directory', status=404)
    dirs = []
    files = []
    if not is_root:
        dirs.append((my_path / '..').relative_to(root))
    for item in dir_items:
        rel_item = item.relative_to(root)
        if item.is_dir():
            dirs.append(rel_item)
        #else:
        #    print(magic.from_file(str(item), mime=True))
        elif magic.from_file(str(item), mime=True) in imagetypes:
            files.append({ 'file': rel_item, 'thumb': rel_item, 'type': 'Image' })
        elif magic.from_file(str(item), mime=True) in imagetypes + videotypes:
            files.append({ 'file': rel_item, 'thumb': None, 'type': 'Video' })
    return {'dirs': dirs, 'files': files, 'gallery_name': gallery_name}

app.add_routes([
    web.static('/pics', root), 
])
app.add_routes([web.get('/{path:.*}', handle)])

if __name__ == '__main__':
    web.run_app(app, host=args.host, port=args.port)
