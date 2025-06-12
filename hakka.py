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


from ckiptagger import WS, POS
#from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger#, CkipNerChunker
#ws_driver  = CkipWordSegmenter(level=1)
#pos_driver = CkipPosTagger(level=1)
ws = WS("./data")
pos = POS("./data")

def pack_ws_pos_sentence(segmented_sent, tagged_sent):
   assert len(segmented_sent) == len(tagged_sent)
   res = []
   for word, tag in zip(segmented_sent, tagged_sent):
      res.append(f'{word}({tag})')
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

            segmented_sents  = ws([chinese])
            tagged_sents = pos(segmented_sents)
            row.insert(13, pack_ws_pos_sentence(segmented_sents[0], tagged_sents[0]))

            print('\t'.join(row))#[1:3] + row[11:14]  + row))#[:4], tsv[10])
            cw.writerow(row)#[1:3] + row[11:14] + row)#[:4], tsv[10])
    else:
        tsv.insert(10, tsv[10])

        hakka, chinese = search_hakka_chinese(sense=tsv[10])
        if chinese == '': continue

        tsv.insert(11, hakka)
        tsv.insert(12, chinese)
#       print(tsv[1], tsv[2], tsv[12])#hakka)

        segmented_sents  = ws([chinese])
        tagged_sents = pos(segmented_sents)
        tsv.insert(13, pack_ws_pos_sentence(segmented_sents[0], tagged_sents[0]))

        print('\t'.join(tsv))#[1:3] + tsv[11:14] + tsv))#[:4], tsv[10])
#       cw.writerow(tsv)
        cw.writerow(tsv)#[1:3] + tsv[11:14]  + tsv)#[:4], tsv[10])
