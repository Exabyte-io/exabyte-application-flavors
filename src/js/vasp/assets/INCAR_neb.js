export default `ISTART = 0
IBRION = 1
EDIFFG = -0.001
ENCUT = 500
NELM = 100
NSW = 100
IMAGES = {{ input.INTERMEDIATE_IMAGES.length || neb.nImages }}
SPRING = -5
ISPIN = 2
`;
