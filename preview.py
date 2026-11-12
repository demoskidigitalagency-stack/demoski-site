import re,os,shutil
src,dst='dist','preview'
if os.path.exists(dst): shutil.rmtree(dst)
shutil.copytree(src,dst)
for root,_,files in os.walk(dst):
    for f in files:
        if not f.endswith('.html'): continue
        p=os.path.join(root,f); pre='' if root==dst else '../'
        def fix(m):
            path=m.group(2)
            if path=='' or path.endswith('/'): path+='index.html'
            return '%s="%s%s"'%(m.group(1),pre,path)
        s=open(p,encoding='utf-8').read()
        s=re.sub(r'(href|src)="/([^"/][^"]*|)"',fix,s)
        if root==dst:
            head=re.search(r'<head>(.*?)</head>',s,re.S).group(1)
            keep=''.join(re.findall(r'<link rel="stylesheet"[^>]*>',head))
            body=re.search(r'<body[^>]*>(.*)</body>',s,re.S).group(1)
            s='<title>Demoski Live Account</title><meta name="claude:viewport-fit-sides" content="cover">'+keep+body
        open(p,'w',encoding='utf-8').write(s)
