# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Read the HTML file
with open('d:/PORTFOLIO_THREAD/quyenvu/portfolio.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ------- 1. ADD CSS for profile card (insert before </style>) -------
profile_css = '''
        /* PROFILE CARD */
        .profile-card {
            display: flex;
            align-items: center;
            gap: 1.4rem;
            background: rgba(255,255,255,0.72);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(192, 132, 252, 0.22);
            border-radius: 20px;
            padding: 1.4rem 2rem;
            margin: 1.2rem auto 2rem;
            max-width: 560px;
            box-shadow: 0 6px 28px rgba(192, 132, 252, 0.13);
            text-align: left;
            animation: fadeInUp 0.8s ease 0.25s forwards;
            opacity: 0;
        }

        .profile-avatar {
            flex-shrink: 0;
            width: 66px;
            height: 66px;
            border-radius: 50%;
            background: linear-gradient(135deg, #c084fc, #f472b6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            font-weight: 800;
            color: white;
            letter-spacing: 1px;
            box-shadow: 0 4px 16px rgba(192, 132, 252, 0.4);
        }

        .profile-info {
            flex: 1;
        }

        .profile-name {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 0.2rem;
            font-family: 'Be Vietnam Pro', sans-serif;
        }

        .profile-msv {
            font-size: 0.85rem;
            color: var(--accent-purple);
            font-weight: 600;
            margin-bottom: 0.3rem;
        }

        .profile-school {
            font-size: 0.88rem;
            color: var(--text-mid);
            font-weight: 500;
            margin-bottom: 0.6rem;
        }

        .profile-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .profile-tag {
            background: linear-gradient(135deg, rgba(232, 213, 255, 0.7), rgba(200, 230, 255, 0.7));
            border-radius: 50px;
            padding: 3px 12px;
            font-size: 0.78rem;
            font-weight: 500;
            color: var(--text-mid);
            border: 1px solid rgba(192, 132, 252, 0.18);
        }

        @media (max-width: 580px) {
            .profile-card {
                flex-direction: column;
                text-align: center;
                padding: 1.2rem 1.4rem;
            }
            .profile-tags { justify-content: center; }
        }
'''

# Insert CSS before </style>
css_insert_marker = '    </style>'
if css_insert_marker in content:
    content = content.replace(css_insert_marker, profile_css + css_insert_marker)
    print('CSS inserted OK')
else:
    print('CSS marker NOT found')

# ------- 2. REPLACE hero-name and hero-info with profile card -------
old_html = '        <p class="hero-name">Trường Đại học Ngoại ngữ \u2013 Đại học Quốc gia Hà Nội</p>\r\n        <p class="hero-info">MSV: 25042558 &nbsp;·&nbsp; Lớp: VNU1001_E252063 &nbsp;·&nbsp; Học phần: Công nghệ số</p>'

new_html = '''        <div class="profile-card">
            <div class="profile-avatar">VKQ</div>
            <div class="profile-info">
                <h2 class="profile-name">Vũ Khánh Quyên</h2>
                <p class="profile-msv">MSV: 25042558</p>
                <p class="profile-school">🏫 Trường Đại học Ngoại ngữ – Đại học Quốc gia Hà Nội</p>
                <div class="profile-tags">
                    <span class="profile-tag">📚 Lớp: VNU1001_E252063</span>
                    <span class="profile-tag">💻 Nhập môn Công nghệ số &amp; AI</span>
                    <span class="profile-tag">🎓 2025–2026</span>
                </div>
            </div>
        </div>'''

if old_html in content:
    content = content.replace(old_html, new_html)
    print('Hero HTML replaced OK')
else:
    print('Trying LF line endings...')
    old_html_lf = '        <p class="hero-name">Trường Đại học Ngoại ngữ \u2013 Đại học Quốc gia Hà Nội</p>\n        <p class="hero-info">MSV: 25042558 &nbsp;·&nbsp; Lớp: VNU1001_E252063 &nbsp;·&nbsp; Học phần: Công nghệ số</p>'
    if old_html_lf in content:
        content = content.replace(old_html_lf, new_html)
        print('Hero HTML replaced OK (LF)')
    else:
        # Find what we have
        idx = content.find('hero-name')
        if idx >= 0:
            snippet = content[idx-10:idx+300]
            print('Found hero-name at', idx)
            print('Snippet:', repr(snippet[:200]))
        else:
            print('hero-name NOT found in content')

# Also remove the old CSS for hero-name and hero-info since we replaced the elements
# (keep them in case they're used elsewhere, actually just leave them)

# ------- 3. SAVE -------
with open('d:/PORTFOLIO_THREAD/quyenvu/portfolio.html', 'w', encoding='utf-8') as f:
    f.write(content)

import os
size_kb = os.path.getsize('d:/PORTFOLIO_THREAD/quyenvu/portfolio.html') / 1024
print(f'Saved! Size: {size_kb:.1f} KB')
