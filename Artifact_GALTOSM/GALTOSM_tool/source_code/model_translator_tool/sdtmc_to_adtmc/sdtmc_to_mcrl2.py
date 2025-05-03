import sys
import os

# Check if 3 arguments are provided
if len(sys.argv) != 4:
    print("Usage: python3 code.py <file1> <file2> <file3>")
    sys.exit(1)

# Initialize variables
state_file = None
labels_file = None
trans_file = None

# Iterate through input files and assign based on extension
for file_path in sys.argv[1:]:
    if file_path.endswith('.sta'):
        state_file = file_path
    elif file_path.endswith('.lab'):
        labels_file = file_path
    elif file_path.endswith('.tra'):
        trans_file = file_path
    else:
        print("unrecognized file type\nEnter valid files in any order")
        sys.exit(1)


if not all([state_file, labels_file, trans_file]):
    print("Error: Missing one or more required files (.sta, .lab, .tra)")
    sys.exit(1)

trans_dir = os.path.dirname(trans_file)
trans_base = os.path.splitext(os.path.basename(trans_file))[0]

# Generate new filename
output_filename = os.path.join(trans_dir, f"{trans_base}_A2S.mcrl2")




with open(state_file) as f1:
    state_file_lines = [line.rstrip('\n') for line in f1]
with open(trans_file) as f2:
    trans_file_lines = [line.rstrip('\n') for line in f2]
with open(labels_file) as f3:
    labels_file_lines = [line.rstrip('\n') for line in f3]
f1.close()
f2.close()
f3.close()


old_states=[]
actions=[]
initial_states=[]

act=labels_file_lines[0].split()
act_dict={}
for a in act:
    act_dict[a.split('=')[0]]=a.split('=')[-1][1:-1]


state_labels={}
for i in range(1,len(labels_file_lines)):
    lab_line=labels_file_lines[i].split(':')[-1].split()
    label=''
    for j in range(len(lab_line)):
        if lab_line[j]!='0' and lab_line[j]!='1':
            label+=act_dict[lab_line[j]]
            label+='_PLUS_'
    label=label[:-6]
    if label:
        if label not in actions:
            actions.append(label)
        state_labels['s'+labels_file_lines[i].split(':')[0]]=label
    else:
        state_labels['s'+labels_file_lines[i].split(':')[0]]='PHI'


for i in range(1,len(labels_file_lines)):
    if '0' in labels_file_lines[i].split(':')[-1]:
        initial_states.append('s'+labels_file_lines[i].split(':')[0])


for i in range(1,len(state_file_lines)):
    old_states.append('s'+state_file_lines[i].split(':')[0])
    if 's'+state_file_lines[i].split(':')[0] not in state_labels:
        state_labels['s'+state_file_lines[i].split(':')[0]]='PHI'
        if 'PHI' not in actions:
            actions.append('PHI')


new_states=[]
for i in range(len(old_states)):
    new_states.append(old_states[i])
    new_states.append(old_states[i]+'BAR')


transitions={}
# Old Transitions
for x in old_states:
    transitions[x]=[]
    transitions[x].append('1.0'+'@'+state_labels[x]+'@'+x+'BAR')
# New Transitions
for i in range(1,len(trans_file_lines)):
    origin='s'+trans_file_lines[i].split()[0]+'BAR'
    destination='s'+trans_file_lines[i].split()[1]
    prob=trans_file_lines[i].split()[-1]
    if state_labels['s'+trans_file_lines[i].split()[0]]==state_labels['s'+trans_file_lines[i].split()[1]]:
        action='tau'
    else:
        action=state_labels['s'+trans_file_lines[i].split()[1]]+'_PLUS_bot'
        if action not in actions:
            actions.append(action)
    if origin in transitions:
        transitions[origin].append(prob+'@'+action+'@'+destination)
    else:
        transitions[origin]=[]
        transitions[origin].append(prob+'@'+action+'@'+destination)


from fractions import Fraction
ctr=1
mcrl2_code='\n act '
for i in range(len(actions)):
    mcrl2_code+=actions[i]+', '
mcrl2_code=mcrl2_code[:-2]
mcrl2_code+=';\n\n'

mcrl2_code+='proc '
for x in transitions:
    mcrl2_code+=x+' = '
    if (len(transitions[x]))==1:
        mcrl2_code+='dist b'+str(ctr)+':Bool[if(b'+str(ctr)+',1,0)].(b'+str(ctr)+'->'+transitions[x][0].split('@')[1]+'.'+transitions[x][0].split('@')[-1]+')'
    elif (len(transitions[x]))==2:
        mcrl2_code+='dist b'+str(ctr)+':Bool[if(b'+str(ctr)+','+str(Fraction(transitions[x][0].split('@')[0]))+','+str(Fraction(transitions[x][1].split('@')[0]))+')'
        mcrl2_code+='].('
        mcrl2_code+='b'+str(ctr)+'->'+transitions[x][0].split('@')[1]+'.'+transitions[x][0].split('@')[-1]+' + '
        mcrl2_code+='!b'+str(ctr)+'->'+transitions[x][1].split('@')[1]+'.'+transitions[x][1].split('@')[-1]
        mcrl2_code+=')'
    else:
        mcrl2_code+='dist n'+str(ctr)+':Pos['
        for i in range(len(transitions[x])):
            mcrl2_code+='if(n'+str(ctr)+'=='+str(i+1)+','+str(Fraction(transitions[x][i].split('@')[0]))+','
        mcrl2_code+='0'
        for i in range(len(transitions[x])):
            mcrl2_code+=')'
        mcrl2_code+='].('
        for i in range(len(transitions[x])):
            mcrl2_code+='(n'+str(ctr)+'=='+str(i+1)+')->'+transitions[x][i].split('@')[1]+'.'+transitions[x][i].split('@')[-1]+'+'
        mcrl2_code = mcrl2_code[:-1]
        mcrl2_code+=')'
    mcrl2_code+=';\n'
    ctr+=1

mcrl2_code+='\n init '
for i in range(len(initial_states)):
    mcrl2_code+=initial_states[i]+', '
mcrl2_code=mcrl2_code[:-2]
mcrl2_code+=';\n\n'

with open(output_filename, 'w') as f:
    f.write(mcrl2_code)

print("File Save as: ",output_filename)