bot sub [s, phrase, lexical].
phrase sub [vpsg, vppl, pp, npsg, nppl, np].
lexical sub [nprp, npl, vpl, vsg, det, nsg, npl, p].


fido ---> nprp.
biscuits ---> npl.
feed ---> vpl.
feeds ---> vsg.
the ---> det.
dog ---> nsg.
puppies ---> npl.
with ---> p.


vsg_np__vpsg rule
vpsg ===>
cat> vsg,
cat> np.

vpl_np__vppl rule
vppl ===>
cat> vpl,
cat> np.

p_np__pp rule
pp ===>
cat> p,
cat> np.

nprp__npsg rule
npsg ===>
cat> nprp.

det_nsg__npsg rule
npsg ===>
cat> det,
cat> nsg.

det_nsg_pp__npsg rule
npsg ===>
cat> det,
cat> nsg,
cat> pp.

det_npl__nppl rule
nppl ===>
cat> det,
cat> npl.

det_npl_pp__nppl rule
nppl ===>
cat> det,
cat> npl,
cat> pp.

npl__nppl rule
nppl ===>
cat> npl.

npl_pp__nppl rule
nppl ===>
cat> npl,
cat> pp.

npsg__np rule
np ===>
cat> npsg.

nppl__np rule
np ===>
cat> nppl.

npsg_vpsg__s rule
s ===>
cat> npsg,
cat> vpsg.

nppl_vppl__s rule
s ===>
cat> nppl,
cat> vppl.
