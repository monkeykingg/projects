:- discontiguous sub/2,intro/2.
:- ale_flag(subtypecover,_,off).

bot sub [cat,list,agr,vform,gap_struc].
  cat sub [s,agreeable].
    agreeable sub [aux,gappable]
              intro [agr:agr].
      gappable sub [np,verbal]
               intro [gap:gap_struc].
        verbal sub [v,vp]
               intro [vform:vform,
                      subcat:list].
          v intro [agent:agr,
                   experiencer:agr].
   gap_struc sub [np,none].

list sub [e_list,ne_list].
  ne_list intro [hd:cat,tl:list].

vform sub [active,passive,participle].
agr sub ['3p','3s','2sp','1s','1p'].

s rule
s ===>
cat> (NP,np),
cat> (vp,subcat:[NP],vform:active,gap:none).

s_gap rule
s ===>
cat> (Gap,np,agr:A),
cat> (vp,subcat:[_],agr:A,vform:passive,gap:Gap).

aux rule
(vp,vform:passive,agr:A,
    subcat:SubCat,gap:Gap) ===>
cat> (aux,agr:A),
cat> (vp, vform:participle,
          subcat:SubCat,
          gap:Gap).

vp rule
(vp,agr:A,vform:VF,subcat:SubCatRest,gap:Gap) ===>
cat> (v,agr:A,vform:VF,subcat:[NP|SubCatRest]),
cat> (NP,np,gap:Gap).

kicked ---> (v,agr:A,
             subcat:[(np,agr:B),
                     (np,agr:A)],
             agent:A,
             experiencer:B,
             gap:none).
cans ---> (np,agr:'3p',gap:none).
were ---> aux.

empty (np,gap:(np,agr:A),agr:A).
