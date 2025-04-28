# MenuTitle: Sync Master Widths
# -*- coding: utf-8 -*-
__doc__="""
Synchronizes all layers and masters to match the width of the first master while maintaining side bearing proportions.
"""

from GlyphsApp import *

def sync_master_widths():
    # Get the current font
    font = Glyphs.font
    
    # Get the selected glyphs
    selected_glyphs = font.selectedLayers
    if not selected_glyphs:
        print("No glyph selected")
        return
    
    # Process each selected glyph
    for layer in selected_glyphs:
        glyph = layer.parent
        
        # Get the first master layer as reference
        first_master = glyph.layers[0]
        if not first_master:
            print(f"No master layers found in {glyph.name}")
            continue
        
        # Store original spacing and calculate proportions
        original_LSB = first_master.LSB
        original_RSB = first_master.RSB
        original_total_sidebearings = original_LSB + original_RSB
        lsb_proportion = original_LSB / original_total_sidebearings if original_total_sidebearings > 0 else 0.5
        
        # Get original glyph width (this will be maintained across masters)
        original_width = first_master.width
        
        # Process all layers
        for current_layer in glyph.layers:
            # Skip if it's the first master (reference)
            if current_layer == first_master:
                continue
            
            # Calculate new sidebearings to maintain original width
            paths_width = current_layer.bounds.size.width
            total_sidebearings = original_width - paths_width
            
            # Apply new sidebearings while maintaining proportions
            current_layer.LSB = total_sidebearings * lsb_proportion
            current_layer.RSB = total_sidebearings * (1 - lsb_proportion)
            
            # Update the layer
            current_layer.updateMetrics()
    
    print("Process completed")

# Run the function
sync_master_widths() 