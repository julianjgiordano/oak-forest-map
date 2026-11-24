"""Build web/story/index.html (the guided Panel 75 chapter) from web/beneath/index.html plus the story parts.
Usage: python3 make_story.py <web folder>"""
import sys, os
W = sys.argv[1]; P = os.path.join(W, 'tools', 'story_parts')
s = open(os.path.join(W, 'beneath', 'index.html')).read()
def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:80]); s = s.replace(a, b)
R('"three": "./vendor/three.module.min.js"', '"three": "../beneath/vendor/three.module.min.js"')
for f in ['OrbitControls.js', 'CSS2DRenderer.js', 'lines/Line2.js', 'lines/LineGeometry.js', 'lines/LineMaterial.js']:
    R(f"from './vendor/{f}'", f"from '../beneath/vendor/{f}'")
R("get('data/p75.json', 'json'), get('data/p75.bin', 'arrayBuffer'), get('data/p75_extra.json', 'json'), get('data/p75_gates.json', 'json')",
  "get('../beneath/data/p75.json', 'json'), get('../beneath/data/p75.bin', 'arrayBuffer'), get('../beneath/data/p75_extra.json', 'json'), get('../beneath/data/p75_gates.json', 'json')")
R('<title>Panel 75 · Oak Forest</title>', '<title>Panel 75: the story · Oak Forest</title>')
R('<meta property="og:url" content="https://oakforest.juliangiordano.com/beneath/">', '<meta property="og:url" content="https://oakforest.juliangiordano.com/story/">')
R('<meta property="og:image" content="https://oakforest.juliangiordano.com/beneath/og-image.jpg">', '<meta property="og:image" content="https://oakforest.juliangiordano.com/beneath/og-image.jpg">\n<meta name="robots" content="noindex">')
R('family=Inter:wght@400;500;600;700&display=swap', 'family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap')
R('  @media (prefers-reduced-motion: reduce) { .lbl { transition:none; } }\n</style>', '  @media (prefers-reduced-motion: reduce) { .lbl { transition:none; } }\n' + open(os.path.join(P, 'story.css.txt')).read() + '</style>')
R('<div id="loading" role="status">Loading the land…</div>', '<div id="loading" role="status">Loading the land…</div>\n' + open(os.path.join(P, 'story.dom.txt')).read())
R('<a href="./" aria-current="page"><span class="l">Panel 75 in 3D</span><span class="s">Panel 75</span></a>', '<a href="../beneath/"><span class="l">Panel 75 in 3D</span><span class="s">Panel 75</span></a>')
# the opening map uses MapLibre, as /map/ does (same version, with SRI)
R("script-src 'self' 'unsafe-inline' ;", "script-src 'self' 'unsafe-inline' https://unpkg.com;")
R('</head>', '<link href="https://unpkg.com/maplibre-gl@5.24.1/dist/maplibre-gl.css" rel="stylesheet" integrity="sha384-uTttxo/aOKbdE5RlD/SPzSDoDmNvGlUYPjONi2MN/b7c9HPSvW07OIuyP7uL6jxK" crossorigin="anonymous">\n<script src="https://unpkg.com/maplibre-gl@5.24.1/dist/maplibre-gl.js" integrity="sha384-nXMl9YiLoSG5KBPTFgvxVuIqQQcqIvo0bFrvoEaGJC6r7IibIzF1S36Zbf/sKBtL" crossorigin="anonymous"></script>\n</head>')
R("renderer.setPixelRatio(Math.min(devicePixelRatio, isPhone ? 1.5 : 2));", "renderer.setPixelRatio(Math.min(devicePixelRatio, isPhone ? 1 : 2));")
R("  const run = playing ? dtr : 0; simT += run;", "  const run = (playing || storyRun) ? dtr : 0; simT += run;")
R("    let side = camera.position.z < -d ? -1 : 1;                  // the camera is on the larger-d side -> the section goes to the smaller-d side",
  "    let side = sectFix ? sectFix.side : (camera.position.z < -d ? -1 : 1);   // the camera is on the larger-d side -> the section goes to the smaller-d side")
R("    if (room(side) < SEC.W * 0.6) side = -side;\n    const dP = d + side * 30,",
  "    if (!sectFix && room(side) < SEC.W * 0.6) side = -side;\n    const dP = sectFix ? sectFix.d : d + side * 30,")
R("addEventListener('keydown', e => {\n  if (e.target.tagName === 'INPUT'", "addEventListener('keydown', e => {\n  if (window.__storyLocked) return;\n  if (e.target.tagName === 'INPUT'")
# x-ray also on materials whose vertex shader sinkify has already rewritten
R("""    sh.vertexShader = 'varying vec3 vXw;\\n' + sh.vertexShader.replace('#include <project_vertex>', `#include <project_vertex>
      vec4 _xw = vec4(transformed, 1.0);
      #ifdef USE_INSTANCING
        _xw = instanceMatrix * _xw;
      #endif
      vXw = (modelMatrix * _xw).xyz;`);""",
"""    const XW = `
      vec4 _xw = vec4(transformed, 1.0);
      #ifdef USE_INSTANCING
        _xw = instanceMatrix * _xw;
      #endif
      vXw = (modelMatrix * _xw).xyz;`;
    sh.vertexShader = 'varying vec3 vXw;\\n' + (sh.vertexShader.includes('#include <project_vertex>') ? sh.vertexShader.replace('#include <project_vertex>', '#include <project_vertex>' + XW)
      : sh.vertexShader.replace('gl_Position = projectionMatrix * mvPosition;', 'gl_Position = projectionMatrix * mvPosition;' + XW));""")
story = open(os.path.join(P, 'story.js.txt')).read() + "\nfor (const m_ of [treeMat, wallBMat, roofBMat]) xray(m_, 0, 'land' + m_.id);\n"
R("setTime(tPos);\ndocument.getElementById('loading').remove();", story + "\nsetTime(tPos);\ndocument.getElementById('loading').remove();")
a = s.index("renderer.setAnimationLoop((now) => {"); b = s.index("</script>", a)
s = s[:a] + """renderer.setAnimationLoop((now) => {
  tick(now);
  SU.uTime.value = now / 1000; SU.uPulse.value = 0;
  storyFrame(now);
  if (shearMode && machine.visible && !playing) updateMachine(faceH('75', tPos), now);
  if (XR.uXR.value > 0) { XR.uCam.value.copy(camera.position); XR.uTgt.value.copy(controls.target); }
  if (window.__storyLocked) camera.lookAt(controls.target); else controls.update();
  if (!window.__skip3D) { renderer.render(scene, camera); labelRenderer.render(scene, camera); }
  if (layerOn.labels && (frame++ % 6 === 0)) declutter();
});
""" + s[b:]
os.makedirs(os.path.join(W, 'story'), exist_ok=True)
open(os.path.join(W, 'story', 'index.html'), 'w').write(s)
print('story/index.html', len(s))
