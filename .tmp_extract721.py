import re, html, io, sys

raw = open('D:/Study-Notes/.tmp_gh721.html', encoding='utf-8', errors='replace').read()

# The GitHub issue body is embedded; the visible text we want appears as literal
# substrings (with the < etc. only appearing in the JSON-escaped copies).
t = html.unescape(raw)
# collapse the JSON-escaped duplicate by decoding \uXXXX in a copy
t2 = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), t)
t2 = html.unescape(t2)

out = []
def show(kw, ctx=200):
    for src, name in ((t, 'raw'), (t2, 'decoded')):
        i = src.find(kw)
        if i >= 0:
            out.append('== [%s] %s ==' % (name, kw))
            out.append(src[max(0, i-ctx):i+ctx].replace('\n', '\\n'))
            break
    else:
        out.append('== NOT FOUND: %s ==' % kw)

for kw in ['index.quark', 'quarkshare_list', '我的夸克分享', '我的PikPak分享',
           '大量目录路径实际不存在', 'Tacit0924', 'index.daily', 'index.video',
           'index.share', 'index.115']:
    show(kw)

# print all "- index.xxx.txt" bullet lines found
idx = sorted(set(re.findall(r'- ?index\.[a-z0-9]+\.txt[^\n\\]{0,120}', t2)))
out.append('== index bullets ==')
out.extend(idx)

open('/tmp/gh721_extract.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
