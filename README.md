# Multiline Variable Font Generator

This script creates variable fonts with offset lines in Glyphs 3. It works by duplicating and offsetting lines across multiple masters.

## How it Works

### Line Processing

1. **Base Line (Regular Master)**

   - Start with a single line in the Regular master

2. **Offset Lines (Other Masters)**
   - The script creates multiple copies of the line
   - Each copy is offset by a specific distance
   - Lines are made thicker in each subsequent master

### Master Setup

You need five masters with proper axis setup:

- **Regular Master**: Contains the original line
- **Medium Master**: Duplicates original line and makes duplicate thicker
- **SemiBold Master**: makes both lines thicker
- **Bold Master**: even thicker
- **Black Master**: now the lines have different height and width
