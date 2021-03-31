export default `&INPUT
    asr = 'simple'
    flfrc = 'force_constants.fc'
    flfrq = 'frequencies.freq'
    dos = .true.
    fldos = 'phonon_dos.out'
    deltaE = 1.d0
    {% for d in igrid.dimensions -%}
    nk{{loop.index}} = {{d}}
    {% endfor %}
 /
`;
