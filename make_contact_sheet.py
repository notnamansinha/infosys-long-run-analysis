from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent
imgs = [Image.open(p).convert("RGB") for p in sorted((root / "output" / "preview_pages").glob("page-*.png"))]
thumb_w = 300
thumbs = []
for i, im in enumerate(imgs, 1):
    h = int(im.height * thumb_w / im.width)
    t = im.resize((thumb_w, h))
    thumbs.append((i, t))
cols = 4
cell_h = max(t.height for _, t in thumbs) + 36
sheet = Image.new("RGB", (cols * 320, ((len(thumbs)+cols-1)//cols) * cell_h), "#DDE3E8")
d = ImageDraw.Draw(sheet)
f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)
for idx, (n, t) in enumerate(thumbs):
    x = (idx % cols) * 320 + 10
    y = (idx // cols) * cell_h + 30
    sheet.paste(t, (x, y))
    d.text((x, 5 + (idx // cols) * cell_h), f"Page {n}", fill="#16324F", font=f)
sheet.save(root / "output" / "report_contact_sheet.png")
print(root / "output" / "report_contact_sheet.png")
