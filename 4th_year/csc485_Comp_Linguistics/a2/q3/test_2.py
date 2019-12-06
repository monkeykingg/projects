import nltk



grammer = nltk.CFG.fromstring("""
S -> NP_s VP
S -> NP_s VP AdvP
S -> NP_s VP-Aux
S -> NP_s VP-Aux AdvP

NP_s -> NPro_s | NPrp | NComP
NP_o -> NPro_o | NPrp | NComP

NComP -> NCountP | NMassP

NCountP -> NVowelP | NConsonantP
NVowelP -> Det-v NVowel
NConsonantP -> Det-c NConsonant

NMassP -> Det-m NMass | NMass

NComP -> NComP PP
NComP -> Det AdjP | AdjP

AdjP -> Adj AdjP | Adj NMass | Adj NVowel | Adj NConsonant
PP -> P NP_o

VP -> Vi-sp            % regular intransitive verb structure
VP -> Vi-sp Adv
VP -> Adv Vi-sp       %     and with an adverb before the verb
% adverb right before a verb phrase without aux

VP -> VP PP            % preposition after a verb phrase without aux
VP_AUX -> VP_AUX PP 

VP -> Vi-sp
VP -> Vi-sp AdvP
VP -> AdvP Vi-sp
VP -> AdvP VP
VP -> VP PP
VP-Aux -> VP-Aux PP

VP-Aux -> Aux-Vi Vi | Aux-Vi AdvP Vi
VP-Aux -> Aux-Vi-gp Vi-gp | Aux-Vi-gp AdvP Vi-gp
VP-Aux -> Aux-Vi-pp Vi-pp | Aux-Vi-pp AdvP Vi-pp
VP-Aux -> Aux-Vt-pp Vm-pp | Aux-Vt-pp AdvP Vm-pp

Aux-Vt-pp -> AuxPassive

Aux-Vi-gp -> AuxProgressive

Aux-Vt-pp -> AuxProgressive AuxProgressivePassive

Aux-Vi-pp -> AuxPerfect

Aux-Vt-pp -> AuxPerfect AuxPerfectPassive

Aux-Vi-gp -> AuxPerfect AuxPerfectProgressive

Aux-Vt-pp -> AuxPerfect AuxPerfectProgressive AuxProgressivePassive

Aux-Vi -> AuxModal

Aux-Vt-pp -> AuxModal AuxModalPassive

Aux-Vi-gp -> AuxModal AuxModalProgressive

Aux-Vt-pp -> AuxModal AuxModalProgressive AuxProgressivePassive

Aux-Vi-pp -> AuxModal AuxModalPerfect

Aux-Vt-pp -> AuxModal AuxModalPerfect AuxPerfectPassive

Aux-Vi-gp -> AuxModal AuxModalPerfect AuxPerfectProgressive

Aux-Vt-pp -> AuxModal AuxModalPerfect AuxPerfectProgressive AuxProgressivePassive

VP -> Vm-sp NP_o

VP -> Vd-sp NP_o NComP

VP -> Vm-sp-that RelativePronoun S
VP -> Vd-sp-that NP_o RelativePronoun S

VP -> Vm-sp-to ParticleTo V-inf-P
VP -> Vd-sp-to NP_o ParticleTo V-inf-P

V-inf-P -> Vm-to ParticleTo V-inf-P
V-inf-P -> Vd-to NP_o ParticleTo V-inf-P
V-inf-P -> Vi | Vm NP_o | Vd NP_o NComP

V-inf-P -> AdvP V-inf-P

VP -> V-was NP_o | V-was PP | V-was AdvP PP

Det -> 'the' | 'my'
Det-m -> 'the' | 'my' 
Det-v -> 'the' | 'my' | 'an'
Det-c -> 'the' | 'my' | 'a' 

NMass -> 'fur' | 'cheese' | 'autopoiesis' | 'menu' | 'help'
NVowel -> 'eggplant' | 'autoclave' | 'elephant'
NConsonant -> 'cat' | 'boat' | 'poodle' | 'cloth' | 'man' | 'hovercraft' | 'rutabaga'

NPrp -> 'Nadia' | 'Ross' | 'Marseilles' | 'Google'

NPro_s -> 'I' | 'he' | 'she' | 'it' | 'we' | 'they' | 'you'
NPro_o -> 'him' | 'her' | 'it' | 'us' | 'them' | 'you'

Adj -> 'handsome' | 'tall' | 'long' | 'soft'
P -> 'with' | 'for' | 'on' | 'onto' | 'to' | 'of' | 'from' | 'before' | 'after'
Adv -> 'slowly' | 'immediately' | 'already' | 'really' | 'always'

AuxModal -> 'can' | 'may' | 'could' | 'should' | 'might' | 'must' | 'would' | 'will'
AuxPerfect -> 'have' | 'had' | 'has'
AuxProgressive -> 'are' | 'were' | 'is' | 'was' | 'am'
AuxPassive -> 'are' | 'were' | 'is' | 'was' | 'am'

AuxModalPerfect -> 'have'
AuxModalProgressive -> 'be'
AuxModalPassive -> 'be'
AuxPerfectProgressive -> 'been'
AuxPerfectPassive -> 'been'
AuxProgressivePassive -> 'being'

RelativePronoun -> 'that'
ParticleTo -> 'to'

Vi -> 'arrive' | 'leave' | 'shoot' | 'eat' | 'jump' | 'believe' | 'win' | 'help' | 'demand'
Vi-sp -> 'arrived' | 'left' | 'shot' | 'ate' | 'jumped' | 'believed' | 'won' | 'helped' | 'demanded'
Vi-pp -> 'arrived' | 'left' | 'shot' | 'eaten' | 'jumped' | 'believed' | 'won' | 'helped' | 'demanded'
Vi-gp -> 'arriving' | 'leaving' | 'shooting' | 'eating' | 'jumping' | 'believing' | 'winning' | 'helping' | 'demanding'

Vm -> 'leave' | 'shoot' | 'eat' | 'fondle' | 'bring' | 'tell' | 'jump' | 'believe' | 'win' | 'see' | 'want' | 'help' | 'remind' | 'reward' | 'demand' | 'find' | 'give' | 'have'
Vm-sp -> 'left' | 'shot' | 'ate' | 'fondled' | 'brought' | 'told' | 'jumped' | 'believed' | 'won' | 'saw' | 'wanted' | 'helped' | 'reminded' | 'rewarded' | 'demanded' | 'found' | 'gave' | 'had'
Vm-pp -> 'left' | 'shot' | 'eaten' | 'fondled' | 'brought' | 'told' | 'jumped' | 'believed' | 'won' | 'seen' | 'wanted' | 'helped' | 'reminded' | 'rewarded' | 'demanded' | 'found' | 'given'

Vd -> 'bring' | 'tell' | 'remind' | 'demand' | 'give'
Vd-sp -> 'brought' | 'told' | 'reminded' | 'demanded' | 'gave'
Vd-pp -> 'brought' | 'told' | 'reminded' | 'demanded' | 'given'

Vm-sp-that -> 'told' | 'believed' | 'saw' | 'reminded'
Vd-sp-that -> 'told' | 'reminded'
Vm-sp-to -> 'left' | 'wanted' | 'demanded' | 'had' | 'aspired'
Vd-sp-to -> 'brought' | 'told' | 'reminded' | 'demanded' | 'gave'
Vm-to -> 'leave' | 'want' | 'demand' | 'have'
Vd-to -> 'bring' | 'tell' | 'remind' | 'demand' | 'give'

V-was -> 'was' | 'were'
""")

test_trans_neg = """Nadia ate
Nadia slowly ate
Nadia ate slowly
Nadia ate slowly with cat
Nadia ate with cat slowly
Nadia ate slowly with the long soft cat
Nadia ate with the long soft cat slowly
Nadia ate with the cat with long soft fur
Nadia ate slowly with the cat with long soft fur
Nadia ate with the cat with long soft fur slowly
Nadia was eating
Nadia was slowly eating
Nadia was eating slowly
Nadia was slowly eating with cat
Nadia was slowly eating with her cat
Nadia was eating slowly with her cat
Nadia was eating with her cat with long soft fur slowly
Nadia was slowly eating with her cat with long soft fur
Ross is eating with her cat
Ross is eating with her cat on the hovercraft
Ross is eating with her cat on the hovercraft slowly
Ross is slowly eating with her cat on the hovercraft
she has left
she has left slowly
she has slowly left
she has left with the cheese
she has left with the cheese slowly
she has slowly left with the cheese
Nadia has left
Nadia has left from her
Nadia has left from her to the hovercraft
Nadia has slowly left from the cat on the hovercraft
he will leave
he will leave slowly
he will slowly leave
he will leave to the hovercraft
he will leave from her cat
she has been eating
she has been slowly eating
she has been eating slowly
she has been eating with her cat slowly
she has been slowly eating with her cat
she has been being helped
she has been being helped often
she has often been being helped
she has been being helped with her cat
she has been being helped with her cat with long soft fur
she has been being helped with her cat with long soft fur often
she has always been being helped with her cat
the cat with the long soft fur have been eating
the cat with the long soft fur have been slowly eating
the cat with the long soft fur have been eating slowly with Ross
Ross will have been eating
Ross will have slowly been eating
Ross will have been eating slowly
Ross will have been eating with Nadia slowly
Ross will have been eating with her cat with long soft fur
Nadia will have left
Nadia will have slowly left
Nadia will have left slowly
Nadia will have left slowly with her cat
Nadia will have left slowly with her cat with long soft fur
Nadia will have left slowly with her cat with long soft fur slowly
he will be eating
he will slowly be eating
he will be eating slowly
he will be slowly eating
he will be eating with her cat
he will be eating with her cat slowly
he will be eating with her cat with long soft fur slowly
Nadia is seen by her cat
Nadia was seen by her cat
Nadia was seen by her cat often
Nadia was often seen by her cat with long soft fur
the cat with long soft fur was helped by Nadia
the cat with long soft fur was often helped by Nadia
the cat with long soft fur is often helped by Nadia
Ross had been eaten slowly by the elephant
Ross had been slowly eaten by the elephant
Ross had been eaten slowly by the elephant with long soft fur
Ross had been eaten by the elephant with long soft fur slowly
the elephant will be seen by Ross
the elephant will often be seen by Ross
the elephant will be often seen by Ross
the elephant will be seen by Ross often
Nadia had left
Nadia had left immediately
Nadia had left with the elephant on the hovercraft
the tall elephant will have been being seen by Ross
the tall elephant will have been often being seen by Ross
the tall elephant will have been being seen often by Ross
the tall elephant will have been being seen by Ross on the hovercraft
the soft cat had eaten
the soft cat had eaten with Nadia
the soft cat had slowly eaten with Nadia
the soft cat had eaten slowly with Nadia on the hovercraft with Ross 
"""

parser = nltk.parse.BottomUpChartParser(grammer)

test_trans_neg = [s.split() for s in test_trans_neg.split('\n')]
a = 0
for s in test_trans_neg:
    try:
        #print("==========================")
        print(len(list(parser.parse(s))) > 0)
        a+=1

    except Exception as e:
        print(s)
