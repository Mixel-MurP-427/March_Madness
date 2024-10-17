#Randomly generates and saves a March Madness bracket.
#   "C:\Users\jodim\Downloads\Connor2024MarchMadness.txt"

import random, re, copy

#team cannot have name less than 3 letters
all_teams = {
    'East': ['Uconn', 'Iowa St.', 'Illinois', 'Auburn', 'San Diego St.', 'BYU-', 'Washington St.', 'Fla. Atlantic', 'Northwestern', 'Drake', 'Duquesne', 'UAB-', 'Yale', 'Morehead St.', 'South Dakota St.', 'Stetson'], 
    'West': ['North Carolina', 'Arizona', 'Baylor', 'Alabama', 'Saint Mary\'s', 'Clemson', 'Dayton', 'Mississippi St.', 'Michigan St.', 'Nevada', 'New Mexico', 'Grand Canyon', 'Charleston', 'Cologate', 'Long Beach St.', 'Wagner'], 
    'South': ['Houston', 'Marquette', 'Kentucky', 'Duke', 'Wisconsin', 'Texas Tech', 'Florida', 'Nebraska', 'Texas A&M', 'Colorado', 'NC State', 'James Madison', 'Vermont', 'Oakland', 'Western Kentucky', 'Longwood'],
    'Midwest': ['Purdue', 'Tennessee', 'Creighton', 'Kansas', 'Gonzaga', 'South Carolina', 'Texas', 'Utah St.', 'TCU-', 'Colorado St.', 'Oregon', 'McNeese', 'Samford', 'Akron', 'Saint Peter\'s', 'Grambling']}

round1matches = [(0, 15), (7, 8), (4, 11), (3, 12), (5, 10), (2, 13), (6, 9), (1, 14)]

letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')

def get_abbrv(gaTeam):
    if not ' ' in gaTeam:
        return gaTeam[:4]
    elif gaTeam.count(' ') == 1:
        return gaTeam[:3] + gaTeam[gaTeam.index(' ') + 1]
    else:#assume that gaTeam has 2 spaces
        gaIndex = gaTeam.index(' ')
        gaOut = gaTeam[:gaIndex] + gaTeam[gaIndex + 1:]
        return gaTeam[0] + gaTeam[gaIndex + 1:gaIndex + 3] + gaOut[gaOut.index(' ') + 1]

#store abbriviations of all team names in list
abbrv_teams = {}
for division in all_teams:
    abbrv_teams[division] = []
    for team in all_teams[division]:
        abbrv_teams[division].append(get_abbrv(team))

bracket_object = open("Misc_projects/VS2024MarchMadnessTemplate.txt", 'r')
bracket_template = bracket_object.readlines()
bracket_object.close

#assign proper starting teams to template bracket
line = 3
new_template_list = []
for left_division, right_division in zip(('East', 'West'), ('South', 'Midwest')):
    for match in round1matches:
        for team in match:
            newLeftTeam = str(team + 1) + ' ' + all_teams[left_division][team]
            newRightTeam = all_teams[right_division][team] + ' ' + str(team + 1) + '\n'
            new_template_list.append(newLeftTeam + '-' * (20 - len(newLeftTeam)) + bracket_template[line][20:-20] + '-' * (21 - len(newRightTeam)) + newRightTeam)#[20:116]
            line += 1
    line += 1

new_template_string = ''
for row in range(3):
    new_template_string = new_template_string + bracket_template[row]
for row in new_template_list[:16]:
    new_template_string = new_template_string + row
new_template_string = new_template_string + bracket_template[19]
for row in new_template_list[16:]:
    new_template_string = new_template_string + row

#write empty bracket to file. Note that file is overwritten later.
bracket_object = open("Misc_projects/testBracketTemplate.txt", 'w')
bracket_object.write(new_template_string)
bracket_object.close()

#make picks and put in bracket

all_matches = {'East': {32: round1matches, 16: [[], [], [], []], 8: [[], []], 4: [[]], 2: [[]]}}
all_matches['West'] = copy.deepcopy(all_matches['East'])
all_matches['South'] = copy.deepcopy(all_matches['East'])
all_matches['Midwest'] = copy.deepcopy(all_matches['East'])

new_picks_bracket_list = copy.deepcopy(new_template_list)
for MMround in (32, 16, 8, 4):
    switch = 1
    every_other = -1
    for match in range(int(MMround/4)):
        every_other += switch
        for division in all_teams:
            #find whcih two teams are competing
            competitors = all_matches[division][MMround][match]
            #pick winner (seed of)
            winner = random.choice([competitors[0]] * (16-competitors[0]) + [competitors[1]] * (16-competitors[1]))
            #add winner to all_matches
            all_matches[division][MMround/2][every_other].append(winner)
            #add winner to bracket
            str_MMround = str(MMround)
            if len(str_MMround) == 1:
                str_MMround = '0' + str_MMround
            specific_place = re.compile(division[0] + str_MMround + letters[match])
            new_template_string = specific_place.sub(abbrv_teams[division][winner], new_template_string)
        if switch == 0:
            switch = 1
        else:
            switch = 0

#print(all_matches)

def get_seed(gsTeam):
    for division in all_teams:
        try:
            return abbrv_teams[division].index(gsTeam)
        except:
            continue

#pick final 4 and champion
final_matches = {}
for div1, div2, side in zip(('East', 'South'), ('West', 'Midwest'), ('LEFT', 'RITE')):
    competitors = (abbrv_teams[div1][all_matches[div1][2][0][0]], abbrv_teams[div2][all_matches[div2][2][0][0]])
    winner = random.choice([competitors[0]] * (16-all_matches[div1][2][0][0]) + [competitors[1]] * (16-all_matches[div2][2][0][0]))
    final_matches[side] = winner
    specific_place = re.compile(side)
    new_template_string = specific_place.sub(winner, new_template_string)

winner = random.choice([final_matches['LEFT']] * (16-get_seed(final_matches['LEFT'])) + [final_matches['RITE']] * (16-get_seed(final_matches['RITE'])))
specific_place = re.compile('WINR')
new_template_string = specific_place.sub(winner, new_template_string)


bracket_object = open("Misc_projects/testBracketTemplate.txt", 'w')
bracket_object.write(new_template_string)
bracket_object.close()