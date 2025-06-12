from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger#, CkipNerChunker
ws_driver  = CkipWordSegmenter(level=1)
pos_driver = CkipPosTagger(level=1)

def pack_ws_pos_sentece(sentence_ws, sentence_pos):
   assert len(sentence_ws) == len(sentence_pos)
   res = []
   for word_ws, word_pos in zip(sentence_ws, sentence_pos):
      res.append(f'{word_ws}({word_pos})')
   return '\u3000'.join(res)


import sys
MOEmin_filename = sys.argv[1]
for line in open(MOEmin_filename):
    min, chinese = line.split('\t')
    chinese = chinese[1:-2]

    ws  = ws_driver([chinese])
    pos = pos_driver(ws)
    print(min, chinese, pack_ws_pos_sentece(ws[0], pos[0]), sep='\t')
