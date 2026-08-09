import os
import sys
import json
import urllib.request
from collections import Counter

USERNAME = os.environ.get("GH_USERNAME", "hkgupta005-sketch")
TOKEN = os.environ.get("GH_TOKEN", "")

API = "https://api.github.com"

def gh_get(path):
    req = urllib.request.Request(API + path)
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-stats-script")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get_all_repos(username):
    repos = []
    page = 1
    while True:
        chunk = gh_get(f"/users/{username}/repos?per_page=100&page={page}&type=owner")
        if not chunk:
            break
        repos.extend(chunk)
        if len(chunk) < 100:
            break
        page += 1
    return repos

# ---------------- fetch real data ----------------
user = gh_get(f"/users/{USERNAME}")
repos = get_all_repos(USERNAME)

public_repos = user.get("public_repos", 0)
followers = user.get("followers", 0)
following = user.get("following", 0)
total_stars = sum(r.get("stargazers_count", 0) for r in repos)
total_forks = sum(r.get("forks_count", 0) for r in repos)

lang_counter = Counter()
for r in repos:
    lang = r.get("language")
    if lang:
        lang_counter[lang] += 1
top_langs = lang_counter.most_common(6)
if not top_langs:
    top_langs = [("No public repos yet", 1)]

print("public_repos", public_repos, "followers", followers, "stars", total_stars, "forks", total_forks)
print("top_langs", top_langs)

# ---------------- duotone palette (violet + gold only) ----------------
BG = "#0B0910"
PURPLE = "#7C3AED"
PURPLE_LT = "#A78BFA"
GOLD = "#F5B800"
GOLD_LT = "#FFD666"
TEXT = "#E8E6EA"
MUTED = "#8b8690"
PALETTE = [GOLD, PURPLE, GOLD_LT, PURPLE_LT, GOLD, PURPLE]

CSS = '''
text{font-family:'Segoe UI',Arial,sans-serif}
@keyframes popIn{0%{opacity:0;transform:translateY(10px) scale(.85)}100%{opacity:1;transform:translateY(0) scale(1)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes dash{from{stroke-dashoffset:var(--len)}to{stroke-dashoffset:var(--off)}}
.pop{opacity:0;animation:popIn .5s ease forwards;transform-box:fill-box;transform-origin:center}
.fade{opacity:0;animation:fadeIn .6s ease forwards}
.ring{animation:dash 1.4s ease .3s forwards}
'''

def svg_open(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>'
            f'<defs><style type="text/css"><![CDATA[{CSS}]]></style>'
            f'<linearGradient id="gg" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0%" stop-color="{GOLD}"/><stop offset="100%" stop-color="{PURPLE}"/>'
            f'</linearGradient></defs>'
            f'<rect width="{w}" height="{h}" rx="14" fill="{BG}" stroke="url(#gg)" stroke-width="1.5"/>')

def rank_letter(score):
    if score >= 100: return "S"
    if score >= 50: return "A"
    if score >= 20: return "B"
    if score >= 5: return "C"
    return "D"

score = total_stars * 2 + followers * 1 + public_repos * 1.5 + total_forks
RANK = rank_letter(score)
RANK_PCT = max(0.06, min(1.0, score / 120))

# =====================================================================
# 1. STATS CARD (with rank ring on the right, like standard stats widgets)
# =====================================================================
W, H = 480, 190
svg = [svg_open(W, H, f"{USERNAME} GitHub stats")]
svg.append(f'<text x="24" y="34" font-size="16" font-weight="700" fill="{GOLD}" class="fade" style="animation-delay:.05s">GITHUB STATS</text>')
svg.append(f'<line x1="24" y1="46" x2="{W-150}" y2="46" stroke="#2a2020" stroke-width="1"/>')

stats = [
    ("Public Repos", public_repos, PURPLE_LT),
    ("Total Stars", total_stars, GOLD),
    ("Followers", followers, PURPLE_LT),
    ("Total Forks", total_forks, GOLD),
]
label_x = 24
y = 68
for i, (label, val, col) in enumerate(stats):
    svg.append(f'<g class="fade" style="animation-delay:{0.15 + i*0.1:.2f}s">')
    svg.append(f'<text x="{label_x}" y="{y}" font-size="12.5" fill="{TEXT}">{label}</text>')
    svg.append(f'<text x="{W-150-20}" y="{y}" font-size="14" font-weight="800" fill="{col}" text-anchor="end">{val}</text>')
    svg.append('</g>')
    y += 27

# rank ring
cx, cy, r = W - 78, 105, 46
circumference = 2 * 3.14159265 * r
offset = circumference * (1 - RANK_PCT)
svg.append(f'<g class="pop" style="animation-delay:.4s">')
svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#231b30" stroke-width="7"/>')
svg.append(f'<circle class="ring" style="--len:{circumference:.1f};--off:{offset:.1f}" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#gg)" stroke-width="7" stroke-linecap="round" stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{circumference:.1f}" transform="rotate(-90 {cx} {cy})"/>')
svg.append(f'<text x="{cx}" y="{cy+12}" font-size="30" font-weight="800" fill="{GOLD}" text-anchor="middle">{RANK}</text>')
svg.append(f'<text x="{cx}" y="{cy+40}" font-size="10" fill="{MUTED}" text-anchor="middle" letter-spacing="1.5">RANK</text>')
svg.append('</g>')

svg.append(f'<text x="24" y="{H-16}" font-size="10" fill="{MUTED}" class="fade" style="animation-delay:.9s">Live data &#8226; refreshed automatically via GitHub Actions</text>')
svg.append('</svg>')
with open("stats.svg", "w") as f:
    f.write("".join(svg))

# =====================================================================
# 2. TOP LANGUAGES CARD
# =====================================================================
W2, H2 = 480, 190
total = sum(c for _, c in top_langs) or 1
svg = [svg_open(W2, H2, f"{USERNAME} top languages")]
svg.append(f'<text x="24" y="34" font-size="16" font-weight="700" fill="{GOLD}" class="fade" style="animation-delay:.05s">TOP LANGUAGES</text>')
svg.append(f'<line x1="24" y1="46" x2="{W2-24}" y2="46" stroke="#2a2020" stroke-width="1"/>')

y = 66
for i, (lang, count) in enumerate(top_langs):
    pct = count / total * 100
    col = PALETTE[i % len(PALETTE)]
    bar_max = W2 - 48 - 140
    bar_w = max(4, bar_max * (count / total))
    svg.append(f'<g class="fade" style="animation-delay:{0.15 + i*0.1:.2f}s">')
    svg.append(f'<text x="24" y="{y}" font-size="12.5" fill="{TEXT}">{lang}</text>')
    svg.append(f'<rect x="150" y="{y-11}" width="{bar_max}" height="12" rx="6" fill="#1b1618"/>')
    svg.append(f'<rect x="150" y="{y-11}" width="{bar_w:.1f}" height="12" rx="6" fill="{col}"/>')
    svg.append(f'<text x="{W2-24}" y="{y}" font-size="11.5" fill="{MUTED}" text-anchor="end">{pct:.0f}%</text>')
    svg.append('</g>')
    y += 21

svg.append('</svg>')
with open("langs.svg", "w") as f:
    f.write("".join(svg))

# =====================================================================
# 3. TROPHIES / MILESTONES CARD (real thresholds off real counts, no invented numbers)
# =====================================================================
def tier(value, thresholds):
    label, letter = thresholds[0][1], thresholds[0][2]
    for min_v, lbl, ltr in thresholds:
        if value >= min_v:
            label, letter = lbl, ltr
    return label, letter

repo_tier, repo_ltr = tier(public_repos, [(0, "Starter", "D"), (3, "Builder", "C"), (10, "Prolific", "B"), (25, "Powerhouse", "S")])
star_tier, star_ltr = tier(total_stars, [(0, "New", "D"), (5, "Noticed", "C"), (25, "Rising", "B"), (100, "Popular", "S")])
follower_tier, follower_ltr = tier(followers, [(0, "Newcomer", "D"), (10, "Connected", "C"), (50, "Influencer", "B"), (200, "Community Leader", "S")])

W3, H3 = 480, 172
svg = [svg_open(W3, H3, f"{USERNAME} milestones")]
svg.append(f'<text x="24" y="34" font-size="16" font-weight="700" fill="{GOLD}" class="fade" style="animation-delay:.05s">MILESTONES</text>')
svg.append(f'<line x1="24" y1="46" x2="{W3-24}" y2="46" stroke="#2a2020" stroke-width="1"/>')

badges = [
    ("REPOS", repo_tier, repo_ltr, str(public_repos)),
    ("STARS", star_tier, star_ltr, str(total_stars)),
    ("NETWORK", follower_tier, follower_ltr, str(followers)),
]
bw = (W3 - 48 - 24) / 3
for i, (cat, lbl, ltr, val) in enumerate(badges):
    bx = 24 + i * (bw + 12)
    col = GOLD if i % 2 == 0 else PURPLE_LT
    svg.append(f'<g class="pop" style="animation-delay:{0.15 + i*0.12:.2f}s">')
    svg.append(f'<rect x="{bx:.0f}" y="58" width="{bw:.0f}" height="94" rx="12" fill="#141014" stroke="{col}" stroke-width="1.5"/>')
    svg.append(f'<circle cx="{bx+bw-18:.0f}" cy="70" r="12" fill="{col}"/>')
    svg.append(f'<text x="{bx+bw-18:.0f}" y="74.5" font-size="12" font-weight="800" fill="#141014" text-anchor="middle">{ltr}</text>')
    svg.append(f'<text x="{bx+16:.0f}" y="82" font-size="9.5" fill="{MUTED}" letter-spacing="1.5">{cat}</text>')
    svg.append(f'<text x="{bx+16:.0f}" y="112" font-size="22" font-weight="800" fill="{col}">{val}</text>')
    svg.append(f'<text x="{bx+16:.0f}" y="134" font-size="11" fill="{TEXT}" font-weight="700">{lbl}</text>')
    svg.append('</g>')

svg.append(f'<text x="24" y="{H3-14}" font-size="9.5" fill="{MUTED}" class="fade" style="animation-delay:.9s">Tiers computed live from real GitHub data &#8226; no invented numbers</text>')
svg.append('</svg>')
with open("trophies.svg", "w") as f:
    f.write("".join(svg))

print("done: stats.svg, langs.svg, trophies.svg - rank:", RANK)
