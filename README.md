# Multiline Variable Font Generator

This script creates variable fonts with offset lines in Glyphs 3. It works by duplicating and offsetting lines across multiple masters. The Glyphs file needs to have 5 Masters with a weight axis setup correctly for all masters.

## How it Works

### Line Processing

1. **Base Line (Regular Master)**

   - Start with a single line in the Regular master
   - Stroke properties change behaviour, set up stroke end, align and path direction correctly


2. **Offset Lines (Other Masters)**
   - The script creates multiple copies of the line
   - Each copy is offset by a specific distance
   - Lines are made thicker in each subsequent master

### Master Setup

You need five masters with proper axis setup:

- **Single Thin**: Contains the original line
- **Double Thin Thin**: Duplicates original line
- **Double Thin Thick**: makes one line thicker
- **Double Thick Thick**: makes the other line thicker
- **Full**: makes lines even thicker
