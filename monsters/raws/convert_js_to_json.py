import glob
import json
from multiprocessing.pool import Pool

import demjson

# from
paths = [path for path in glob.glob('js/*.js')]
print(paths)
contents = [open(path).read() for path in paths]
javascript = [content[content.find('{'):content.rfind('}')+1] for content in contents]
p = Pool(8)
dicts = p.map(demjson.decode,javascript)
for path,d in zip(paths,dicts):
    with open(path.replace('js','json'),'wb') as f:
        f.write(json.dumps(d).encode('utf-8'))
