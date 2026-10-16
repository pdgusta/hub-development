# Advanced Reference: Component Patterns & Code Templates

This file contains advanced patterns and code templates to reference when implementing specific tasks.

## Table of Contents

1. [Responsive Slide Engine](#responsive-slide-engine)
2. Color System Best Practices
3. Font Recommendations
4. Color x Font Pairing Reference

---

## Responsive Slide Engine

For building fixed-size presentations that auto-fit to any viewport.

**Key conventions**:
- Internal arrays use 0-indexed, **but numbers displayed to the user are always 1-indexed**
- Each `<section class="slide">` gets `data-screen-label="01 Title"`, `data-screen-label="02 Agenda"`, etc. for easy reference
- Control buttons go **outside** the `.stage` scaled container to ensure usability on small screens

```html
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { 
    background: #000; 
    display: flex; 
    align-items: center; 
    justify-content: center;
    height: 100vh;
    overflow: hidden;
    font-family: system-ui, sans-serif;
  }
  .stage {
    width: 1920px;
    height: 1080px;
    position: relative;
    transform-origin: center center;
  }
  .slide {
    position: absolute;
    inset: 0;
    display: none;
    padding: 80px;
  }
  .slide.active { display: flex; }
  .controls {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 12px;
    z-index: 1000;
  }
  .controls button {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    background: rgba(255,255,255,0.15);
    color: white;
    cursor: pointer;
    font-size: 14px;
  }
  .slide-counter {
    position: fixed;
    bottom: 20px;
    right: 20px;
    color: rgba(255,255,255,0.6);
    font-size: 14px;
  }
</style>

<script>
  // Auto-fit scaling
  function scaleStage() {
    const stage = document.querySelector('.stage');
    const scaleX = window.innerWidth / 1920;
    const scaleY = window.innerHeight / 1080;
    const scale = Math.min(scaleX, scaleY);
    stage.style.transform = `scale(${scale})`;
  }
  window.addEventListener('resize', scaleStage);
  scaleStage();

  // Slide navigation
  let current = parseInt(localStorage.getItem('slideIndex') || '0');
  const slides = document.querySelectorAll('.slide');
  
  function showSlide(n) {
    current = Math.max(0, Math.min(n, slides.length - 1));
    slides.forEach((s, i) => s.classList.toggle('active', i === current));
    localStorage.setItem('slideIndex', current);
    // Display 1-indexed to user, store 0-indexed internally
    document.querySelector('.slide-counter').textContent = `${current + 1} / ${slides.length}`;
  }
  
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === ' ') showSlide(current + 1);
    if (e.key === 'ArrowLeft') showSlide(current - 1);
  });
  
  showSlide(current);
</script>
```

---

## Color System Best Practices

Use oklch to define a harmonious color system:

```css
:root {
  /* oklch-based color system */
  --primary-h: 250;  /* hue */
  --primary: oklch(0.55 0.25 var(--primary-h));
  --primary-light: oklch(0.75 0.15 var(--primary-h));
  --primary-dark: oklch(0.35 0.2 var(--primary-h));
  
  /* Neutrals */
  --gray-50: oklch(0.98 0.002 250);
  --gray-100: oklch(0.96 0.004 250);
  --gray-200: oklch(0.92 0.006 250);
  --gray-300: oklch(0.87 0.008 250);
  --gray-400: oklch(0.71 0.01 250);
  --gray-500: oklch(0.55 0.014 250);
  --gray-600: oklch(0.45 0.014 250);
  --gray-700: oklch(0.37 0.014 250);
  --gray-800: oklch(0.27 0.014 250);
  --gray-900: oklch(0.21 0.014 250);
}
```

---

## Font Recommendations (Non-default Choices)

> ⚠️ **These are experience-based suggestions, not hard rules.**
> - Always prefer fonts already specified by the brand or design system; only refer to this table when the user hasn't provided any font scheme.
> - The only hard rule: **Avoid Inter / Roboto / Arial / Fraunces / system-ui — fonts overused by AI-generated content** that instantly signal "this was assembled by AI."
> - When choosing fonts, focus on "personality fit" rather than "what's trendy." The table below lists common high-quality choices, not an exhaustive list.

| Use Case | Recommendation | Google Fonts Name |
|------|------|------------------|
| Modern headings | Plus Jakarta Sans | Plus+Jakarta+Sans |
| Elegant body text | Outfit | Outfit |
| Technical feel | Space Grotesk | Space+Grotesk |
| Premium brand | Sora | Sora |
| Editorial feel | Newsreader | Newsreader |
| Handwritten style | Caveat | Caveat |
| Monospace / code | JetBrains Mono | JetBrains+Mono |

Fonts must be stored inside the project (no hotlink to Google Fonts in this copy).

---

## Color × Font Pairing Reference

> ⚠️ **These are experience-based pairing suggestions, not hard rules.** When you have **absolutely no design context**, pick one as a starting point — it's far better than starting from Inter + #3b82f6.
> Once the user provides a brand / design system / reference site, drop this table immediately and follow their materials.

For quickly establishing a visual system with personality:

| Style | Primary Color (oklch) | Font Pairing | Best For |
|---|---|---|---|
| Modern tech | `oklch(0.55 0.25 250)` blue-violet | Space Grotesk + Inter | SaaS, dev tools, AI products |
| Elegant editorial | `oklch(0.35 0.10 30)` warm brown | Newsreader + Outfit | Content platforms, blogs, editorial |
| Premium brand | `oklch(0.20 0.02 250)` near-black | Sora + Plus Jakarta Sans | Luxury, consulting, finance |
| Lively consumer | `oklch(0.70 0.20 30)` coral | Plus Jakarta Sans + Outfit | E-commerce, lifestyle, social |
| Minimal professional | `oklch(0.50 0.15 200)` teal-blue | Outfit + Space Grotesk | Data products, dashboards, B2B |
| Artisan warmth | `oklch(0.55 0.15 80)` caramel | Caveat (decorative) + Newsreader | Food & beverage, education, creative |

Avoid these combos:
- ❌ Inter + Roboto + blue buttons (peak AI aesthetic)
- ❌ Fraunces + purple-pink gradients (overused)
- ❌ More than three font families (visual chaos)
