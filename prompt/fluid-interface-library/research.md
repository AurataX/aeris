# Fluid interfaces: research and design direction

Research checked 1 October 2026. Prepared for Piyush's request for an original, atmospheric workspace, restrained glass and metal, custom icons, useful docks and immediate interaction. The attached text was reviewed as reference material, not executed as instructions.

## What you are describing

The established subjects are **interaction design, motion design, direct manipulation, perceived performance, rendering performance and material design**. There is no single library or officially named discipline that supplies the whole result. “Fluid interaction architecture” is a useful project label, not an industry standard or a particular Apple technology.

Your reference suggests an environment with depth: an architectural or landscape image, a readable working surface, and a small layer of floating controls. Its appeal comes partly from composition and lighting, which can exist in a static image. Fluidity must be assessed through use.

Separate three clocks: time until input is acknowledged, time until visual motion settles, and time until the requested work completes. A control can respond immediately and settle gracefully while remote work continues. Conversely, an animation can run smoothly while making users wait before they can act again.

Apple's *Designing Fluid Interfaces* discusses responsiveness, interruption and redirection, and explains why frame rate alone does not account for a natural feeling. This is the strongest foundational reference for your description. Its native implementations are examples to learn from, not web code to copy. [Apple WWDC18](https://developer.apple.com/videos/play/wwdc2018/803/)

Apple's current motion guidance favours concise feedback and allowing people to cancel motion. My application: the user's next action should take precedence over finishing an ornamental transition. [Apple Motion](https://developer.apple.com/design/human-interface-guidelines/motion?changes=l_9_3)

## The visual direction I recommend

These are design proposals, not sourced requirements:

- **Atmosphere:** one carefully composed architectural image with foreground, middle distance and background. Metallic structures, indirect light and a quiet horizon supply the 3D feeling.
- **Working surface:** calm, high-contrast content with stable text. Let more atmosphere show on home and discovery views; reduce it during writing, modelling, analysis or editing.
- **Navigation:** one stable dock for primary destinations. Compare bottom-centred and bottom-leading placements using the real content and common pointer paths.
- **Utilities:** a compact top-right cluster with a clearly labelled workspace picker, notifications and account. Custom geometry should still communicate familiar actions.
- **Context:** show local tools beside the object being edited or in an anchored shelf. Avoid accumulating several competing global docks.
- **Signature:** choose one recognisable interaction, such as an active dock capsule that smoothly retargets. Keep the rest precise and quiet.

A good still background can deliver substantial depth without a continuous rendering loop. Use live 3D when users need to manipulate a scene, model, light or camera, or when a measured, optional ambient effect materially improves the experience. This is an engineering recommendation; actual costs depend on assets, devices and implementation.

## Vocabulary without the marketing confusion

| Term | What it contributes | What it does not guarantee |
| --- | --- | --- |
| Glassmorphism | Translucency, background diffusion and layered surfaces | Legibility, physical refraction or fast rendering |
| Metallic styling | Directional tonal variation, rim light and apparent material weight | Actual physically based rendering |
| Neumorphism | Soft raised or inset surfaces | Clear affordance; low-contrast edges can be ambiguous |
| Skeuomorphism | Familiar physical references such as knobs or material cues | Usability in every digital task |
| Spatial continuity | A visible relationship between the object before and after an action | Necessity to morph every element |
| Shared-element transition | Matching an object across two presentations | Correct focus or application state |
| Direct manipulation | The object follows the user's action | A reason to add smoothing lag to dragging |
| Spring motion | Position evolves with physical parameters and velocity | Bounce, a fixed duration or automatic responsiveness |
| Micro-interaction | Feedback for a specific action or state change | A need for continuous decoration |

Treat these as a vocabulary for choices. Combining more “morphisms” does not inherently improve the interface.

## Apple, Ubuntu and GNOME: what to borrow

Apple's material guidance separates Liquid Glass controls/navigation from the content layer and cautions against overuse. Borrow that separation: a functional floating layer over clear content. A CSS blur approximation does not reproduce Apple's native material system. [Apple Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

The official iPhone Duo page exists and describes the product's two-display experiences. I did not inspect or measure the particular opening/closing clip you described, so this report does not assign its exact curve, duration or implementation. [Apple iPhone Duo](https://www.apple.com/iphone-duo/)

Ubuntu's desktop guidance provides the GNOME context. Ubuntu Dock's package metadata links to a branch of Dash to Dock; those are useful references for dock placement and window switching. A shell extension is a different execution environment from a React web application. [Ubuntu desktop guide](https://help.ubuntu.com/stable/ubuntu-help/), [Ubuntu Dock package](https://packages.ubuntu.com/en/source/jammy-updates/gnome/gnome-shell-extension-ubuntu-dock), [Dash to Dock source](https://github.com/micheleg/dash-to-dock)

GNOME's Libadwaita exposes spring motion with damping-related overshoot, initial velocity and a settling threshold. Physics-driven settling does not inherently have a fixed duration. Study this to understand release and settling behaviour, not as a JavaScript dependency. The main documentation inspected identifies itself as an alpha development version, so verify the installed stable API before native implementation. [Adw.SpringAnimation](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/class.SpringAnimation.html)

Blur My Shell adds blur to GNOME shell regions. It is a reference for material placement and configurable effects, not evidence that large animated blurs will be inexpensive in a browser. [Blur My Shell source](https://github.com/aunetx/blur-my-shell)

## Libraries and repositories: distinct jobs

These are documented capabilities plus my fit assessment, not comparative runtime benchmarks. No stars-based ranking is used.

| Project | Category | Where I would evaluate it for your direction |
| --- | --- | --- |
| [Motion](https://github.com/motiondivision/motion) | React/JS animation engine | Default candidate for React layout, gestures and spring feedback. Framer Motion is now Motion; a component using it is not another independent engine. |
| [React Spring](https://github.com/pmndrs/react-spring) | Spring-first animation engine | An alternative for physics-oriented or React Three Fiber work. Do not add it alongside Motion merely to animate ordinary buttons. |
| [Anime.js](https://github.com/juliangarnier/anime) | JavaScript animation engine | Consider for targeted SVG and timeline work outside the main component interaction system. |
| [GSAP](https://github.com/greensock/GSAP) | Animation and sequencing toolkit | Consider for complex art-directed sequences; keep routine navigation independent of long timelines. |
| [Aceternity Floating Dock](https://ui.aceternity.com/components/floating-dock) | Copyable UI component | Inspect the desktop/mobile split, magnification and label behaviour. Adapt the interaction, visual language and semantics. |
| [Aceternity Layout Grid](https://ui.aceternity.com/components/layout-grid) | Layout transition example | Study item-to-detail continuity. Supply real back navigation, focus handling and interrupted-state behaviour. |
| [Aceternity Stateful Button](https://ui.aceternity.com/components/stateful-button) | State feedback example | Connect pending and success to real operations. Never inherit demo timers as simulated production success. |
| [React Bits](https://github.com/DavidHDev/react-bits) | Component/effect collection | Shortlist Dock, Glass Surface, Specular Button and Option Wheel from its catalog; each needs its own review. |
| [Animate UI](https://github.com/imskyleen/animate-ui) | Animated component distribution | Evaluate common controls against your interaction contract and existing accessible primitives. |
| [Magic UI](https://github.com/magicuidesign/magicui) | Copyable animated components | Select specific effects for suitable regions; avoid adopting a whole showcase aesthetic by default. |
| [Radix Primitives](https://github.com/radix-ui/primitives) | Accessible interaction primitives | Consider as the structural base for dialogs, menus and popovers; visual styling is a separate layer. |
| [Use Gesture](https://github.com/pmndrs/use-gesture) | Gesture handling | Evaluate for dragging and pinching when gestures are core to the task. Include non-gesture alternatives. |
| [React Three Fiber](https://github.com/pmndrs/react-three-fiber) | React renderer for Three.js | Use for actual manipulable 3D content; it is not required for a 3D-looking wallpaper. |
| [Vaul](https://github.com/emilkowalski/vaul) | React drawer | A useful drawer reference; check current maintenance, compatibility and gesture behaviour before selecting it. |

I examined official documentation and repositories across these families, not thousands of independent Framer Motion libraries. The deliverable contains 1,200 prompts, not a claim of 1,200 library audits.

### A concrete React Bits finding

The inspected Glass Surface source builds SVG displacement filters and includes an alternate rendering class when its support check rejects a browser. Its browser detection explicitly excludes Safari and Firefox from that SVG path. That is component-specific behaviour, not a universal claim that those browsers cannot show glass. [Glass Surface source inspected](https://raw.githubusercontent.com/DavidHDev/react-bits/main/src/content/Components/GlassSurface/GlassSurface.jsx)

Fluid Glass imports Three.js, React Three Fiber, Drei and a transmission material. The maintainer also distinguishes its preset/custom-model approach from Glass Surface. My conclusion: do not use these as interchangeable drop-in skins for standard buttons. [Fluid Glass source](https://raw.githubusercontent.com/DavidHDev/react-bits/main/src/content/Components/FluidGlass/FluidGlass.jsx), [maintainer explanation](https://github.com/DavidHDev/react-bits/discussions/893)

The Dock source is separately inspectable. Test magnification against moving hit targets, keyboard labels and touch behaviour before making it your default navigation. [React Bits Dock source](https://raw.githubusercontent.com/DavidHDev/react-bits/main/src/content/Components/Dock/Dock.jsx)

Licensing is not uniform: Motion and React Spring present MIT licenses; React Bits declares MIT plus Commons Clause, which is not equivalent to plain MIT. GSAP publishes its own standard license. Confirm the exact chosen asset/version, including any paid examples, when adopting code. [React Bits license](https://raw.githubusercontent.com/DavidHDev/react-bits/main/LICENSE.md), [GSAP license](https://gsap.com/community/standard-license/)

## Engineering fluidity

For React, begin with CSS for basic feedback and one interaction engine when needed. Motion layout animations operate through transforms and support shared layouts; scaling can distort children, which needs explicit handling. Native View Transitions capture visual states and can be useful for view-level changes. [Motion layout documentation](https://motion.dev/docs/react-layout-animations)

Do not assume every API with “Motion” in its name behaves the same when interrupted. The current `animateView` documentation says its default approach queues an incoming transition; an immediate interruption option is available. That default could conflict with your desired latest-input behaviour. [Motion view animation documentation](https://motion.dev/docs/animate-view)

Document-level View Transitions and newer element-scoped transitions need separate evaluation. Chrome documents subtree-scoped, concurrent transitions; this does not establish universal browser support. Feature-detect and keep a normal DOM update fallback. [Chrome same-document guide](https://developer.chrome.com/docs/web-platform/view-transitions/same-document), [element-scoped guide](https://developer.chrome.com/docs/css-ui/view-transitions/element-scoped-view-transitions)

Google's rendering guidance recommends transforms and opacity where possible, measurement of paint/layout work, and restraint with `will-change`. Blur, filters and clipping are not blanket performance-safe substitutes. Even transform-based code must be checked in context. [High-performance CSS animation guide](https://web.dev/articles/animations-guide)

INP measures response to click, tap and keyboard interactions through the next paint; it does not measure full network completion, hover quality or animation frame pacing. Its “good” field threshold is at most 200 ms at the 75th percentile, segmented by mobile and desktop. Use separate traces for animation and dragging. [INP definition](https://web.dev/articles/inp)

### Proposed starting targets

These are project hypotheses, not Apple specifications or guarantees:

| Interaction | Starting treatment |
| --- | --- |
| Press | Immediate visible pressed state; do not postpone activation until animation ends |
| Hover/focus finish | Roughly 80–140 ms, small material or icon change |
| Menu/picker | Roughly 120–200 ms, anchored, minimal travel |
| Dock selection | Roughly 160–240 ms perceived settling; retarget during rapid selection |
| Object expansion | Roughly 200–320 ms, only when identity benefits from continuity |
| Direct manipulation | Follow input without decorative easing; optional restrained release settling |
| Reduced motion | Immediate state changes; remove nonessential spatial movement |

A 60 Hz display has about 16.7 ms between refreshes; 120 Hz has about 8.3 ms. These are full frame intervals, not budgets entirely available to JavaScript. Track input response, dropped frames, layout/paint work and resource use on representative hardware. Record before/after traces; do not infer performance from an attractive video.

## Corrections to the pasted master prompt

1. A library choice cannot guarantee fluidity. State management, main-thread work and loading paths still matter.
2. Custom SVGs are a branding choice; familiar stock icons can be excellent. Morphing unrelated paths can cost complexity without improving comprehension.
3. A crossfade is legitimate when it matches the relationship. A container morph is not automatically superior.
4. Avoid automatic percentages of “UI removal.” Map each capability to a discoverable location and test whether people can find it.
5. Keep critical actions available without hover, especially on touch and keyboard.
6. Immediate acknowledgement is not false success. Optimistic updates need a pending model and recovery; React documents rollback/error patterns. [React useOptimistic](https://react.dev/reference/react/useOptimistic)
7. Reduced motion should remove nonessential movement, not simply make every large animation shorter. The relevant WCAG interaction-animation criterion is AAA; adopting it here is a design requirement, not a claim that all motion violates AA. [W3C interaction animation](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
8. Contrast must survive the underlying image. WCAG specifies 4.5:1 for normal text with defined exceptions; target sizing has separate criteria and exceptions. Use larger comfortable targets as a design choice and test the actual composition. [W3C contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [W3C target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

## Practical adoption sequence

First build one representative vertical slice: open a workspace, change an option, select an object, expand details, edit, save, handle failure, and return. Establish the feature map and state model before expanding the visual system. Use real content density rather than empty mockup cards.

Then validate the slice with fast repeated input, slow responses, resizing, keyboard navigation, a bright wallpaper, a long translated label and reduced effects. Preserve unsaved work and focus through every state. Only then propagate the tested primitives across the product.

The included prompt library is systematically composed from 20 domain briefs, 15 interaction assignments and four modes. It is intended to help you run these focused passes across future products. It does not replace product discovery, user testing or profiling.
