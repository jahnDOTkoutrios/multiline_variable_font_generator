# MenuTitle: Multi Line Variable 2 Axis 250523
# -*- coding: utf-8 -*-
__doc__="""
Creates multi-line variable font with specified offsets.
"""

from GlyphsApp import *
from GlyphsApp.plugins import *
from GlyphsApp.UI import *
from vanilla import *
import math

# Configuration
# ============
# Offset values for paths
ORIGINAL_OFFSET = -70  # Offset value for original paths in all masters


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
MASTER4_WIDTH = 80
MASTER4_HEIGHT = 80

# Stroke widths for Master 5
MASTER5_ORIGINAL_WIDTH = 80    # Original paths keep their width
MASTER5_ORIGINAL_HEIGHT = 10   # Original paths have reduced height
MASTER5_OFFSET_WIDTH = 10      # Offset paths have reduced width
MASTER5_OFFSET_HEIGHT = 80     # Offset paths keep their height

# Spacing adjustments
SPACING_ADJUSTMENT_MASTER3 = -15  # Spacing adjustment for Master 3
SPACING_ADJUSTMENT_MASTER4 = -30  # Spacing adjustment for Master 4

# Stroke placement
STROKE_PLACEMENT = 0  # 0 = left, 1 = center, 2 = right

def filterForName(name):
    for filter in Glyphs.filters:
        if filter.__class__.__name__ == name:
            return filter

def set_stroke_attributes(path, width, height):
    """Helper function to set stroke attributes with proper line caps"""
    path.attributes['strokeWidth'] = width
    path.attributes['strokeHeight'] = height
    # Don't set line caps here, they will be copied from original path

def create_offset_path(original_path, offset_value, is_centered=False):
    """Helper function to create offset path while preserving stroke attributes"""
    # Create a copy of the path
    offset_path = original_path.copy()
    
    # Adjust offset value if stroke is centered
    if is_centered:
        offset_value = offset_value / 2
    
    # Apply Offset Curve filter with exact parameters
    temp_layer = GSLayer()
    temp_layer.shapes.append(offset_path)
    offsetCurveFilter = filterForName('GlyphsFilterOffsetCurve')
    offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', str(offset_value), str(offset_value), '0', '0.5'])
    
    if len(temp_layer.paths) > 0:
        offset_path = temp_layer.paths[0]
        # Copy all stroke attributes from original path
        for attr in ['lineCapStart', 'lineCapEnd', 'strokeWidth', 'strokeHeight', 'strokePos']:
            if attr in original_path.attributes:
                offset_path.attributes[attr] = original_path.attributes[attr]
    
    return offset_path



def calculate_diagonal_offset(path, desired_distance):
    """
    Calculate the offset vector and correction needed to ensure
    that the measured distance between the duplicated paths at 90 degrees
    is exactly desired_distance.

    Returns (normal_x, normal_y, corrected_offset_per_side)
    """
    if len(path.nodes) < 2:
        return (0, 0, desired_distance)

    node1 = path.nodes[0]
    node2 = path.nodes[1]

    dx = node2.x - node1.x
    dy = node2.y - node1.y

    length = math.hypot(dx, dy)
    if length == 0:
        return (0, 0, desired_distance)

    # Normalize the direction vector
    dx /= length
    dy /= length

    # Calculate the angle
    angle_rad = math.atan2(dy, dx)

    # Normal vector (90 degree rotated)
    normal_x = dy
    normal_y = -dx

    # For horizontal lines (dy ≈ 0), we want to use the full offset
    if abs(dy) < 1e-6:
        return (0, 1, desired_distance / 2)  # Return vertical normal for horizontal lines

    # For vertical lines (dx ≈ 0), we want to use the full offset
    if abs(dx) < 1e-6:
        return (1, 0, desired_distance / 2)  # Return horizontal normal for vertical lines

    # For diagonal lines, calculate the correction factor
    correction_factor = abs(math.sin(angle_rad))  # if measuring horizontally
    if correction_factor == 0:
        correction_factor = 1e-6  # avoid division by zero

    corrected_offset_per_side = (desired_distance / 2) / correction_factor

    return (normal_x, normal_y, corrected_offset_per_side)



class MultiLineVariableUI:
    def __init__(self):
        # Default values
        self.original_offset = -70
        self.min_stroke_width = 10
        self.medium_stroke_width = 35
        self.max_stroke_width = 60
        self.maintain_y_position = True  # Default to True
        
        # Create the window with a reduced height
        self.w = FloatingWindow((400, 340), "Multi Line Variable Settings")
        
        # Create UI elements
        y = 10
        
        # Main offset
        self.w.offset_label = TextBox((10, y, 380, 22), "Main Offset (distance between lines):")
        y += 25
        self.w.original_offset = EditText((10, y, 380, 22), "", callback=self.saveSettings)
        y += 40
        
        # Stroke widths
        self.w.min_stroke_label = TextBox((10, y, 380, 22), "Minimum Stroke Width:")
        y += 25
        self.w.min_stroke_width = EditText((10, y, 380, 22), "", callback=self.saveSettings)
        y += 40
        
        self.w.medium_stroke_label = TextBox((10, y, 380, 22), "Medium Stroke Width:")
        y += 25
        self.w.medium_stroke_width = EditText((10, y, 380, 22), "", callback=self.saveSettings)
        y += 40
        
        self.w.max_stroke_label = TextBox((10, y, 380, 22), "Maximum Stroke Width:")
        y += 25
        self.w.max_stroke_width = EditText((10, y, 380, 22), "", callback=self.saveSettings)
        y += 40
        
        # Add some padding before the button
        y += 20
        
        # Process button with larger size and more padding
        self.w.process_button = Button((10, y, 380, 32), "Process Selected Glyphs", callback=self.process_glyphs)
        
        # Load saved settings
        self.loadSettings()
        
        # Show window
        self.w.open()
    
    def safe_float(self, value, default=0.0):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def saveSettings(self, sender):
        # Save all settings with error handling
        self.original_offset = self.safe_float(self.w.original_offset.get(), -70)
        self.min_stroke_width = self.safe_float(self.w.min_stroke_width.get(), 10)
        self.medium_stroke_width = self.safe_float(self.w.medium_stroke_width.get(), 40)
        self.max_stroke_width = self.safe_float(self.w.max_stroke_width.get(), 80)
    
    def loadSettings(self):
        # Load all settings into UI
        self.w.original_offset.set(str(self.original_offset))
        self.w.min_stroke_width.set(str(self.min_stroke_width))
        self.w.medium_stroke_width.set(str(self.medium_stroke_width))
        self.w.max_stroke_width.set(str(self.max_stroke_width))
    
    def process_glyphs(self, sender):
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
            
            # Store original paths from master layer
            original_paths = [path.copy() for path in glyph.layers[master1.id].paths]
            
            # Get list of all layer IDs to delete (non-master layers)
            layers_to_delete = []
            for current_layer in glyph.layers:
                if not current_layer.isMasterLayer:
                    layers_to_delete.append(current_layer.layerId)
            
            # Delete layers in reverse order to avoid index issues
            for layer_id in sorted(layers_to_delete, reverse=True):
                del glyph.layers[layer_id]
            
            # Clear all paths from master layers
            for master_layer in [glyph.layers[master1.id], glyph.layers[master2.id], glyph.layers[master3.id], glyph.layers[master4.id], glyph.layers[master5.id]]:
                master_layer.clear()
            
            # Get the layers for each master
            layer1 = glyph.layers[master1.id]
            layer2 = glyph.layers[master2.id]
            layer3 = glyph.layers[master3.id]
            layer4 = glyph.layers[master4.id]
            layer5 = glyph.layers[master5.id]
            
            # Store original spacing and calculate proportions
            original_LSB = layer1.LSB
            original_RSB = layer1.RSB
            original_total_sidebearings = original_LSB + original_RSB
            lsb_proportion = original_LSB / original_total_sidebearings if original_total_sidebearings > 0 else 0.5
            
            # Get original glyph width (this will be maintained across masters)
            original_width = layer1.width
            
            # --- Create processed paths: tag originals and duplicates ---
            processed_paths_master1 = []
            processed_paths_other = []
            for path in original_paths:
                is_centered = path.attributes.get('strokePos', 0) == 0
                if is_centered and self.maintain_y_position:
                    # For centered paths, create two offset paths using diagonal logic
                    # First path: shifted in positive direction
                    path1 = path.copy()
                    temp_layer = GSLayer()
                    temp_layer.shapes.append(path1)
                    normal_x, normal_y, offset = calculate_diagonal_offset(path1, self.original_offset)
                    if abs(normal_x) < 1e-6:  # If line is vertical
                        y_offset = offset / normal_y if abs(normal_y) > 1e-6 else offset
                        offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', '0', str(y_offset), '0', '0.5'])
                    else:
                        x_offset = offset / normal_x
                        offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', str(x_offset), '0', '0', '0.5'])
                    if len(temp_layer.paths) > 0:
                        path1 = temp_layer.paths[0]
                        for attr in ['lineCapStart', 'lineCapEnd', 'strokeWidth', 'strokeHeight', 'strokePos']:
                            if attr in path.attributes:
                                path1.attributes[attr] = path.attributes[attr]
                        path1.attributes['mlv_type'] = 'duplicate'
                        path1.attributes['offset_direction'] = 0
                        processed_paths_other.append(path1)
                    # Second path: shifted in negative direction
                    path2 = path.copy()
                    temp_layer = GSLayer()
                    temp_layer.shapes.append(path2)
                    normal_x, normal_y, offset = calculate_diagonal_offset(path2, self.original_offset)
                    if abs(normal_x) < 1e-6:
                        y_offset = -offset / normal_y if abs(normal_y) > 1e-6 else -offset
                        offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', '0', str(y_offset), '0', '0.5'])
                    else:
                        x_offset = -offset / normal_x
                        offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', str(x_offset), '0', '0', '0.5'])
                    if len(temp_layer.paths) > 0:
                        path2 = temp_layer.paths[0]
                        for attr in ['lineCapStart', 'lineCapEnd', 'strokeWidth', 'strokeHeight', 'strokePos']:
                            if attr in path.attributes:
                                path2.attributes[attr] = path.attributes[attr]
                        path2.attributes['mlv_type'] = 'duplicate'
                        path2.attributes['offset_direction'] = 1
                        processed_paths_other.append(path2)
                    # Only add the original to master 1
                    orig = path.copy()
                    orig.attributes['mlv_type'] = 'original'
                    processed_paths_master1.append(orig)
                else:
                    # For non-centered or not maintaining Y, keep original and create offset path
                    orig = path.copy()
                    orig.attributes['mlv_type'] = 'original'
                    processed_paths_master1.append(orig)
                    processed_paths_other.append(orig.copy())
                    offset_path = create_offset_path(path, self.original_offset, is_centered)
                    offset_path.attributes['mlv_type'] = 'duplicate'
                    processed_paths_other.append(offset_path)
            
            # --- Bracket layers: all paths thickness 10 ---
            def add_bracket_layer(master, bracket_layer, thickness):
                bracket_layer.associatedMasterId = master.id
                bracket_layer.attributes["axisRules"] = {} if master==master1 else {"a01": {"max": 100}, "a02": {"max": 100}}
                if master == master1:
                    # For master 1 bracket layer, add only the offset/duplicate paths for centered, and original+offset for non-centered
                    for path in processed_paths_other:
                        new_path = path.copy()
                        set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                        bracket_layer.shapes.append(new_path)
                else:
                    # For other masters, only add original (pre-offset) paths
                    for path in original_paths:
                        new_path = path.copy()
                        set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                        bracket_layer.shapes.append(new_path)
                # Now set LSB/RSB to match the original master width and proportions
                bracket_layer.width = original_width
                paths_width = bracket_layer.bounds.size.width
                total_sidebearings = bracket_layer.width - paths_width
                bracket_layer.LSB = total_sidebearings * lsb_proportion
                bracket_layer.RSB = total_sidebearings * (1 - lsb_proportion)
                bracket_layer.updateMetrics()
                glyph.layers.append(bracket_layer)

            add_bracket_layer(master1, GSLayer(), self.min_stroke_width)
            add_bracket_layer(master2, GSLayer(), self.min_stroke_width)
            add_bracket_layer(master3, GSLayer(), self.min_stroke_width)
            add_bracket_layer(master4, GSLayer(), self.min_stroke_width)
            add_bracket_layer(master5, GSLayer(), self.min_stroke_width)

            # --- Master 1: only original paths (thickness min_stroke_width) ---
            for path in processed_paths_master1:
                if path.attributes.get('mlv_type') == 'original':
                    new_path = path.copy()
                    set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                    layer1.shapes.append(new_path)

            # --- Master 2: original and duplicate as before (use min_stroke_width for both) ---
            for path in processed_paths_other:
                new_path = path.copy()
                set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                layer2.shapes.append(new_path)

            # --- Master 3: original=medium, duplicate=min (for diagonals, offset_direction 0=medium, 1=min) ---
            for path in processed_paths_other:
                new_path = path.copy()
                if path.attributes.get('mlv_type') == 'original':
                    set_stroke_attributes(new_path, self.medium_stroke_width, self.medium_stroke_width)
                elif path.attributes.get('mlv_type') == 'duplicate' and 'offset_direction' in path.attributes:
                    if path.attributes['offset_direction'] == 0:
                        set_stroke_attributes(new_path, self.medium_stroke_width, self.medium_stroke_width)
                    else:
                        set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                else:
                    set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                layer3.shapes.append(new_path)

            # --- Master 4: original=min, duplicate=max (for diagonals, offset_direction 0=min, 1=max) ---
            for path in processed_paths_other:
                new_path = path.copy()
                if path.attributes.get('mlv_type') == 'original':
                    set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                elif path.attributes.get('mlv_type') == 'duplicate' and 'offset_direction' in path.attributes:
                    if path.attributes['offset_direction'] == 0:
                        set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                    else:
                        set_stroke_attributes(new_path, self.max_stroke_width, self.max_stroke_width)
                else:
                    set_stroke_attributes(new_path, self.max_stroke_width, self.max_stroke_width)
                layer4.shapes.append(new_path)

            # --- Master 5: both original and duplicate = max_stroke_width ---
            for path in processed_paths_other:
                new_path = path.copy()
                set_stroke_attributes(new_path, self.max_stroke_width, self.max_stroke_width)
                layer5.shapes.append(new_path)

            # --- Sidebearings and metrics sync ---
            for current_layer in [layer2, layer3, layer4, layer5]:
                paths_width = current_layer.bounds.size.width
                total_sidebearings = original_width - paths_width
                current_layer.LSB = total_sidebearings * lsb_proportion
                current_layer.RSB = total_sidebearings * (1 - lsb_proportion)
                current_layer.updateMetrics()

            # Call sync_master_widths at the end of processing
            sync_master_widths()

# --- Sync all layers' widths and sidebearings to the first master (reference logic) ---
def sync_master_widths():
    font = Glyphs.font
    selected_glyphs = font.selectedLayers
    if not selected_glyphs:
        print("No glyph selected")
        return
    for layer in selected_glyphs:
        glyph = layer.parent
        first_master = glyph.layers[0]
        if not first_master:
            print(f"No master layers found in {glyph.name}")
            continue
        original_LSB = first_master.LSB
        original_RSB = first_master.RSB
        original_total_sidebearings = original_LSB + original_RSB
        lsb_proportion = original_LSB / original_total_sidebearings if original_total_sidebearings > 0 else 0.5
        original_width = first_master.width
        for current_layer in glyph.layers:
            if current_layer == first_master:
                continue
            paths_width = current_layer.bounds.size.width
            total_sidebearings = original_width - paths_width
            current_layer.LSB = total_sidebearings * lsb_proportion
            current_layer.RSB = total_sidebearings * (1 - lsb_proportion)
            current_layer.updateMetrics()
    print("Sync Master Widths: Process completed")

# Run the UI
MultiLineVariableUI()
