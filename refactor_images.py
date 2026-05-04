import os
import re
import json
import shutil

def extract_year(filename):
    m1 = re.search(r'(?:reading|Reading)_(\d+)', filename, re.IGNORECASE)
    if m1:
        if len(m1.group(1)) == 4: return int(m1.group(1))
        if len(m1.group(1)) == 2:
            yr = int(m1.group(1))
            return 1900 + yr if yr > 50 else 2000 + yr
            
    m2 = re.search(r'(?:reading|poster|leeds)[-_]*(\d{4})', filename, re.IGNORECASE)
    if m2: return int(m2.group(1))
    
    if 'Reading1988' in filename or 'reading1988' in filename: return 1988
    if 'Reading-and-Leeds-Poster' in filename: return 2013
    
    m3 = re.search(r'(\d{4})', filename)
    if m3: return int(m3.group(1))
    return None

def main():
    if not os.path.exists('images'):
        os.makedirs('images')
        
    # Read index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Extract posters
    match = re.search(r'let posters = (\[.*?\]);', html, flags=re.DOTALL)
    if not match:
        print("Could not find posters array in index.html")
        return
        
    posters = json.loads(match.group(1))
    
    for p in posters:
        old_url = p['src']
        filename = old_url.split('/')[-1]
        
        year = extract_year(filename)
        if not year:
            print(f"Could not extract year from {filename}")
            continue
            
        ext = filename.split('.')[-1]
        new_filename = f"poster_{year}.{ext}"
        new_path = f"images/{new_filename}"
        
        # Move file if it exists locally
        if os.path.exists(filename):
            shutil.move(filename, new_path)
            print(f"Moved {filename} to {new_path}")
        else:
            print(f"File {filename} not found locally, skipping move.")
            
        # Update src
        p['src'] = new_path
        
    # Replace in HTML
    new_posters_json = json.dumps(posters, indent=2)
    new_html = html[:match.start(1)] + new_posters_json + html[match.end(1):]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    # Also update reading_posters.json if it exists
    if os.path.exists('reading_posters.json'):
        with open('reading_posters.json', 'w', encoding='utf-8') as f:
            json.dump(posters, f, indent=2)

if __name__ == "__main__":
    main()
