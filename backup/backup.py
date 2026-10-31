import json,os,re,urllib.request,hashlib
U='https://pbkrwghuwqufosodcxtw.supabase.co';K='sb_publishable_bzFGyPbxFyfgU4CQ72ryuQ_S4vwUvt2'
req=urllib.request.Request(U+'/rest/v1/posts?select=*&published=eq.true&order=created_at.desc',headers={'apikey':K})
posts=json.load(urllib.request.urlopen(req))
os.makedirs('backup/images',exist_ok=True);imgs={}
for p in posts:
  m=re.match(r'^<!--tags:(.*?)-->\n?',p.get('body') or '');p['tags']=[t.strip() for t in m.group(1).split(',') if t.strip()] if m else []
  for url in re.findall(r'!\[.*?\]\((https://[^\s)]+)\)',p.get('body') or ''):
    name=hashlib.sha1(url.encode()).hexdigest()[:10]+'-'+url.rsplit('/',1)[-1][:80];path='backup/images/'+name;imgs[url]=path
    if not os.path.exists(path):
      try:open(path,'wb').write(urllib.request.urlopen(url).read())
      except Exception as e:print('image failed',url,e)
json.dump({'posts':posts,'images':imgs},open('backup/posts.json','w'),indent=2,ensure_ascii=False)
print(len(posts),'posts',len(imgs),'images')
