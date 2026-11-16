# Focused library and platform study prompts

These 20 supplementary prompts complement the 1,200 domain prompts. They are not included in the browser count. Use the linked official resource as reference data, inspect the current source, and preserve the product brief. Report observations separately from recommendations and untested hypotheses.

## T01 — Apple fluid interaction study

Study [Designing Fluid Interfaces](https://developer.apple.com/videos/play/wwdc2018/803/). Extract a compact interaction contract for responsiveness, interruption, redirection and gesture release. Apply it to opening a workspace and immediately changing destination. Draw the state sequence and name the stable anchors. Propose a browser implementation without assuming access to Apple's native APIs or inventing exact Apple animation constants. Deliver a six-step interaction test and a reduced-motion alternative.

## T02 — Native material hierarchy

Read [Apple's material guidance](https://developer.apple.com/design/human-interface-guidelines/materials). Design a web material hierarchy for an architectural-background workspace: atmosphere, readable content, navigation and transient controls. Show why each layer exists, with bright-background and opaque-fallback states. Explain which visual qualities are approximated in CSS and which are not reproduced. Preserve crisp text and avoid stacking glass panels merely for decoration.

## T03 — GNOME spring study

Inspect [Libadwaita SpringAnimation](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/class.SpringAnimation.html) and its linked parameter documentation. Explain damping, initial velocity, target and settling threshold through a drawer released by a gesture. Compare no overshoot with a small settling overshoot. Translate the behavioural intent into the existing web stack without importing native code or claiming identical physics constants. Record the documentation version and test interruption and reduced animation.

## T04 — Ubuntu-style dock placement

Study [Dash to Dock](https://github.com/micheleg/dash-to-dock) as a desktop navigation reference. Design bottom-centred, bottom-leading and edge-mounted alternatives for the real product. Compare workspace obstruction, reach, discoverability, active indicators and small-screen adaptation. Choose one and keep its destinations stable. Do not copy shell window-management semantics blindly into browser routing. Deliver one chosen layout and a feature-location map.

## T05 — Blur placement and cost

Inspect [Blur My Shell](https://github.com/aunetx/blur-my-shell) to understand which shell regions receive materials and what options are exposed. Translate the idea into a bounded web experiment with a static architectural image, one glass dock and an opaque control variant. Measure the resulting page on representative hardware if possible. Identify paint area, idle activity and scrolling behaviour. Report unexecuted measurements honestly; native shell results are not browser benchmarks.

## T06 — Motion layout continuity

Using [Motion layout documentation](https://motion.dev/docs/react-layout-animations), implement an object preview that expands into details and returns to its original location. Preserve focus, scroll position and object identity. Check text and border distortion, repeated object selection and missing shared elements. Prefer a direct state fallback when reduced motion is enabled. Explain which values belong to product state and which are only presentation. Do not defer navigation until motion completes.

## T07 — Motion interruption comparison

Compare a component layout transition with [Motion animateView](https://motion.dev/docs/animate-view) for rapid A → B → C navigation. Inspect current interruption defaults and distinguish queuing from retargeting. Build the smallest experiment that demonstrates behaviour on repeated clicks. Record acknowledgement and destination correctness separately from visual smoothness. Recommend one mechanism for this specific interaction; do not conclude that every transition in the application needs the same mechanism.

## T08 — Aceternity dock adaptation

Inspect [Aceternity Floating Dock](https://ui.aceternity.com/components/floating-dock). Adapt it to the product's four or five actual primary destinations. Replace demo styling with smoked glass, restrained metal and labelled coherent icons. Evaluate magnification, keyboard focus, touch labels and hit-target movement. Preserve active-route semantics and reserve space below content. Deliver a source/dependency note and an interruption test; remove magnification if it reduces precision.

## T09 — Aceternity expansion pattern

Inspect [Aceternity Layout Grid](https://ui.aceternity.com/components/layout-grid) as a reference for preview-to-detail continuity. Rebuild the interaction around a real product object rather than copying the demo's card arrangement. Include close, back, keyboard activation, focus restoration and interrupted selection. Keep all required content reachable when images fail. Show a static fallback and verify that the transition does not stretch reading text or create duplicate interactive objects.

## T10 — Honest stateful buttons

Review [Aceternity Stateful Button](https://ui.aceternity.com/components/stateful-button). Connect its visual states to a real asynchronous operation or a clearly labelled test harness. Model idle, pressed, pending, success and failure without fixed timers that pretend a save succeeded. Preserve labels and focus; prevent duplicate commits only when required. Provide a retry path and a test where the server rejects the action after initial feedback.

## T11 — React Bits glass compatibility

Inspect [Glass Surface source](https://raw.githubusercontent.com/DavidHDev/react-bits/main/src/content/Components/GlassSurface/GlassSurface.jsx), including CSS and feature checks. Evaluate it for a small workspace picker, not every content card. Compare SVG and fallback rendering on the target browser set. Check text contrast, resizing, high contrast and opaque mode. Report actual observed support rather than converting source browser detection into a universal compatibility claim. Keep a simpler CSS surface as a comparison.

## T12 — React Bits Fluid Glass evaluation

Inspect [Fluid Glass source](https://raw.githubusercontent.com/DavidHDev/react-bits/main/src/content/Components/FluidGlass/FluidGlass.jsx). List the rendering dependencies and assets required for the selected effect. Compare a still render, CSS translucency and live transmission rendering in one bounded region. Assess whether the task benefits from live interaction. Include canvas failure, inactive tab, resizing and reduced effects. Keep essential navigation in accessible DOM controls. Recommend the simplest option that retains the desired visual outcome.

## T13 — React Bits dock usability

Inspect [Dock source](https://raw.githubusercontent.com/DavidHDev/react-bits/main/src/content/Components/Dock/Dock.jsx). Evaluate its pointer-driven sizing against keyboard and touch use. Adapt optical icon sizes and visible labels to the product. Test rapid travel across icons, active selection, long translated names and mobile overflow. Maintain consistent target positions where possible. Deliver behavioural changes and their rationale, not just a new palette.

## T14 — React Spring alternative

Evaluate [React Spring](https://github.com/pmndrs/react-spring) for a draggable panel with a constrained release. Compare the implementation burden with the animation mechanism already installed. Test grabbing the panel while it is settling, cancelling a gesture and changing its target. Preserve direct pointer tracking and keyboard alternatives. Recommend adopting it only if this task benefits enough to justify the dependency; avoid two engines controlling the same property.

## T15 — SVG sequence with Anime.js

Inspect [Anime.js](https://github.com/juliangarnier/anime) and current SVG documentation. Design one stateful save icon with clear idle, pending, success and failure meanings. Prefer group transforms if they suffice; justify any path morph. Integrate cleanup with component lifetime and ensure rapid repeated state changes converge correctly. Provide static SVG states for reduced motion. Compare the result with a CSS-only version before introducing a new engine.

## T16 — GSAP boundary study

Evaluate [GSAP](https://github.com/greensock/GSAP) for one optional art-directed workspace introduction. Keep routine navigation and all content usable without the sequence. Define skip, interruption, cleanup and reduced-motion behaviour. Inspect the current license and exact plugins used. Compare against a short CSS/Motion transition and remove the sequence if it adds waiting or fails to communicate product context. Do not add scroll hijacking to the main workspace.

## T17 — Animated primitive audit

Inspect one menu or dialog from [Animate UI](https://github.com/imskyleen/animate-ui) and the product's existing accessible primitive. Compare focus management, Escape, outside click, touch, interruption and reduced motion. Keep the better semantics and adapt only the visual treatment needed by the brief. Deliver a small before/after interaction matrix, dependencies and any missing behaviour. A visually polished demo is not automatic accessibility evidence.

## T18 — Selective component collection use

Review [Magic UI](https://github.com/magicuidesign/magicui) for a single useful pattern such as an interactive control or bounded reveal. Explain where it supports a user task. Remove decorative loops and effects that compete with content. Integrate the product's material and motion tokens, then test repeated use rather than only first impression. Deliver a retain, simplify or reject decision with evidence for that component.

## T19 — Live 3D versus rendered depth

Evaluate [React Three Fiber](https://github.com/pmndrs/react-three-fiber) for an architectural background with controllable perspective. First define whether users need to manipulate the scene. Compare a static image, a two-layer depth effect and live 3D. Document asset transfer, initialization, frame work, idle use and failure recovery where measurable. Preserve plain-background mode and legible content. Choose live 3D only when its task or experiential value justifies the measured cost.

## T20 — Gesture and accessible surface integration

Use [Use Gesture](https://github.com/pmndrs/use-gesture) as a reference for input handling and [Radix Primitives](https://github.com/radix-ui/primitives) as a reference for accessible controls. Design a touch-friendly contextual inspector with a non-drag way to open, resize and close it. Avoid conflicting scroll and drag gestures. Test pointer cancellation, keyboard focus and interruption. Reuse the product's existing capabilities before adding packages and explain ownership of gesture, focus and animation state.
