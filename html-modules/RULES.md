# HTML Module Generation Rules (Memory)

These rules MUST be followed strictly for all remaining Kubernetes modules (Module 2 to Module 24).

## 0. Workflow & Approval Rule (CRITICAL)
- **1-by-1 Execution:** Process ONLY ONE module at a time. Do not generate multiple modules at once.
- **Explicit Approval Required:** Wait for Anas's explicit approval before moving to the next module.
- **Folder Structure:** Har naya module apne ek separate folder mein banaya jayega (e.g., `module-4/module-4.html`).

## 1. Content & Tone (Strict Matching)
- **Strict Content Matching (CRITICAL):** Tumhara (AI ka) banaya hua har HTML module `kubernetes-mastery-lab.md` ke us specific module ke content se 100% match hona chahiye. Lab file mein di gayi koi bhi Analogy, Concept, Hands-on step, Error, ya Best Practice **miss nahi honi chahiye**. Lab document aur HTML module mein 0% mismatch hona chahiye.
- **Language:** Strictly **Roman Urdu**.
- **Tone:** Conversational, easy to understand, well-explained for mastery.
- **NO EMOJIS:** Do not use any emojis in the text, HTML, or images.

## 2. HTML Layout & CSS (Cartoonish Style)
- **Style:** Clean paper background (`#fcf9f2`). Pura dashboard aur tamam modules ek hi **"Cartoonish" (Playful/Neo-brutalism)** style mein hone chahiye (maslan thick borders, solid drop shadows, soft rounded shapes).
- **Logos:** Style cartoonish hoga lekin **LOGOS HAMESHA REAL AUR OFFICIAL HONGEY** (e.g., Kubernetes, Docker ke original logos).
- **Typography:** `Georgia` ya koi soft rounded font. Clean headers with `#2c3e50` and `#4a6fa5` colors.

## 3. Required Sections
Every module must exactly follow this structure:
1. **Badge & Title:** `<div class="badge">Module X</div>` and `<h1>...</h1>`.
2. **Intro Text & Image:** Clean HTML/CSS animated diagram.
3. **Analogy:** `<div class="analogy"><strong>Analogy:</strong> ...</div>`
4. **Concepts:** `<h2>Hum Kya Seekhenge (Concepts)</h2>` with an unordered list.
5. **Hands-on Steps:** `<h2>Hands-on Steps</h2>` with an ordered list.
6. **Errors:** `<div class="error-section"><h3>Errors (Jo hum break karke fix karenge)</h3>...</div>`
7. **Best Practices:** `<div class="best-practice"><h3>Best Practices</h3>...</div>`
8. **Done-Check:** `<h2>Done-Check</h2>`

## 4. Visual Diagrams (HTML/CSS)
- **Style (CRITICAL):** Clean HTML/CSS animated diagrams. **DO NOT use watercolor blob backgrounds or turbulence filters in the HTML diagrams.** Keep the background clean and focus on clear flow animations.
- **Logos (CRITICAL):** You MUST use **REAL/OFFICIAL logos**. Use an `<img src="...">` pointing to their official public SVG URL (e.g., Wikimedia URLs).
- **Detailed Explanatory Text (CRITICAL):** Since the user is a beginner, the text inside the animated diagrams (on nodes, flows, etc.) must be **extremely descriptive and self-explanatory**. 
- **Animation Flow & Direction:** Animation ka flow bilkul clear hona chahiye ke traffic/data kahan se aa raha hai aur kahan ja raha hai. Flow lines ke upar text likhein (e.g., "Traffic coming from User", "Going to Pod") taake ek beginner ko poora concept easily samajh aa jaye.
- **Diagram Info-Text Placement (CRITICAL):** Diagram ko explain karne wala `.info-text` block HAMESHA `<div class="html-diagram">` ke container se **bahar aur neeche** rakhna hai. Isay kabhi bhi absolute position de kar diagram ke andar mat dalo, warna wo animation ko kha jayega (overlap kar dega).
- **Padding/Margin & Overflow Verification (CRITICAL):** HTML likhne se pehle HAR BAR verify karo ke padding, margin, aur absolute elements (jaise sticky notes) sahi jagah par hain. Koi bhi text, image, ya div container se bahar nikal kar cut nahi hona chahiye.
- **Read Rules First:** Har naya module shuru karne se pehle tum (AI) in rules ko lazmi parhoge aur check karoge.

## 5. Footer Signature (Bottom of HTML)
At the very end of the `.container`, use the exact SVG-based footer structure.
**Do not use emojis, use SVGs.**
```html
<div class="footer-signature">
    <!-- SVGs for Profile, Email, LinkedIn -->
    ... (Anas Khan | anas.devops@hotmail.com | devanaskhanops)
</div>
```

## 6. Git Commit & Push (CRITICAL)
- **1-by-1 Commit:** Jab Anas kisi bhi module ko **approve** kar de, toh tum (AI) lazmi taur par usay Git mein add, commit, aur push karoge.
- **Clean Commits:** Har module ka apna ek alag aur clean commit hona chahiye (e.g., `git commit -m "feat: add module 4 - configmaps and secrets"`).
- **Push & GH-Pages Update:** Commit karne ke baad HAMESHA pehle apni branch (`dev`) par `git push` karna hai, aur sath hi `gh-pages` branch ko bhi lazmi update kar ke push karna hai taake live dashboard par naya module foran available ho jaye!
