import sys
import os
fn=sys.argv[1]
#fn1=os.path.basename(fn)
#base_location = os.path.dirname(fn)

abs_path = os.path.abspath(fn)

# Extract just the filename
fn1 = os.path.basename(abs_path)

# Extract the base location (directory path)
base_location = os.path.dirname(abs_path)


with open(fn,'r') as f:
    lines=f.readlines()
f.close()


# Pre-processing the file to infer states, transitions, actions, probabilities and initial distribution.
tran_list=[]
initial=''
for i in range(len(lines)):
    if i==0:
        origin='s'+lines[i].split(',')[-1].rstrip()[:-1]
        initial=origin
        action='tau'
        dest=[]
        prob=[]
        cp=1.0
        il=lines[i].split('(')[-1].split(',')[0].split(' ')
        if len(il)>1:
            il1=0
            il2=1
            while il1<=len(il):
                dest.append(il[il1])
                il1+=2
            while il2<len(il):
                p=float(il[il2].split('/')[0])/float(il[il2].split('/')[-1])
                prob.append(p)
                cp-=p
                il2+=2
            prob.append(str(cp))
        else:
            dest.append(il[0])
            prob.append('1.0')
        for j in range(len(prob)):
            tlm=[]
            tlm.append(origin)
            tlm.append(action+'.s'+dest[j])
            tlm.append(str(prob[j]))
            tran_list.append(tlm)
        continue
    a=lines[i].rstrip().split(',')
    origin=''
    action=''
    dest=[]
    prob=[]
    cp=1.0
    for j in range(1,len(a[0])):
        origin+=a[0][j]
    for h in range(1,len(a)-1):
        for j in range(1,len(a[h])):
            if a[h][j]!=')' and a[h][j]!='"':
                action+=a[h][j]
            if j+1==len(a[h]) and a[h][j]!=')' and a[h][j]!='"':
                action+='_'  
    if action.startswith("label("):
        continue
    action=action.replace('(','_')
    action=action.replace(')','')    
    action=action.replace(',','_')
    action=action.replace(' ','')
    a[-1]=a[-1][:-1]
    b=a[-1].split(' ')
    if len(b)>1:
        j=0
        k=1
        while j<=len(b):
            dest.append(b[j])
            j+=2
        while k<len(b):
            p=float(b[k].split('/')[0])/float(b[k].split('/')[-1])
            prob.append(p)
            cp-=p
            k+=2
        prob.append(str(cp))
    else:
        dest.append(b[0])
        prob.append('1.0')
    for k in range(len(dest)):
        tlm=[]
        tlm.append('s'+origin)
        tlm.append(action+'.s'+dest[k])
        tlm.append(str(prob[k]))
        tran_list.append(tlm)
#print(tran_list)
state={}
action=[]
prism_pr_adj={}
for i in range(len(tran_list)):
    if tran_list[i][0].split('s')[-1] not in state:
        state[tran_list[i][0].split('s')[-1]]=tran_list[i][0]
    if tran_list[i][1].split('.')[-1].split('s')[-1] not in state:
        state[tran_list[i][1].split('.')[-1].split('s')[-1]]=tran_list[i][1].split('.')[-1]
    if tran_list[i][1].split('.')[0] not in action and tran_list[i][1].split('.')[0]!='tau':
        action.append(tran_list[i][1].split('.')[0])
    if str(tran_list[i][0]) not in prism_pr_adj:
        prism_pr_adj[str(tran_list[i][0])]={}
        prism_pr_adj[str(tran_list[i][0])][str(tran_list[i][1])]=str(tran_list[i][-1])
    else:
        prism_pr_adj[str(tran_list[i][0])][str(tran_list[i][1])]=str(tran_list[i][-1])
deadlock=list(set(state.values())-set(prism_pr_adj.keys()))
# CONVERTING THE ADTMC TO SDTMC USING THE MODEL EMBEDDING ats FOR PROBABILISTIC SYSTEMS.
labels={}
mapping={}
ats_adj={}
transition_count=1
ctr=0
for x in prism_pr_adj:
    a=x
    b=prism_pr_adj[x]
    #print(a,b)
    if a not in labels:
        labels[a]='bot'
    if a not in mapping:
        mapping[a]=a
    for y in b:
        if y not in mapping and y.split('.')[0]!='tau':
            mapping[y]='s'+str(len(state)+ctr)
            ctr+=1
        if y not in labels and y.split('.')[0]!='tau':
            labels[mapping[y]]=y.split('.')[0]
    if x not in ats_adj:
        ats_adj[x]={}
        for y in prism_pr_adj[x]:
            if y.split('.')[0]!='tau':
                ats_adj[x][mapping[y]]=prism_pr_adj[x][y]
                transition_count+=1
            else:
                ats_adj[x][y.split('.')[-1]]=prism_pr_adj[x][y]
                transition_count+=1
for x,y in mapping.items():
    if x!=y:
        ats_adj[y]={x.split('.')[-1]:1.0}
        transition_count+=1
for x in deadlock:
    labels[x]='bot'
    mapping[x]=x
# GENERATING THE SDTMC CODE. (PRISM). The code assigns automatic reward structures correspondoing to each action,
# and each step of the original model as 'original step'. The Code at the end also prints the state mapping for old and
# new states. COMMENT/UNCOMMENT these optional features based on your requirement.
code3=''
code3+='\n\n dtmc \n\t module ats_ADTMC \n\n //Variables\n'
code3+='s:[0..'+str(len(mapping)-1)+'] init '+initial.split('s')[-1]
code3+=';\n'
for a,b in ats_adj.items():
    code3+='\n [] s='+a.split('s')[-1]+' ->'
    for c in b:
        code3+=' '+str(b[c])+":(s'="+c.split('s')[-1]+')+'
    code3=code3[:-1]
    code3+=';'
for x in deadlock:
    code3+='\n [] s='+x.split('s')[-1]+" -> 1.0:(s'="+x.split('s')[-1]+');'
code3+='\n\n\t endmodule \n\n //Labels'
code3+='\n label "Initial" = (s='+initial.split('s')[-1]+');'
if deadlock:
    code3+='\n label "Final" = '
    for x in deadlock:
        code3+='(s='+x.split('s')[-1]+')|'
    code3=code3[:-1]
    code3+=';'
code3+='\n label "bot"= '
for i in labels:
    if labels[i]=='bot':
        code3+='(s='+i.split('s')[-1]+')|'
code3=code3[:-1]
code3+=';'
for i in range(len(action)):
    flag=0
    for j in labels:
        if labels[j]==action[i]:
            flag=1
            break
    if flag==1:
        code3+='\n label "'+action[i]+'"= '
        for j in labels:
            if labels[j]==action[i]:
                code3+='(s='+j.split('s')[-1]+')|'
        code3=code3[:-1]
        code3+=';'
    else:
        continue

if fn1.endswith('.lts'):
    fn1=fn1.split('.lts')[0]
else:
    fn1=fn1.split('.aut')[0]
file7=base_location+'/'+fn1+'.prism'

if code3!='':
    file = open(file7,'w')
    file.write(code3)
    file.close()
