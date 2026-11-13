NONE = 'alleroed faxe gentofte herlev hoersholm kolding odder syddjurs varde vejen horsens thisted fredensborg vallensbaek ikastbrande herning ringkoebingskjern egedal struer frederikshavn frederikssund klimaraadet dyrenesbeskyttelse ms'.split()
KEEP = 'au bornsvilkar djoef dlf dm dsr dtu finansforbundet ida koebenhavn frederiksberg moedrehjaelpen roedekors sind wwf hk bupl foa prosa ruc ucn'.split()
H0 = '''aalborg aarhus albertslund assens ballerup bornholm broendby broenderslev dakofa dn dragoer esbjerg faaborgmidtfyn fanoe favrskov
furesoe gladsaxe glostrup greve gribskov haderslev halsnaes hedensted helsingoer hilleroed hoejetaastrup holbaek holstebro hvidovre ishoej
jammerbugt kerteminde koege kraeftensbekaempelse ku laesoe langeland lejre lemvig lolland middelfart naestved noedhjaelp norddjurs nordfyn
nyborg odense odsherred rebild redbarnet ringsted roskilde rudersdal samsoe silkeborg skanderborg solroed soroe stevns svendborg toender vejle
vesthimmerland via viborg flygtningehjaelp cbs'''.split()
S = {s: [('H', 0)] for s in H0}
S.update({
 'aabenraa': [('H', 1)], 'fredericia': [('H', 1)], 'kalundborg': [('H', 1)], 'morsoe': [('box', 300, 25, 517, 253)], 'randers': [('H', 2)], 'diabetes': [('H', 3)],
 '3f': [('V', 0)], 'aau': [('V', 0)], 'dj': [('V', 0)], 'handicap': [('V', 0)], 'guldborgsund': [('V', 0)], 'hjoerring': [('V', 0)],
 'skive': [('V', 0)], 'slagelse': [('V', 0)], 'soenderborg': [('V', 0)],
 'hjerteforeningen': [('H', 0), ('V', 1)], 'roedovre': [('box', 21, 21, 280, 296)],
 'lyngbytaarbaek': [('Hr', 0, 1)], 'sdu': [('Hr', 0, 2)],
 'aeldresagen': [('box', 262, 0, 376, 112)], 'taarnby': [('box', 20, 20, 168, 192)], 'vordingborg': [('box', 268, 84, 416, 282)],
 'billund': [('box', 20, 98, 247, 368)], 'msf': [('box', 0, 0, 245, 191), ('redonly',), ('erase', 150, 140, 245, 191)],
 'absalon': [('tile', 112, 338, 356, 582)], 'amnesty': [('tile', 368, 67, 528, 227)], 'grl-rep': [('tile', 78, 88, 270, 322)],
 'kirkenskorshaer': [('tile', 50, 50, 160, 160)], 'mariagerfjord': [('tile', 25, 25, 308, 308)], 'unicef': [('tile', 414, 74, 570, 216)],
 'itu': [('txt', 'ITU', '#ffffff', '#000000')], 'kp': [('txt', 'KP', '#ffffff', None)],
})
