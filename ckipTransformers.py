from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger#, CkipNerChunker

# Initialize drivers
ws_driver  = CkipWordSegmenter(level=1)
pos_driver = CkipPosTagger(level=1)
#ner_driver = CkipNerChunker(level=1)

# Input text
text = [
   '傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。',
#  '空白 也是可以的～',
]

# Run pipeline
ws  = ws_driver(text)
pos = pos_driver(ws)
#ner = ner_driver(text)

# Pack word segmentation and part-of-speech results
def pack_ws_pos_sentece(sentence_ws, sentence_pos):
   assert len(sentence_ws) == len(sentence_pos)
   res = []
   for word_ws, word_pos in zip(sentence_ws, sentence_pos):
      res.append(f'{word_ws}({word_pos})')
   return '\u3000'.join(res)

print(pack_ws_pos_sentece(ws[0], pos[0]))

# Show results
for sentence, sentence_ws, sentence_pos in zip(text, ws, pos):#, ner):
   continue
   print(sentence)
   print(pack_ws_pos_sentece(sentence_ws, sentence_pos))
#  for entity in sentence_ner:
#     print(entity)
   print()

