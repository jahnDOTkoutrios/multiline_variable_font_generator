# Multiline Variable Font Generator

This project generates multiline variable fonts using Glyphs 3. The setup involves creating a custom script that works with Glyphs' variable font capabilities to produce fonts with multiple line variations.

## Glyphs Setup

### Masters Configuration

The font uses a two-master setup in Glyphs:

1. **Regular Master**

   - Base weight and width
   - Standard line thickness
   - Reference point for interpolation

2. **Bold Master**
   - Increased weight
   - Modified line thickness
   - Used for weight axis interpolation

### Axis Configuration

The font supports the following axes:

- **Weight (wght)**: Controls the thickness of the lines
  - Range: 100-900
  - Default: 400
  - Regular Master: 400
  - Bold Master: 900

### Layer Setup

Each glyph contains multiple layers:

1. **Background Layer**

   - Contains the base shape
   - Used as reference for line generation

2. **Line Layers**
   - Multiple layers for different line variations
   - Each layer represents a different line configuration
   - Named according to their position (e.g., "Line 1", "Line 2", etc.)

### Script Integration

The Python script (`250416_multi_line_var.py`) is designed to work with Glyphs 3 and performs the following functions:

1. Generates multiple line variations for each glyph
2. Sets up proper interpolation between masters
3. Configures the variable font axes
4. Handles layer management and naming

## Usage

1. Open your font in Glyphs 3
2. Run the script from the Scripts menu
3. The script will:
   - Generate line variations
   - Set up masters
   - Configure interpolation
   - Prepare the font for export

## Requirements

- Glyphs 3
- Python 3.x
- Basic understanding of variable font concepts

## Notes

- Ensure your glyphs have proper background layers before running the script
- The script assumes a two-master setup (Regular and Bold)
- Line variations are generated based on the background layer
- Interpolation is handled automatically between masters
