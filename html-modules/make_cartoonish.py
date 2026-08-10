import os
import re

# List of files to process
files_to_remove_emojis = [
    '../index.html',
    'index.html',
    'module-5/module-5.html'
]

files_to_upgrade_css = [
    'module-0/module-0.html',
    'module-1/module-1.html',
    'module-2/module-2.html',
    'module-3/module-3.html',
    'module-4/module-4.html'
]

css_injection = """
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&display=swap" rel="stylesheet">
    <style>
        /* Neo-Brutalism Overrides applied by script */
        body {
            font-family: 'Nunito', sans-serif !important;
            background-image: radial-gradient(#e5e0d8 2px, transparent 2px) !important;
            background-size: 30px 30px !important;
        }
        .container {
            border: 4px solid #2c3e50 !important;
            box-shadow: 12px 12px 0px #2c3e50 !important;
            border-radius: 16px !important;
        }
        .html-diagram {
            border: 4px solid #2c3e50 !important;
            box-shadow: 8px 8px 0px #2c3e50 !important;
        }
        .diagram-node, .node, .info-box, .info-text, .info-card {
            border: 3px solid #2c3e50 !important;
            box-shadow: 4px 4px 0px #2c3e50 !important;
            border-radius: 12px !important;
            background-color: #fff !important;
        }
        .diagram-node:hover, .node:hover, .info-box:hover, .info-text:hover, .info-card:hover {
            transform: translate(-2px, -2px) !important;
            box-shadow: 6px 6px 0px #2c3e50 !important;
        }
        h1, h2, h3 {
            font-weight: 900 !important;
            color: #2c3e50 !important;
        }
        .badge {
            border: 2px solid #2c3e50 !important;
            box-shadow: 2px 2px 0px #2c3e50 !important;
        }
    </style>
</head>
"""

# Emoji removal regex (basic approach: remove specific emojis we know we used)
emojis_to_remove = ['✅', '👉', '🚀', '🔒', '➜', '✨']

for filepath in files_to_remove_emojis + files_to_upgrade_css:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove emojis
        for emoji in emojis_to_remove:
            content = content.replace(emoji, '')
            
        # Add CSS if in the upgrade list
        if filepath in files_to_upgrade_css:
            if 'Neo-Brutalism Overrides applied by script' not in content:
                content = content.replace('</head>', css_injection)
                
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Processed {filepath}")
    else:
        print(f"File not found: {filepath}")
