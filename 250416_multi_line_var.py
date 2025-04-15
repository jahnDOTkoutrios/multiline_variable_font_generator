from GlyphsApp import *
from GlyphsApp.plugins import *

# Configuration
# ============
# Offset values for paths
ORIGINAL_OFFSET = -40  # Offset value for original paths in all masters
THICK_OFFSET = 20      # Offset value for thicker paths in Master 3
EXTRA_THICK_OFFSET = 40  # Offset value for extra thick paths in Master 4

# Stroke widths for Master 1
MASTER1_ORIGINAL_WIDTH = 10
MASTER1_ORIGINAL_HEIGHT = 10
MASTER1_OFFSET_WIDTH = 1
MASTER1_OFFSET_HEIGHT = 1

# Stroke widths for Master 2
MASTER2_ORIGINAL_WIDTH = 10
MASTER2_ORIGINAL_HEIGHT = 10
MASTER2_OFFSET_WIDTH = 40
MASTER2_OFFSET_HEIGHT = 40

# Stroke widths for Master 3
MASTER3_WIDTH = 40
MASTER3_HEIGHT = 40

# Stroke widths for Master 4
MASTER4_WIDTH = 60
MASTER4_HEIGHT = 60

# Stroke widths for Master 5
MASTER5_ORIGINAL_WIDTH = 40    # Original paths keep their width
MASTER5_ORIGINAL_HEIGHT = 10   # Original paths have reduced height
MASTER5_OFFSET_WIDTH = 10      # Offset paths have reduced width
MASTER5_OFFSET_HEIGHT = 40     # Offset paths keep their height

# Spacing adjustments
SPACING_ADJUSTMENT_MASTER3 = -15  # Spacing adjustment for Master 3
SPACING_ADJUSTMENT_MASTER4 = -30  # Spacing adjustment for Master 4

# Stroke placement
STROKE_PLACEMENT = 0  # 0 = left, 1 = center, 2 = right

def filterForName(name):
    for filter in Glyphs.filters:
        if filter.__class__.__name__ == name:
            return filter

def process_glyphs():
    # Get the current font
    font = Glyphs.font
    
    # Get the selected glyph
    selected_glyphs = font.selectedLayers
    if not selected_glyphs:
        print("No glyph selected")
        return
    
    # Get all masters
    master1 = font.masters[0]
    master2 = font.masters[1]
    master3 = font.masters[2]
    master4 = font.masters[3]
    master5 = font.masters[4]
    
    # Get the Offset Curve filter
    offsetCurveFilter = filterForName('GlyphsFilterOffsetCurve')
    
    # Process the selected glyph
    for layer in selected_glyphs:
        glyph = layer.parent
        # Get the layers for each master
        layer1 = glyph.layers[master1.id]
        layer2 = glyph.layers[master2.id]
        layer3 = glyph.layers[master3.id]
        layer4 = glyph.layers[master4.id]
        layer5 = glyph.layers[master5.id]
        
        # Store original spacing
        original_LSB = layer1.LSB
        original_RSB = layer1.RSB
        
        # Store original paths
        original_paths = [path.copy() for path in layer1.paths]
        
        # Step 1: Process Master 1
        # Create offset paths for Master 1
        offset_paths = []
        for path in original_paths:
            # Create a copy of the path
            offset_path = path.copy()
            # Apply Offset Curve filter with exact parameters
            temp_layer = GSLayer()
            temp_layer.shapes.append(offset_path)
            offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', str(ORIGINAL_OFFSET), str(ORIGINAL_OFFSET), '0', '0.5'])
            if len(temp_layer.paths) > 0:
                offset_path = temp_layer.paths[0]
            offset_paths.append(offset_path)
        
        # Clear and rebuild Master 1
        layer1.clear()
        # Add original paths with specified stroke
        for path in original_paths:
            path.attributes['strokeWidth'] = MASTER1_ORIGINAL_WIDTH
            path.attributes['strokeHeight'] = MASTER1_ORIGINAL_HEIGHT
            path.attributes['strokePlacement'] = STROKE_PLACEMENT
            layer1.shapes.append(path)
        # Add offset paths with specified stroke
        for path in offset_paths:
            path.attributes['strokeWidth'] = MASTER1_OFFSET_WIDTH
            path.attributes['strokeHeight'] = MASTER1_OFFSET_HEIGHT
            path.attributes['strokePlacement'] = STROKE_PLACEMENT
            layer1.shapes.append(path)
        # Restore original spacing
        layer1.LSB = original_LSB
        layer1.RSB = original_RSB
        
        # Step 2: Process Master 2
        layer2.clear()
        # Add original paths with specified stroke
        for path in original_paths:
            new_path = path.copy()
            new_path.attributes['strokeWidth'] = MASTER2_ORIGINAL_WIDTH
            new_path.attributes['strokeHeight'] = MASTER2_ORIGINAL_HEIGHT
            new_path.attributes['strokePlacement'] = STROKE_PLACEMENT
            layer2.shapes.append(new_path)
        # Add offset paths with specified stroke
        for path in offset_paths:
            new_path = path.copy()
            new_path.attributes['strokeWidth'] = MASTER2_OFFSET_WIDTH
            new_path.attributes['strokeHeight'] = MASTER2_OFFSET_HEIGHT
            new_path.attributes['strokePlacement'] = STROKE_PLACEMENT
            layer2.shapes.append(new_path)
        # Restore original spacing
        layer2.LSB = original_LSB
        layer2.RSB = original_RSB
        
        # Step 3: Process Master 3
        layer3.clear()
        # Add original paths with thicker stroke
        for path in original_paths:
            new_path = path.copy()
            new_path.attributes['strokeWidth'] = MASTER3_WIDTH
            new_path.attributes['strokeHeight'] = MASTER3_HEIGHT
            new_path.attributes['strokePlacement'] = STROKE_PLACEMENT
            layer3.shapes.append(new_path)
        
        # Add offset paths with thicker stroke
        for path in offset_paths:
            new_path = path.copy()
            new_path.attributes['strokeWidth'] = MASTER3_WIDTH
            new_path.attributes['strokeHeight'] = MASTER3_HEIGHT
            new_path.attributes['strokePlacement'] = STROKE_PLACEMENT
            layer3.shapes.append(new_path)
        
        # Restore original spacing
        layer3.LSB = original_LSB
        layer3.RSB = original_RSB
        
        # Step 4: Process Master 4
        layer4.clear()
        # Add original paths with thicker stroke
        for path in original_paths:
            new_path = path.copy()
            new_path.attributes['strokeWidth'] = MASTER4_WIDTH
            new_path.attributes['strokeHeight'] = MASTER4_HEIGHT
            new_path.attributes['strokePlacement'] = STROKE_PLACEMENT
            layer4.shapes.append(new_path)
        
        # Add offset paths with thicker stroke
        for path in offset_paths:
            new_path = path.copy()
            new_path.attributes['strokeWidth'] = MASTER4_WIDTH
            new_path.attributes['strokeHeight'] = MASTER4_HEIGHT
            new_path.attributes['strokePlacement'] = STROKE_PLACEMENT
            layer4.shapes.append(new_path)
        
        # Restore original spacing
        layer4.LSB = original_LSB
        layer4.RSB = original_RSB
        
        # Step 5: Process Master 5
        layer5.clear()
        # Add original paths with specified stroke
        for path in original_paths:
            new_path = path.copy()
            new_path.attributes['strokeWidth'] = MASTER5_ORIGINAL_WIDTH
            new_path.attributes['strokeHeight'] = MASTER5_ORIGINAL_HEIGHT
            new_path.attributes['strokePlacement'] = STROKE_PLACEMENT
            layer5.shapes.append(new_path)
        # Add offset paths with specified stroke
        for path in offset_paths:
            new_path = path.copy()
            new_path.attributes['strokeWidth'] = MASTER5_OFFSET_WIDTH
            new_path.attributes['strokeHeight'] = MASTER5_OFFSET_HEIGHT
            new_path.attributes['strokePlacement'] = STROKE_PLACEMENT
            layer5.shapes.append(new_path)
        # Restore original spacing
        layer5.LSB = original_LSB
        layer5.RSB = original_RSB

# Run the script
process_glyphs()
