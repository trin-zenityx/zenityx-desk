# ZenityX Desk — hero video design

## Palette
- bg: #FFFFFF (pure white — must blend invisibly into the website hero)
- ink: #1d1d1f (headlines)
- sub: #8a8a8e (secondary)
- ghost: #f3f3f5 (oversized background type)
- red: #E8392E (ZenityX accent — cursor, marker, rules)
- red-deep: #B3261E
- ok-green: #2fbf8f (status dot only)

## Typography
- Display/headlines: "IBM Plex Sans Thai" 700, tracking -0.03em
- Meta/labels: "IBM Plex Mono" 500, letterspaced caps

## Motion personality
- Apple-grade restraint: confident springs (back.out, expo.out), no bounce spam
- ZenityX owl mascot = playful counterpoint, used once at the resolve

## What NOT to do
- No emojis, no gradients on text, no dark frames (white canvas throughout)
- No element may sit outside the white canvas look — video edges must stay white

## Render
- Always render at 4K for crisp type on Retina (page shows it at ~1340 CSS px = ~2680 device px):
  `npx hyperframes render . --resolution landscape-4k --quality high`
- Then copy to `hero.mp4` + `../../site/assets/hero.mp4`; poster = frame ~7.8s scaled to 1920w.
