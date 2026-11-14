import csv, json, re, collections
R=lambda f: list(csv.DictReader(open(f+'.csv',encoding='utf-8')))
EN='9'
types={r['id']:r['identifier'].capitalize() for r in R('types')}
sp={r['id']:r for r in R('pokemon_species')}
spname={r['pokemon_species_id']:r['name'] for r in R('pokemon_species_names') if r['local_language_id']==EN}
formname={}
fid2pid={r['id']:r['pokemon_id'] for r in R('pokemon_forms')}
for r in R('pokemon_form_names'):
    if r['local_language_id']==EN and r['pokemon_name']: formname[fid2pid.get(r['pokemon_form_id'])]=r['pokemon_name']
pk=R('pokemon')
REG=re.compile(r'-(alola|galar|hisui|paldea)')
keep=[]
for p in pk:
    if p['is_default']=='1': keep.append(p)
    elif REG.search(p['identifier']) and not re.search(r'totem|cap|zen',p['identifier']): keep.append(p)
kid={p['id'] for p in keep}
ptypes=collections.defaultdict(list)
for r in R('pokemon_types'):
    if r['pokemon_id'] in kid: ptypes[r['pokemon_id']].append((int(r['slot']),types[r['type_id']]))
pab=collections.defaultdict(list)
for r in R('pokemon_abilities'):
    if r['pokemon_id'] in kid and r['is_hidden']=='0': pab[r['pokemon_id']].append(int(r['ability_id']))
stats=collections.defaultdict(lambda:[0]*6)
for r in R('pokemon_stats'):
    if r['pokemon_id'] in kid and int(r['stat_id'])<=6: stats[r['pokemon_id']][int(r['stat_id'])-1]=int(r['base_stat'])
EXCL={'12','13','28','29'}
PREF=['18','17','25','20','23','16','15','14','11','10','9','24','30','31','32']
lv=collections.defaultdict(lambda:collections.defaultdict(list)); pool=collections.defaultdict(set)
for r in csv.DictReader(open('pokemon_moves.csv')):
    p=r['pokemon_id']
    if p not in kid or r['version_group_id'] in EXCL or int(r['move_id'])>=10000: continue
    m=int(r['move_id']); pool[p].add(m)
    if r['pokemon_move_method_id']=='1': lv[p][r['version_group_id']].append((int(r['level'] or 0),m))
abil_used=set(); move_used=set(); out=[]
for p in keep:
    s=sp[p['species_id']]; pid=p['id']
    vg=next((v for v in PREF if v in lv[pid]),None)
    L=sorted(set(lv[pid][vg])) if vg else []
    start=sorted({m for l,m in L if l==1}, key=lambda m:[x for x in L if x[1]==m][0])
    lvl=[[l,m] for l,m in L if l>=1]
    name=formname.get(pid) if p['is_default']!='1' else None
    name=name or spname[p['species_id']]
    leg=2 if s['is_mythical']=='1' else 1 if s['is_legendary']=='1' else 0
    t=[x for _,x in sorted(ptypes[pid])]
    move_used|=pool[pid]; abil_used|=set(pab[pid])
    out.append({'i':int(pid),'s':int(s['id']),'n':name,'t':t,'f':int(s['evolves_from_species_id'] or 0),'b':int(s['is_baby']),'g':leg,
      'r':1 if p['is_default']!='1' else 0,'a':pab[pid],'bs':stats[pid],'st':start,'lv':lvl,
      'p':sorted(pool[pid])})
# moves
mn={r['move_id']:r['name'] for r in R('move_names') if r['local_language_id']==EN}
mft={}
for r in csv.DictReader(open('move_flavor_text.csv',encoding='utf-8')):
    if r['language_id']==EN and 'be used' not in r['flavor_text'] and int(r['version_group_id'])>=mft.get(r['move_id'],(0,''))[0]: mft[r['move_id']]=(int(r['version_group_id']),r['flavor_text'])
cls={'1':'Status','2':'Physical','3':'Special'}
moves={}
for r in R('moves'):
    m=int(r['id'])
    if m not in move_used: continue
    d=re.sub(r'\s+',' ',mft.get(r['id'],(0,''))[1].replace('­','')).strip()
    moves[m]=[mn.get(r['id'],r['identifier']),types[r['type_id']],int(r['power']) if r['power'] else 0,int(r['accuracy']) if r['accuracy'] else 0,cls[r['damage_class_id']],d]
an={r['ability_id']:r['name'] for r in R('ability_names') if r['local_language_id']==EN}
aft={}
for r in csv.DictReader(open('ability_flavor_text.csv',encoding='utf-8')):
    if r['language_id']==EN: aft[r['ability_id']]=re.sub(r'\s+',' ',r['flavor_text'].replace('­','')).strip()
abil={a:[an.get(str(a),str(a)),aft.get(str(a),'')] for a in abil_used}
js='window.PMD_DATA='+json.dumps({'pk':out,'mv':moves,'ab':abil},ensure_ascii=False,separators=(',',':'))+';'
open('data.js','w',encoding='utf-8').write(js)
print(len(out),len(moves),len(abil),len(js))
