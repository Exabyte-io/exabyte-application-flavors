export default ` start nwchem
 title "Test"
 charge {{ input.CHARGE }}
 geometry units au noautosym
 {{ input.ATOMIC_POSITIONS }}
 end
 basis
   * library {{ input.BASIS }}
 end
 dft
 xc {{ input.FUNCTIONAL }}
 mult {{ input.MULT }}
 end
 task dft energy`;
