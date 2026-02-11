"""
Convert preview.svg to preview.png
Requires: cairosvg (pip install cairosvg)
"""

try:
    import cairosvg
    cairosvg.svg2png(url='preview.svg', write_to='preview.png', output_width=1200, output_height=800)
    print("✅ Successfully converted preview.svg to preview.png")
except ImportError:
    print("❌ cairosvg not installed. Install with: pip install cairosvg")
except Exception as e:
    print(f"❌ Error converting SVG: {e}")
