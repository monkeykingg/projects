bot sub [cat, agr, vform, list, number, case, sem].

list sub [e_list, ne_list].
    ne_list intro [hd:bot, tl:list].

vform sub [active, passive, participle].

agr intro [number:number, case:case].
sem sub [kick, can].
    kick intro [agent:agr, experiencer:agr].
number sub [singular, plural].
case sub [first, second, third].

cat sub [s, gappable, agreeable, vproj].
    agreeable sub [aux, has_sem] intro [agr:agr].
        has_sem sub [v, np] intro [sem:sem].
    gappable sub [np, vp] intro [gap:gap_struc].
    vproj sub [vp, v] intro [vform:vform, subcat:list].

empty np.

cans ---> (np, agr:(number:plural, case:third)).
were ---> (aux, agr:(number:plural, case:second)).
were ---> (aux, agr:(number:plural, case:third)).
kicked ---> (v, agr:Agent,
                subcat:[(np, agr:Agent),(np, agr:Experiencer)],
                sem:(kick, agent:Agent, experiencer:Experiencer)).

v_np__vp rule
(vp, subcat:[AgentNP]) ===>
cat> (v, agr:A, subcat:[AgentNP, ExperiencerNP]),
cat> (np, ExperiencerNP).