bot sub [cat, gender_feature, sem].
    cat sub [v, det, has_gender] intro [sem:sem].
        has_gender sub [s, np, vp, n, pn] intro [gender:gender_feature].
    gender_feature sub [m, f, neu].
    sem sub [waiter, cat].

    np sub [nprp].

she ---> (pn, gender:f).
he ---> (pn, gender:m).
is ---> v.
the ---> (det).
waiter ---> (n, gender:m, sem:waiter).
waitress ---> (n, gender:f, sem:waiter).
cat ---> (n, gender:neu, sem:cat).

det_n__np rule
    (np, gender:Gender, sem:Sem) ===>
    cat> det,
    cat> (gender:Gender, sem:(Sem, cat), n).

pn__np rule
    (np, gender:Gender) ===>
    cat> (pn, gender:Gender).

v_np__vp rule
    (vp, gender:Gender) ===>
    cat> v,
    cat> (np, gender:Gender).

np_vp__s rule
    (s, gender:Gender) ===>
    cat> (np, gender:Gender),
    cat> (vp, gender:Gender).

np_vp__s rule
    (s, gender:Gender) ===>
    cat> (np),
    cat> (vp, gender:(neu, Gender)).