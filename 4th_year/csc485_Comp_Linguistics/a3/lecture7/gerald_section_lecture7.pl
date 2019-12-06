bot sub [cat,list,agr,vform].
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

list sub [e_list,ne_list].
  ne_list intro [hd:bot,tl:list].

vform sub [active,passive,participle].
agr sub [3p,3s,2sp,1s,1p].

s rule
s ===> 
cat> (NP,np,agr:A)
cat> (vp,agr:A,subcat:[NP]).

aux rule
(vp,vform:passive,agr:A,
    subcat:SubCat) ===> 
cat> (aux,agr:A),
cat> (vp, vform:participle,
          subcat:SubCat).

vp rule
(vp,agr:A,subcat:SubCatRest) ===> 
cat> (v,agr:A,subcat:[NP|SubCatRest]),
cat> (NP,np).

kicked ---> (v,agr:A,
             subcat:[(np,agr:B),
                     (np,agr:A)],
             agent:A,
             experiencer:B).
cans ---> (np,agr:3p).
were ---> aux.

empty np.


