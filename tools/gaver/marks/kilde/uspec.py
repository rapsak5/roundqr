NONE = ['cardiff', 'manchester']
KEEP = ['kth', 'ucd']
S = {s: [('H', 0)] for s in 'bangor bristol edinburgh galway lund maynooth sheffield standrews tcd'.split()}
S.update({
 'dcu': [('Hr', 0, 1)],
 'aberdeen': [('box', 20, 64, 182, 260)], 'aberystwyth': [('box', 14, 33, 99, 131)],
 'glasgow': [('tile', 42, 42, 240, 323)], 'leeds': [('tile', 32, 32, 140, 140)], 'limerick': [('tile', 24, 26, 188, 272)],
 'newcastle': [('tile', 30, 28, 176, 208)], 'nottingham': [('tile', 41, 41, 232, 232)], 'stockholm': [('tile', 30, 30, 241, 236)],
 'strathclyde': [('tile', 44, 40, 332, 316)], 'swansea': [('tile', 6, 6, 122, 156)], 'ucc': [('tile', 44, 52, 136, 146)],
 'uppsala': [('tile', 29, 0, 117, 88)],
})
