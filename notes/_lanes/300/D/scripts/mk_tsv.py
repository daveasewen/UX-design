import re
PRJ='/projects/01a0a457-df26-7151-80c8-7d2f74bf7c97/'
L=open('snap_18.txt').read().split('\n'); lst=L[28:178]
snap={}
for l in lst:
    p,rest=l.split(' ',1)
    src=';'.join(re.findall(r'\[sources: ([^\]]*)\]',rest)); al=';'.join(re.findall(r'\[aliases: ([^\]]*)\]',rest))
    desc=rest.split(' — ',1)[1] if ' — ' in rest else ''
    snap[p]=(src,al,desc.replace('\t',' '))
rows=[l.split('\t') for l in open('store_listing.tsv').read().strip().split('\n')]
with open('/mnt/user-data/outputs/D-store-census.tsv','w') as o:
    o.write('scope\trel_path\tbytes\tupdated\tin_boot_snapshot\tsource_tag\taliases\tsnapshot_description\n')
    for p,b,u in rows:
        scope='project' if p.startswith(PRJ) else 'account'
        rel=p.replace(PRJ,'') if scope=='project' else p
        s=snap.get(p,('','',''))
        o.write(f'{scope}\t{rel}\t{b}\t{u[:19]}\t{1 if p in snap else 0}\t{s[0]}\t{s[1]}\t{s[2]}\n')
# listing-only file (no profile/preferences) for the device
open('/mnt/user-data/outputs/D-boot-snapshot-listing.txt','w').write('\n'.join(L[26:180])+'\n')
print(open('/mnt/user-data/outputs/D-store-census.tsv').read().count('\n'))
