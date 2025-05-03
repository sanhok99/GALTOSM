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
        print("unrecognized file type\n Enter valid files in any order")
        sys.exit(1)


if not all([state_file, labels_file, trans_file]):
    print("Error: Missing one or more required files (.sta, .lab, .tra)")
    sys.exit(1)

trans_dir = os.path.dirname(trans_file)
trans_base = os.path.splitext(os.path.basename(trans_file))[0]

# Generate new filename
output_filename = os.path.join(trans_dir, f"{trans_base}_A2S.aut")




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
initial_state=''

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
        state_labels[labels_file_lines[i].split(':')[0]]=label
    else:
        state_labels[labels_file_lines[i].split(':')[0]]='PHI'

for i in range(1,len(state_file_lines)):
    old_states.append(state_file_lines[i].split(':')[0])
    if state_file_lines[i].split(':')[0] not in state_labels:
        state_labels[state_file_lines[i].split(':')[0]]='PHI'
        if 'PHI' not in actions:
            actions.append('PHI')

for i in range(1,len(labels_file_lines)):
    if '0' in labels_file_lines[i].split(':')[-1]:
        initial_state=labels_file_lines[i].split(':')[0]

new_states=[]
for i in range(len(old_states)):
    new_states.append(old_states[i])
    new_states.append(str(len(old_states)+int(old_states[i])))

transitions={}
# Old Transitions
for x in old_states:
    transitions[x]=[]
    transitions[x].append('1'+'@'+state_labels[x]+'@'+str(int(x)+len(old_states)))

# New Transitions
for i in range(1,len(trans_file_lines)):
    origin=str(int(trans_file_lines[i].split()[0])+len(old_states))
    destination=trans_file_lines[i].split()[1]
    prob=trans_file_lines[i].split()[-1]
    if state_labels[trans_file_lines[i].split()[0]]==state_labels[trans_file_lines[i].split()[1]]:
        action='tau'
    else:
        action=state_labels[trans_file_lines[i].split()[1]]+'_PLUS_bot'
        if action not in actions:
            actions.append(action)
    if origin in transitions:
        transitions[origin].append(prob+'@'+action+'@'+destination)
    else:
        transitions[origin]=[]
        transitions[origin].append(prob+'@'+action+'@'+destination)

num_tra=0
cadp_aut=''
for x in transitions:
    for y in transitions[x]:
        if y.split('@')[1]=='tau':
            cadp_aut+='\n('+x+',* ; prob '+y.split('@')[0]+','+y.split('@')[2]+')'
        else:
            cadp_aut+='\n('+x+','+y.split('@')[1]+'; prob '+y.split('@')[0]+','+y.split('@')[2]+')'
        num_tra+=1
cadp_aut_line1='\n('+initial_state+','+str(num_tra)+','+str(len(new_states))+')'
cadp_aut=cadp_aut_line1+cadp_aut
#print(cadp_aut)

with open(output_filename, 'w') as f:
    f.write(cadp_aut)

#print("file saved in: ",trans_dir)
print("File Save as: ",output_filename)
