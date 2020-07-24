from pathlib import Path

from aiohttp import web
import aiohttp_jinja2
import jinja2
import magic

@aiohttp_jinja2.template('gallery.html.jinja2')
async def handle(request):
    path = request.match_info.get('path', '')
    is_root = path == ''
    my_path = (request.app['root'] / path).resolve()
    try:
        my_path.relative_to(request.app['root'])
    except ValueError as e:
        return web.Response(text='not allowed', status=403)
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
        dirs.append((my_path / '..').relative_to(request.app['root']))
    for item in dir_items:
        rel_item = item.relative_to(request.app['root'])
        if item.is_dir():
            dirs.append(rel_item)
        #else:
        #    print(magic.from_file(str(item), mime=True))
        elif magic.from_file(str(item), mime=True) in request.app['imagetypes']:
            files.append({'file': rel_item, 'thumb': rel_item, 'type': 'Image'})
        elif magic.from_file(str(item), mime=True) in request.app['videotypes']:
            files.append({'file': rel_item, 'thumb': None, 'type': 'Video'})
    return {'dirs': dirs, 'files': files, 'gallery_name': gallery_name}

async def create_app(gallery_root=None):
    app = web.Application()
    app['root'] = Path(gallery_root).absolute() if gallery_root else Path().absolute()
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('spg', 'templates'))

    # https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types
    app['imagetypes'] =  ['image/apng', 'image/bmp', 'image/gif', 'image/x-icon', 'image/jpeg', 'image/png', 'image/svg+xml', 'image/webp']

    app['videotypes'] = ['video/mp4']

    app.add_routes([
        web.static('/pics', app['root']),
    ])
    app.add_routes([web.get('/{path:.*}', handle)])
    return app