'''
Convert glyphwiki.svg to png files
'''
import argparse
import cairosvg
import base64
import os

INPUT_PATH = '../glyphwiki.svg'
WIDTH = 400
HEIGHT = 400
SVG_STR_WRAPPER_PRO = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" baseProfile="full" viewBox="0 0 200 200" width="{WIDTH}" height="{HEIGHT}">\n<g fill="black">\n<path d="'
SVG_STR_WRAPPER_POST = '"/>\n</g>\n</svg>'

def check_and_create_folder(folder):
    if not os.path.isdir(folder):
        print(f'folder {folder} does not exist, creating ...')
        try:
            os.makedirs(folder, exist_ok=True)
        except:
            print(f'Cannot create folder {folder}.')
            return

def wrap_svg_str(svg_raw):
    return SVG_STR_WRAPPER_PRO + svg_raw + SVG_STR_WRAPPER_POST

def load_and_convert(output):

    check_and_create_folder(os.path.join(output, 'png'))
    check_and_create_folder(os.path.join(output, 'svg'))

    with open(INPUT_PATH, 'r') as f:
        lines = f.readlines()

    print('Start converting and saving png and svg files.')

    for line in lines:
        line_splitted = line.split()
        unicode_char = line_splitted[0]
        svg_raw = base64.b64decode(line_splitted[1].encode('ascii')).decode('ascii')
        bytestring = wrap_svg_str(svg_raw)
        unicode_hex = str(hex(ord(unicode_char)))[2:]
        cairosvg.surface.PNGSurface.convert(bytestring=bytestring, width=WIDTH, height=HEIGHT, write_to=open(os.path.join(output, 'png', unicode_hex + '.png'), 'wb'))
        with open(os.path.join(output, 'svg', unicode_hex + '.svg'), 'w') as f:
            f.write(bytestring)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default = './test', help='output folder of png files')
    args = parser.parse_args()

    load_and_convert(args.output)
