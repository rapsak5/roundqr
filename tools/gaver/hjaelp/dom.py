import sys
from PIL import Image
from collections import Counter
im=Image.open(sys.argv[1]).convert('RGB'); c=Counter(im.getdata())
print([('#%02x%02x%02x'%k,v) for k,v in c.most_common(6) if sum(k)<700][:3])
