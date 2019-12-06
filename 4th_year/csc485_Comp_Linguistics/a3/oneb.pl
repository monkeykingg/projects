bot sub [cat, number, no_number].
cat sub [s, has_number, pp].
number sub [singular, plural].
has_number sub [n, v, np, vp] intro [number:number].
no_number sub [det, p].


fido ---> (np, number:singular).
biscuits ---> (n, number:plural).
feed ---> (v, number:plural).
feeds ---> (v, number:singular).
the ---> det.
dog ---> (n, number:singular).
puppies ---> (n, number:plural).
with ---> p.


vp__v_np rule
(vp, number:Number) ===>
cat> (v, number:Number),
cat> np.

pp__p_np rule
pp ===>
cat> p,
cat> np.

np__n rule
(np, number:Number) ===>
cat> (n, number:Number).

np__det_n rule
(np, number:Number) ===>
cat> det,
cat> (n, number:Number).

np__det_n_pp rule
(np, number:Number) ===>
cat> det,
cat> (n, number:Number),
cat> pp.

np__n_pp rule
(np, number:Number) ===>
cat> (n, number:Number),
cat> pp.

s__np_vp rule
s ===>
cat> (np, number:Number),
cat> (vp, number:Number).
