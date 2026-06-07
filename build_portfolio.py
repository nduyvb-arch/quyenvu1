# -*- coding: utf-8 -*-
import sys, json, os, html
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document

# Load images data
with open('d:/PORTFOLIO_THREAD/quyenvu/images_data.json', 'r') as f:
    images_data = json.load(f)

def get_docx_content(week):
    fname = f'd:/PORTFOLIO_THREAD/quyenvu/w{week}.docx'
    doc = Document(fname)
    paras = []
    for para in doc.paragraphs:
        if para.text.strip():
            paras.append(para.text.strip())
    return paras

# Get content for all weeks
week_content = {}
for w in range(1, 7):
    week_content[w] = get_docx_content(w)
    print(f'W{w}: {len(week_content[w])} paragraphs, first: {week_content[w][0][:50] if week_content[w] else "empty"}')

# Week metadata
weeks_meta = {
    1: {
        'title': 'Tuần 1: Quản lý Tệp & Thư mục',
        'subtitle': 'File Management & Digital Organization',
        'icon': '📁',
        'color': '#f8b4d9',
        'summary': 'Thực hành quản lý tệp tin và thư mục trên hệ điều hành Windows: tạo, đổi tên, sao chép, di chuyển và xóa tệp.'
    },
    2: {
        'title': 'Tuần 2: Nghiên cứu Thông tin',
        'subtitle': 'Research & Information Literacy',
        'icon': '🔍',
        'color': '#b4d9f8',
        'summary': 'Báo cáo nghiên cứu về ứng dụng ngôn ngữ học trong việc học và giảng dạy tiếng Hàn, khảo sát tài liệu khoa học về AI trong học ngoại ngữ.'
    },
    3: {
        'title': 'Tuần 3: Kỹ năng Viết Prompt AI',
        'subtitle': 'AI Prompt Engineering',
        'icon': '🤖',
        'color': '#d4f8b4',
        'summary': 'Nghiên cứu và phát triển kỹ năng viết prompt trong học tập tiếng Hàn: tóm tắt bài đọc, giải thích ngữ pháp và tạo câu hỏi từ vựng.'
    },
    4: {
        'title': 'Tuần 4: Công cụ Hợp tác Trực tuyến',
        'subtitle': 'Online Collaboration Tools',
        'icon': '🤝',
        'color': '#f8d4b4',
        'summary': 'Ứng dụng công cụ hợp tác trực tuyến (Trello, Google Docs, Zalo) trong thực hiện dự án nhóm, quản lý tiến độ và phân công nhiệm vụ.'
    },
    5: {
        'title': 'Tuần 5: AI Tạo sinh & Nội dung Số',
        'subtitle': 'Generative AI & Digital Content',
        'icon': '✨',
        'color': '#e8b4f8',
        'summary': 'Ứng dụng công cụ AI tạo sinh (Claude, DALL-E 3) để xây dựng bài thuyết trình chuyên nghiệp về "Ứng dụng AI trong Giáo dục".'
    },
    6: {
        'title': 'Tuần 6: Sử dụng AI có Trách nhiệm',
        'subtitle': 'Responsible AI Use',
        'icon': '⚖️',
        'color': '#f8f4b4',
        'summary': 'Báo cáo về việc sử dụng AI có trách nhiệm trong học tập và nghiên cứu tại môi trường đại học, phân tích chính sách và đưa ra góc nhìn cá nhân.'
    }
}

def make_image_gallery(week_num):
    imgs = images_data.get(f'w{week_num}', [])
    if not imgs:
        return '<p class="no-images">📷 Tuần này chưa có ảnh minh họa</p>'
    
    html_parts = ['<div class="gallery-grid">']
    for i, img in enumerate(imgs):
        src = f"data:{img['mime']};base64,{img['data']}"
        html_parts.append(f'''
        <div class="gallery-item" onclick="openLightbox('{src}', 'Hình {i+1} - Tuần {week_num}')">
            <img src="{src}" alt="Hình {i+1} tuần {week_num}" loading="lazy">
            <div class="gallery-overlay"><span>🔍 Xem lớn</span></div>
        </div>''')
    html_parts.append('</div>')
    return '\n'.join(html_parts)

def make_content_section(week_num):
    paras = week_content[week_num]
    # Take first 8 paragraphs as content preview
    preview_paras = paras[:12]
    content_parts = []
    for p in preview_paras:
        escaped = html.escape(p)
        content_parts.append(f'<p>{escaped}</p>')
    return '\n'.join(content_parts)

# Build the full HTML
print("Building HTML...")

weeks_html = ''
for w in range(1, 7):
    meta = weeks_meta[w]
    gallery = make_image_gallery(w)
    content = make_content_section(w)
    img_count = len(images_data.get(f'w{w}', []))
    
    weeks_html += f'''
    <section class="week-section" id="week-{w}">
        <div class="week-header" style="--week-color: {meta["color"]}">
            <div class="week-badge">{meta["icon"]} Tuần {w}</div>
            <h2 class="week-title">{meta["title"]}</h2>
            <p class="week-subtitle">{meta["subtitle"]}</p>
            <div class="week-meta">
                <span class="meta-tag">📄 Báo cáo đầy đủ</span>
                <span class="meta-tag">🖼️ {img_count} hình ảnh</span>
            </div>
        </div>
        
        <div class="week-body">
            <div class="week-summary-card">
                <h3>📋 Tóm tắt bài học</h3>
                <p>{meta["summary"]}</p>
            </div>
            
            <div class="week-tabs">
                <button class="tab-btn active" onclick="showTab(this, 'content-{w}')">📝 Nội dung</button>
                <button class="tab-btn" onclick="showTab(this, 'gallery-{w}')">🖼️ Hình ảnh</button>
            </div>
            
            <div id="content-{w}" class="tab-panel active">
                <div class="doc-content">
                    {content}
                </div>
            </div>
            
            <div id="gallery-{w}" class="tab-panel">
                {gallery}
            </div>
        </div>
    </section>
'''

full_html = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Portfolio học phần Nhập môn Công nghệ số và AI - Vũ Khánh Quyên - ĐHNN ĐHQG Hà Nội">
    <title>Portfolio | Vũ Khánh Quyên | Công nghệ số & AI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --pastel-pink: #ffd6e7;
            --pastel-blue: #c8e6ff;
            --pastel-mint: #c8f5e4;
            --pastel-lavender: #e8d5ff;
            --pastel-peach: #ffe8d0;
            --pastel-yellow: #fff9c4;
            --pastel-rose: #fce4ec;
            --bg-main: #fef9f5;
            --bg-card: #ffffff;
            --text-dark: #3d2b4f;
            --text-mid: #6b5a7a;
            --text-light: #9b8aab;
            --accent-purple: #c084fc;
            --accent-pink: #f472b6;
            --accent-blue: #60a5fa;
            --shadow-soft: 0 4px 24px rgba(192, 132, 252, 0.12);
            --shadow-hover: 0 8px 40px rgba(192, 132, 252, 0.22);
            --border-radius: 20px;
            --border-light: 1px solid rgba(192, 132, 252, 0.15);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: \'Be Vietnam Pro\', sans-serif;
            background: var(--bg-main);
            color: var(--text-dark);
            line-height: 1.7;
            overflow-x: hidden;
        }

        /* Floating background shapes */
        body::before {
            content: \'\';
            position: fixed;
            top: -200px;
            right: -200px;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(255, 214, 231, 0.4), transparent 70%);
            pointer-events: none;
            z-index: 0;
        }
        body::after {
            content: \'\';
            position: fixed;
            bottom: -200px;
            left: -200px;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(200, 230, 255, 0.4), transparent 70%);
            pointer-events: none;
            z-index: 0;
        }

        /* NAV */
        nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
            background: rgba(255, 249, 245, 0.85);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(192, 132, 252, 0.12);
            padding: 0 2rem;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .nav-brand {
            font-weight: 700;
            font-size: 1.1rem;
            color: var(--text-dark);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .nav-brand span {
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-links {
            display: flex;
            gap: 4px;
            list-style: none;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-mid);
            font-size: 0.85rem;
            font-weight: 500;
            padding: 6px 14px;
            border-radius: 20px;
            transition: all 0.3s ease;
        }

        .nav-links a:hover {
            background: var(--pastel-lavender);
            color: var(--text-dark);
        }

        /* HERO */
        .hero {
            position: relative;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 80px 2rem 4rem;
            overflow: hidden;
        }

        .hero-bg-blobs {
            position: absolute;
            inset: 0;
            z-index: 0;
            pointer-events: none;
        }

        .blob {
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.5;
            animation: blobFloat 8s ease-in-out infinite;
        }

        .blob-1 {
            width: 400px; height: 400px;
            background: var(--pastel-pink);
            top: 5%; left: -5%;
            animation-delay: 0s;
        }
        .blob-2 {
            width: 350px; height: 350px;
            background: var(--pastel-blue);
            top: 10%; right: 0%;
            animation-delay: 2s;
        }
        .blob-3 {
            width: 300px; height: 300px;
            background: var(--pastel-mint);
            bottom: 10%; left: 15%;
            animation-delay: 4s;
        }
        .blob-4 {
            width: 250px; height: 250px;
            background: var(--pastel-lavender);
            bottom: 5%; right: 10%;
            animation-delay: 1s;
        }

        @keyframes blobFloat {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(20px, -20px) scale(1.05); }
            66% { transform: translate(-10px, 15px) scale(0.97); }
        }

        .hero-content {
            position: relative;
            z-index: 1;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: white;
            border: 1px solid rgba(192, 132, 252, 0.25);
            border-radius: 50px;
            padding: 8px 20px;
            font-size: 0.85rem;
            color: var(--text-mid);
            font-weight: 500;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-soft);
            animation: fadeInDown 0.8s ease forwards;
        }

        .hero-badge .dot {
            width: 8px; height: 8px;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.4); opacity: 0.7; }
        }

        .hero h1 {
            font-family: \'Playfair Display\', serif;
            font-size: clamp(2.8rem, 6vw, 5rem);
            font-weight: 700;
            line-height: 1.15;
            margin-bottom: 1rem;
            animation: fadeInUp 0.8s ease 0.1s forwards;
            opacity: 0;
        }

        .hero h1 .gradient-text {
            background: linear-gradient(135deg, #c084fc, #f472b6, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-name {
            font-size: clamp(1.2rem, 3vw, 1.8rem);
            color: var(--text-mid);
            font-weight: 400;
            margin-bottom: 0.5rem;
            animation: fadeInUp 0.8s ease 0.2s forwards;
            opacity: 0;
        }

        .hero-info {
            font-size: 0.95rem;
            color: var(--text-light);
            margin-bottom: 2.5rem;
            animation: fadeInUp 0.8s ease 0.3s forwards;
            opacity: 0;
        }

        .hero-stats {
            display: flex;
            gap: 2rem;
            justify-content: center;
            margin-bottom: 3rem;
            animation: fadeInUp 0.8s ease 0.4s forwards;
            opacity: 0;
        }

        .stat-card {
            background: white;
            border-radius: 16px;
            padding: 1.2rem 1.8rem;
            border: var(--border-light);
            box-shadow: var(--shadow-soft);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-hover);
        }

        .stat-number {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stat-label {
            font-size: 0.8rem;
            color: var(--text-light);
            font-weight: 500;
        }

        .hero-cta {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
            color: white;
            padding: 14px 32px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1rem;
            text-decoration: none;
            box-shadow: 0 8px 24px rgba(192, 132, 252, 0.35);
            transition: all 0.3s ease;
            animation: fadeInUp 0.8s ease 0.5s forwards;
            opacity: 0;
        }

        .hero-cta:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(192, 132, 252, 0.5);
        }

        /* SCROLL INDICATOR */
        .scroll-indicator {
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            color: var(--text-light);
            font-size: 0.8rem;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateX(-50%) translateY(0); }
            50% { transform: translateX(-50%) translateY(8px); }
        }

        /* MAIN CONTENT */
        main {
            position: relative;
            z-index: 1;
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem 1.5rem 6rem;
        }

        /* WEEK SECTION */
        .week-section {
            margin-bottom: 3rem;
            background: var(--bg-card);
            border-radius: var(--border-radius);
            overflow: hidden;
            border: var(--border-light);
            box-shadow: var(--shadow-soft);
            transition: box-shadow 0.3s ease;
        }

        .week-section:hover {
            box-shadow: var(--shadow-hover);
        }

        .week-header {
            padding: 2.5rem;
            background: linear-gradient(135deg, color-mix(in srgb, var(--week-color) 60%, white), color-mix(in srgb, var(--week-color) 30%, white));
            position: relative;
            overflow: hidden;
        }

        .week-header::before {
            content: \'\';
            position: absolute;
            top: -30%;
            right: -5%;
            width: 250px;
            height: 250px;
            background: rgba(255,255,255,0.35);
            border-radius: 50%;
        }

        .week-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: white;
            border-radius: 50px;
            padding: 6px 16px;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 1rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }

        .week-title {
            font-size: clamp(1.3rem, 3vw, 1.8rem);
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 0.4rem;
        }

        .week-subtitle {
            color: var(--text-mid);
            font-size: 0.95rem;
            font-weight: 400;
            margin-bottom: 1rem;
        }

        .week-meta {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .meta-tag {
            background: rgba(255,255,255,0.7);
            border-radius: 50px;
            padding: 4px 14px;
            font-size: 0.8rem;
            font-weight: 500;
            color: var(--text-mid);
        }

        .week-body {
            padding: 2rem;
        }

        .week-summary-card {
            background: linear-gradient(135deg, #fdf4ff, #f0f8ff);
            border-radius: 14px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(192, 132, 252, 0.12);
        }

        .week-summary-card h3 {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-dark);
            margin-bottom: 0.7rem;
        }

        .week-summary-card p {
            color: var(--text-mid);
            font-size: 0.93rem;
            line-height: 1.7;
        }

        /* TABS */
        .week-tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 1.5rem;
        }

        .tab-btn {
            padding: 9px 20px;
            border: 1.5px solid rgba(192, 132, 252, 0.2);
            border-radius: 50px;
            background: white;
            color: var(--text-mid);
            font-family: \'Be Vietnam Pro\', sans-serif;
            font-size: 0.88rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.25s ease;
        }

        .tab-btn:hover {
            border-color: var(--accent-purple);
            color: var(--accent-purple);
        }

        .tab-btn.active {
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
            color: white;
            border-color: transparent;
            box-shadow: 0 4px 16px rgba(192, 132, 252, 0.3);
        }

        .tab-panel {
            display: none;
        }

        .tab-panel.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* DOC CONTENT */
        .doc-content {
            background: #fafafa;
            border-radius: 14px;
            padding: 1.8rem;
            border: 1px solid rgba(0,0,0,0.05);
            max-height: 400px;
            overflow-y: auto;
        }

        .doc-content::-webkit-scrollbar {
            width: 6px;
        }
        .doc-content::-webkit-scrollbar-track {
            background: #f0f0f0;
            border-radius: 3px;
        }
        .doc-content::-webkit-scrollbar-thumb {
            background: rgba(192, 132, 252, 0.4);
            border-radius: 3px;
        }

        .doc-content p {
            color: var(--text-mid);
            font-size: 0.9rem;
            margin-bottom: 0.8rem;
            line-height: 1.75;
        }

        /* GALLERY */
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 12px;
        }

        .gallery-item {
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            aspect-ratio: 4/3;
            cursor: pointer;
            background: #f0f0f0;
            border: 1px solid rgba(0,0,0,0.06);
        }

        .gallery-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.4s ease;
        }

        .gallery-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom, transparent 50%, rgba(192, 132, 252, 0.7));
            display: flex;
            align-items: flex-end;
            justify-content: center;
            padding-bottom: 12px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .gallery-overlay span {
            color: white;
            font-size: 0.8rem;
            font-weight: 600;
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 20px;
            backdrop-filter: blur(4px);
        }

        .gallery-item:hover img {
            transform: scale(1.05);
        }
        .gallery-item:hover .gallery-overlay {
            opacity: 1;
        }

        .no-images {
            color: var(--text-light);
            text-align: center;
            padding: 3rem;
            font-size: 0.95rem;
            background: #fafafa;
            border-radius: 14px;
        }

        /* LIGHTBOX */
        #lightbox {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(10, 5, 20, 0.92);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            gap: 1rem;
            padding: 2rem;
            backdrop-filter: blur(8px);
        }

        #lightbox.active {
            display: flex;
            animation: fadeIn 0.2s ease;
        }

        #lightbox-img {
            max-width: 90vw;
            max-height: 80vh;
            object-fit: contain;
            border-radius: 12px;
            box-shadow: 0 20px 80px rgba(0,0,0,0.5);
        }

        #lightbox-caption {
            color: rgba(255,255,255,0.7);
            font-size: 0.9rem;
        }

        #lightbox-close {
            position: absolute;
            top: 1.5rem;
            right: 1.5rem;
            background: rgba(255,255,255,0.15);
            border: none;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            color: white;
            font-size: 1.3rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }

        #lightbox-close:hover {
            background: rgba(255,255,255,0.25);
        }

        /* FOOTER */
        footer {
            background: linear-gradient(135deg, #3d2b4f, #1a1025);
            color: rgba(255,255,255,0.7);
            text-align: center;
            padding: 3rem 2rem;
            font-size: 0.9rem;
        }

        footer .footer-name {
            font-size: 1.2rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.5rem;
        }

        footer .footer-links {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 1rem;
        }

        footer .footer-links span {
            color: rgba(192, 132, 252, 0.8);
        }

        /* ANIMATIONS */
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* SECTION HEADING */
        .section-heading {
            text-align: center;
            margin-bottom: 3rem;
            padding-top: 2rem;
        }

        .section-heading h2 {
            font-family: \'Playfair Display\', serif;
            font-size: clamp(1.8rem, 4vw, 2.5rem);
            color: var(--text-dark);
            margin-bottom: 0.7rem;
        }

        .section-heading p {
            color: var(--text-light);
            font-size: 0.95rem;
        }

        .section-divider {
            width: 60px;
            height: 4px;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
            border-radius: 2px;
            margin: 1rem auto;
        }

        /* Responsive */
        @media (max-width: 640px) {
            .hero-stats { flex-wrap: wrap; gap: 1rem; }
            .gallery-grid { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); }
            .nav-links { display: none; }
            .week-header { padding: 1.8rem; }
            .week-body { padding: 1.5rem; }
        }

        /* Scroll reveal */
        .reveal {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.7s ease;
        }
        .reveal.visible {
            opacity: 1;
            transform: translateY(0);
        }
    </style>
</head>
<body>

<!-- NAV -->
<nav>
    <a href="#hero" class="nav-brand">
        🎓 <span>Quyên\'s Portfolio</span>
    </a>
    <ul class="nav-links">
        <li><a href="#week-1">Tuần 1</a></li>
        <li><a href="#week-2">Tuần 2</a></li>
        <li><a href="#week-3">Tuần 3</a></li>
        <li><a href="#week-4">Tuần 4</a></li>
        <li><a href="#week-5">Tuần 5</a></li>
        <li><a href="#week-6">Tuần 6</a></li>
    </ul>
</nav>

<!-- HERO -->
<section class="hero" id="hero">
    <div class="hero-bg-blobs">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
        <div class="blob blob-4"></div>
    </div>
    <div class="hero-content">
        <div class="hero-badge">
            <div class="dot"></div>
            Nhập môn Công nghệ số & AI · 2025–2026
        </div>
        <h1>
            <span class="gradient-text">Digital Portfolio</span><br>
            của Vũ Khánh Quyên
        </h1>
        <p class="hero-name">Trường Đại học Ngoại ngữ – Đại học Quốc gia Hà Nội</p>
        <p class="hero-info">MSV: 25042558 &nbsp;·&nbsp; Lớp: VNU1001_E252063 &nbsp;·&nbsp; Học phần: Công nghệ số</p>
        
        <div class="hero-stats">
            <div class="stat-card">
                <div class="stat-number">6</div>
                <div class="stat-label">Tuần học</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">6</div>
                <div class="stat-label">Bài tập nộp</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">31</div>
                <div class="stat-label">Hình ảnh minh họa</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">AI</div>
                <div class="stat-label">Tích hợp xuyên suốt</div>
            </div>
        </div>
        
        <a href="#week-1" class="hero-cta">
            ✨ Khám phá Portfolio
        </a>
    </div>
    <div class="scroll-indicator">
        <span>Cuộn xuống</span>
        ↓
    </div>
</section>

<!-- WEEKS CONTENT -->
<main>
    <div class="section-heading">
        <h2>Hành trình 6 tuần</h2>
        <div class="section-divider"></div>
        <p>Tổng hợp các bài tập và báo cáo theo từng tuần học</p>
    </div>
    
    WEEKS_PLACEHOLDER
</main>

<!-- LIGHTBOX -->
<div id="lightbox" onclick="closeLightbox(event)">
    <button id="lightbox-close" onclick="closeLightbox()">✕</button>
    <img id="lightbox-img" src="" alt="">
    <p id="lightbox-caption"></p>
</div>

<!-- FOOTER -->
<footer>
    <p class="footer-name">✨ Vũ Khánh Quyên</p>
    <p>Portfolio học phần Nhập môn Công nghệ số & AI</p>
    <div class="footer-links">
        <span>Trường ĐH Ngoại ngữ – ĐHQGHN</span>
        <span>·</span>
        <span>MSV: 25042558</span>
        <span>·</span>
        <span>2025–2026</span>
    </div>
</footer>

<script>
    // Tab switching
    function showTab(btn, panelId) {
        const section = btn.closest('.week-body');
        section.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        section.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(panelId).classList.add('active');
    }

    // Lightbox
    function openLightbox(src, caption) {
        document.getElementById('lightbox-img').src = src;
        document.getElementById('lightbox-caption').textContent = caption;
        document.getElementById('lightbox').classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox(e) {
        if (!e || e.target === document.getElementById('lightbox') || e.target === document.getElementById('lightbox-close')) {
            document.getElementById('lightbox').classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeLightbox({ target: document.getElementById('lightbox') });
    });

    // Scroll reveal
    const reveals = document.querySelectorAll('.week-section');
    reveals.forEach(el => el.classList.add('reveal'));

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.08 });

    reveals.forEach(el => observer.observe(el));

    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
</script>

</body>
</html>'''

full_html = full_html.replace('WEEKS_PLACEHOLDER', weeks_html)

output_path = 'd:/PORTFOLIO_THREAD/quyenvu/portfolio.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

size_kb = os.path.getsize(output_path) / 1024
print(f'Portfolio created! Size: {size_kb:.1f} KB')
print(f'Path: {output_path}')
