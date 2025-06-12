import sys
filename = sys.argv[1]
lines = open(filename)

import csv
cr = csv.reader(lines, delimiter='\t')
headers = next(cr)
headers.insert(10, 'sense')
headers.insert(11, 'hakka')
headers.insert(12, 'chinese')
headers.insert(13, 'chinese_ws_pos')
print('\t'.join(headers))#[1:3] + headers[11:14] + headers))

#cw = csv.writer(open(filename + '_每條詞意一行.tsv', 'w'), delimiter='\t')
#cw = csv.writer(open(filename + '_每條詞意一行_僅中文平行例句.tsv', 'w'), delimiter='\t')
cw = csv.writer(open(filename + '_每條詞意一行_僅中文平行例句_加斷詞詞類.tsv', 'w'), delimiter='\t')
cw.writerow(headers)#[1:3] + headers[11:14] + headers)

def search_hakka_chinese(sense):
    hakka=""
    chinese=""
    m = re.search(pattern="例：(?P<hakka>.*)", string=sense)
    if m: 
        hakka = m.group('hakka')
        n = re.search(pattern="例：(?P<hakka>.*)（(?P<chinese>.*)）", string=sense)
        if n: 
            hakka = n.group('hakka')
            chinese = n.group('chinese')
    return hakka, chinese


from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger#, CkipNerChunker
ws_driver  = CkipWordSegmenter(level=1)
pos_driver = CkipPosTagger(level=1)

def pack_ws_pos_sentece(sentence_ws, sentence_pos):
   assert len(sentence_ws) == len(sentence_pos)
   res = []
   for word_ws, word_pos in zip(sentence_ws, sentence_pos):
      res.append(f'{word_ws}({word_pos})')
   return '\u3000'.join(res)


import re, copy
for tsv in cr:
    if tsv[10].startswith('1.'):
        senses = re.split(pattern='\d\.', string=tsv[10])[1:]
        for i in range(len(senses)):
            row = copy.copy(tsv)
            row.insert(10, str(i+1)+'.'+senses[i])

            hakka, chinese = search_hakka_chinese(sense=senses[i])
            if chinese == '': continue

            row.insert(11, hakka)
            row.insert(12, chinese)
#           print(row[1], row[2], row[12])#hakka)

            ws  = ws_driver([chinese])
            pos = pos_driver(ws)
            row.insert(13, pack_ws_pos_sentece(ws[0], pos[0]))

            print('\t'.join(row))#[1:3] + row[11:14]  + row))#[:4], tsv[10])
            cw.writerow(row)#[1:3] + row[11:14] + row)#[:4], tsv[10])
    else:
        tsv.insert(10, tsv[10])

        hakka, chinese = search_hakka_chinese(sense=tsv[10])
        if chinese == '': continue

        tsv.insert(11, hakka)
        tsv.insert(12, chinese)
#       print(tsv[1], tsv[2], tsv[12])#hakka)

        ws  = ws_driver([chinese])
        pos = pos_driver(ws)
        tsv.insert(13, pack_ws_pos_sentece(ws[0], pos[0]))

        print('\t'.join(tsv))#[1:3] + tsv[11:14] + tsv))#[:4], tsv[10])
#       cw.writerow(tsv)
        cw.writerow(tsv)#[1:3] + tsv[11:14]  + tsv)#[:4], tsv[10])
