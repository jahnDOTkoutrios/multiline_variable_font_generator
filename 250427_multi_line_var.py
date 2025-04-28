# MenuTitle: Multi Line Variable 250427
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

    # ✅ Correct the offset so that the 90° measured distance is accurate
    # The measured distance perpendicular to the path = offset_per_side * 2
    # But we need to account for the slope
    correction_factor = abs(math.sin(angle_rad))  # if measuring horizontally
    if correction_factor == 0:
        correction_factor = 1e-6  # avoid division by zero

    corrected_offset_per_side = (desired_distance / 2) / correction_factor

    # Debug
    LogError("=== Debug Information ===")
    LogError(f"Direction: ({dx:.3f}, {dy:.3f})")
    LogError(f"Normal vector: ({normal_x:.3f}, {normal_y:.3f})")
    LogError(f"Angle: {math.degrees(angle_rad):.2f}°")
    LogError(f"Correction factor: {correction_factor:.3f}")
    LogError(f"Desired perpendicular distance: {desired_distance}")
    LogError(f"Corrected offset per side: {corrected_offset_per_side}")
    LogError("===========================")

    return (normal_x, normal_y, corrected_offset_per_side)



class MultiLineVariableUI:
    def __init__(self):
        # Default values
        self.original_offset = -70
        self.min_stroke_width = 10
        self.medium_stroke_width = 40
        self.max_stroke_width = 80
        self.maintain_y_position = True  # Default to True
        
        # Create the window with a larger height
        self.w = FloatingWindow((400, 400), "Multi Line Variable Settings")
        
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
        
        # Toggle for maintaining Y position
        self.w.maintain_y_position = CheckBox((10, y, 380, 22), "Maintain Y position for diagonal lines", value=True, callback=self.saveSettings)
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
        self.maintain_y_position = self.w.maintain_y_position.get()
    
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
            
            # First, handle the first master - keep original paths exactly as they are
            for path in original_paths:
                layer1.shapes.append(path.copy())
            
            # Create bracket layers for each master
            bracket_layer1 = GSLayer()
            bracket_layer1.associatedMasterId = master1.id
            bracket_layer1.LSB = original_LSB
            bracket_layer1.RSB = original_RSB
            bracket_layer1.attributes["axisRules"] = {}  # Empty bracket layer rules
            
            bracket_layer2 = GSLayer()
            bracket_layer2.associatedMasterId = master2.id
            bracket_layer2.LSB = original_LSB
            bracket_layer2.RSB = original_RSB
            bracket_layer2.attributes["axisRules"] = {"a01": {"max": 120}}
            
            bracket_layer3 = GSLayer()
            bracket_layer3.associatedMasterId = master3.id
            bracket_layer3.LSB = original_LSB
            bracket_layer3.RSB = original_RSB
            bracket_layer3.attributes["axisRules"] = {"a01": {"max": 120}}
            
            bracket_layer4 = GSLayer()
            bracket_layer4.associatedMasterId = master4.id
            bracket_layer4.LSB = original_LSB
            bracket_layer4.RSB = original_RSB
            bracket_layer4.attributes["axisRules"] = {"a01": {"max": 120}}
            
            bracket_layer5 = GSLayer()
            bracket_layer5.associatedMasterId = master5.id
            bracket_layer5.LSB = original_LSB
            bracket_layer5.RSB = original_RSB
            bracket_layer5.attributes["axisRules"] = {"a01": {"max": 120}}
            
            # Process paths for the first bracket layer
            processed_paths = []
            for path in original_paths:
                # Check if stroke is centered
                is_centered = path.attributes.get('strokePos', 0) == 0
                
                if is_centered:
                    # For centered paths, create two offset paths
                    # First path: shifted in positive direction
                    path1 = path.copy()
                    temp_layer = GSLayer()
                    temp_layer.shapes.append(path1)
                    if self.maintain_y_position:
                        # Calculate the normal vector and offset
                        normal_x, normal_y, offset = calculate_diagonal_offset(path1, self.original_offset)
                        # Apply the offset only in X direction using the normal vector's X component
                        x_offset = offset / normal_x
                        offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', str(x_offset), '0', '0', '0.5'])
                    else:
                        # Offset in both X and Y directions
                        offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', str(self.original_offset/2), str(self.original_offset/2), '0', '0.5'])
                    if len(temp_layer.paths) > 0:
                        path1 = temp_layer.paths[0]
                        # Copy all stroke attributes from original path
                        for attr in ['lineCapStart', 'lineCapEnd', 'strokeWidth', 'strokeHeight', 'strokePos']:
                            if attr in path.attributes:
                                path1.attributes[attr] = path.attributes[attr]
                        # Add offset direction attribute
                        path1.attributes['offset_direction'] = 0
                    
                    # Second path: shifted in negative direction
                    path2 = path.copy()
                    temp_layer = GSLayer()
                    temp_layer.shapes.append(path2)
                    if self.maintain_y_position:
                        # Calculate the normal vector and offset
                        normal_x, normal_y, offset = calculate_diagonal_offset(path2, self.original_offset)
                        # Apply the offset only in X direction using the normal vector's X component
                        x_offset = -offset / normal_x
                        offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', str(x_offset), '0', '0', '0.5'])
                    else:
                        # Offset in both X and Y directions
                        offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', str(-self.original_offset/2), str(-self.original_offset/2), '0', '0.5'])
                    if len(temp_layer.paths) > 0:
                        path2 = temp_layer.paths[0]
                        # Copy all stroke attributes from original path
                        for attr in ['lineCapStart', 'lineCapEnd', 'strokeWidth', 'strokeHeight', 'strokePos']:
                            if attr in path.attributes:
                                path2.attributes[attr] = path.attributes[attr]
                        # Add offset direction attribute
                        path2.attributes['offset_direction'] = 1
                    
                    # Add both paths to processed_paths
                    processed_paths.append(path1)
                    processed_paths.append(path2)
                else:
                    # For non-centered paths, keep original and create offset path
                    processed_paths.append(path.copy())
                    offset_path = create_offset_path(path, self.original_offset)
                    processed_paths.append(offset_path)
            
            # Add processed paths to first bracket layer
            for path in processed_paths:
                new_path = path.copy()
                set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                bracket_layer1.shapes.append(new_path)
            
            # Add original paths to other bracket layers
            for path in original_paths:
                # Master 2 bracket layer
                new_path = path.copy()
                set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                bracket_layer2.shapes.append(new_path)
                
                # Master 3 bracket layer
                new_path = path.copy()
                set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                bracket_layer3.shapes.append(new_path)
                
                # Master 4 bracket layer
                new_path = path.copy()
                set_stroke_attributes(new_path, self.medium_stroke_width, self.medium_stroke_width)
                bracket_layer4.shapes.append(new_path)
                
                # Master 5 bracket layer
                new_path = path.copy()
                set_stroke_attributes(new_path, self.max_stroke_width, self.max_stroke_width)
                bracket_layer5.shapes.append(new_path)
            
            # Add the bracket layers to the glyph
            glyph.layers.append(bracket_layer1)
            glyph.layers.append(bracket_layer2)
            glyph.layers.append(bracket_layer3)
            glyph.layers.append(bracket_layer4)
            glyph.layers.append(bracket_layer5)
            
            # Step 1: Process Master 1 (already done, keeping original paths)
            
            # Step 2: Process Master 2
            layer2.clear()
            # Add processed paths with specified stroke
            for path in processed_paths:
                new_path = path.copy()
                set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                layer2.shapes.append(new_path)
            
            # Calculate new sidebearings to maintain original width
            paths_width = layer2.bounds.size.width
            total_sidebearings = original_width - paths_width
            layer2.LSB = total_sidebearings * lsb_proportion
            layer2.RSB = total_sidebearings * (1 - lsb_proportion)
            
            # Update bracket layer 2 sidebearings to match original master
            bracket_layer2.LSB = original_LSB
            bracket_layer2.RSB = original_RSB
            
            # Step 3: Process Master 3
            layer3.clear()
            # Add processed paths with different strokes based on whether they're original or offset
            for path in processed_paths:
                new_path = path.copy()
                # Check if this is an original path or a centered path
                is_original = path in original_paths
                is_centered = path.attributes.get('strokePos', 0) == 0
                
                if is_original or (is_centered and path.attributes.get('offset_direction', 0) == 0):
                    # Original paths and first centered path get minimum width
                    set_stroke_attributes(new_path, self.min_stroke_width, self.min_stroke_width)
                else:
                    # Offset paths and second centered path get medium width
                    set_stroke_attributes(new_path, self.medium_stroke_width, self.medium_stroke_width)
                layer3.shapes.append(new_path)
            
            # Calculate new sidebearings to maintain original width
            paths_width = layer3.bounds.size.width
            total_sidebearings = original_width - paths_width
            layer3.LSB = total_sidebearings * lsb_proportion
            layer3.RSB = total_sidebearings * (1 - lsb_proportion)
            
            # Update bracket layer 3 sidebearings to match original master
            bracket_layer3.LSB = original_LSB
            bracket_layer3.RSB = original_RSB
            
            # Step 4: Process Master 4
            layer4.clear()
            # Add processed paths with medium stroke for both original and offset paths
            for path in processed_paths:
                new_path = path.copy()
                set_stroke_attributes(new_path, self.medium_stroke_width, self.medium_stroke_width)
                layer4.shapes.append(new_path)
            
            # Calculate new sidebearings to maintain original width
            paths_width = layer4.bounds.size.width
            total_sidebearings = original_width - paths_width
            layer4.LSB = total_sidebearings * lsb_proportion
            layer4.RSB = total_sidebearings * (1 - lsb_proportion)
            
            # Update bracket layer 4 sidebearings to match original master
            bracket_layer4.LSB = original_LSB
            bracket_layer4.RSB = original_RSB
            
            # Step 5: Process Master 5
            layer5.clear()
            # Add processed paths with specified stroke
            for path in processed_paths:
                new_path = path.copy()
                set_stroke_attributes(new_path, self.max_stroke_width, self.max_stroke_width)
                layer5.shapes.append(new_path)
            
            # Calculate new sidebearings to maintain original width
            paths_width = layer5.bounds.size.width
            total_sidebearings = original_width - paths_width
            layer5.LSB = total_sidebearings * lsb_proportion
            layer5.RSB = total_sidebearings * (1 - lsb_proportion)
            
            # Update bracket layer 5 sidebearings to match original master
            bracket_layer5.LSB = original_LSB
            bracket_layer5.RSB = original_RSB
            
            # Sync all layers to match the width of the first master
            # Store original spacing and calculate proportions
            original_LSB = layer1.LSB
            original_RSB = layer1.RSB
            original_total_sidebearings = original_LSB + original_RSB
            lsb_proportion = original_LSB / original_total_sidebearings if original_total_sidebearings > 0 else 0.5
            
            # Get original glyph width (this will be maintained across masters)
            original_width = layer1.width
            
            # Process all layers
            for current_layer in glyph.layers:
                # Skip if it's the first master (reference)
                if current_layer == layer1:
                    continue
                
                # Calculate new sidebearings to maintain original width
                paths_width = current_layer.bounds.size.width
                total_sidebearings = original_width - paths_width
                
                # Apply new sidebearings while maintaining proportions
                current_layer.LSB = total_sidebearings * lsb_proportion
                current_layer.RSB = total_sidebearings * (1 - lsb_proportion)
                
                # Update the layer
                current_layer.updateMetrics()

# Run the UI
MultiLineVariableUI()
