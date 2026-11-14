import requests, re

url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
# urlLetterF = "https://docs.google.com/document/u/0/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub?pli=1"

# Get the table from Google Doc, remove the irrelevant and only keep what we need
table = requests.get(url).text
table = re.sub(r"<script\b[^>]*>.*?</script>", "", table, flags=re.S | re.I)
table = re.sub(r"<style\b[^>]*>.*?</style>", "", table, flags=re.S | re.I)
 
infos = re.sub(r"<[^>]+>", "\n", table)
info = [l.strip() for l in infos.splitlines() if l.strip()]
   
# in case y-coordinate is missing
try:
    s = info.index("y-coordinate") + 1
except ValueError:
    print("miss the y-coordinate,")
    for l in info[:30]:
        print(repr(l))
    raise SystemExit
     
# group every 3 
groups = []
i = s
while i + 2 < len(info):
    try:
        x = int(info[i])
        p = info[i+1]
        y = int(info[i+2])
        
        if len(p) == 1: # skip when not a char
            groups.append((x, y, p))
            i += 3
        else:
            i += 1
    except ValueError:
        i += 1
         
# find the numbers of column and row       
col = max(c[0] for c in groups) + 1
row = max(c[1] for c in groups) + 1
   
result = [[" "] * col for _ in range(row)]
 
# x-coordinate, y-coordinate mapping
for x, y, p in groups:
    result[y][x] = p
     
# print out the pattern
for ii in reversed(result):
    print("".join(ii))

