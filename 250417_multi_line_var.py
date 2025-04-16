# MenuTitle: Multi Line Variable 250417
# -*- coding: utf-8 -*-
__doc__="""
Creates multi-line variable font with specified offsets.
"""

from GlyphsApp import *
from GlyphsApp.plugins import *
from GlyphsApp.UI import *
from vanilla import *

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

class MultiLineVariableUI:
    def __init__(self):
        # Default values
        self.original_offset = -70
        
        # Master 2
        self.master2_offset_width = 40
        self.master2_offset_height = 40
        
        # Master 3
        self.master3_width = 40
        self.master3_height = 40
        self.master3_original_width = 40
        self.master3_original_height = 40
        
        # Master 4
        self.master4_width = 80
        self.master4_height = 80
        self.master4_original_width = 80
        self.master4_original_height = 80
        
        # Master 5
        self.master5_offset_width = 10
        self.master5_offset_height = 80
        self.master5_original_width = 80
        self.master5_original_height = 10
        
        # Create the window with a larger height
        self.w = FloatingWindow((400, 700), "Multi Line Variable Settings")
        
        # Create UI elements
        y = 10
        
        # Main offset
        self.w.offset_label = TextBox((10, y, 380, 22), "Main Offset (distance between lines):")
        y += 25
        self.w.original_offset = EditText((10, y, 380, 22), "", callback=self.saveSettings)
        y += 40
        
        # Master 2 settings
        self.w.master2_label = TextBox((10, y, 380, 22), "Master 2 - Medium Lines")
        y += 25
        self.w.master2_offset_label = TextBox((10, y, 380, 22), "Offset Path:")
        y += 25
        self.w.master2_offset_width = EditText((10, y, 180, 22), "Width:", callback=self.saveSettings)
        self.w.master2_offset_height = EditText((200, y, 180, 22), "Height:", callback=self.saveSettings)
        y += 40
        
        # Master 3 settings
        self.w.master3_label = TextBox((10, y, 380, 22), "Master 3 - Thick Lines")
        y += 25
        self.w.master3_original_label = TextBox((10, y, 380, 22), "Original Path:")
        y += 25
        self.w.master3_original_width = EditText((10, y, 180, 22), "Width:", callback=self.saveSettings)
        self.w.master3_original_height = EditText((200, y, 180, 22), "Height:", callback=self.saveSettings)
        y += 30
        self.w.master3_offset_label = TextBox((10, y, 380, 22), "Offset Path:")
        y += 25
        self.w.master3_width = EditText((10, y, 180, 22), "Width:", callback=self.saveSettings)
        self.w.master3_height = EditText((200, y, 180, 22), "Height:", callback=self.saveSettings)
        y += 40
        
        # Master 4 settings
        self.w.master4_label = TextBox((10, y, 380, 22), "Master 4 - Extra Thick Lines")
        y += 25
        self.w.master4_original_label = TextBox((10, y, 380, 22), "Original Path:")
        y += 25
        self.w.master4_original_width = EditText((10, y, 180, 22), "Width:", callback=self.saveSettings)
        self.w.master4_original_height = EditText((200, y, 180, 22), "Height:", callback=self.saveSettings)
        y += 30
        self.w.master4_offset_label = TextBox((10, y, 380, 22), "Offset Path:")
        y += 25
        self.w.master4_width = EditText((10, y, 180, 22), "Width:", callback=self.saveSettings)
        self.w.master4_height = EditText((200, y, 180, 22), "Height:", callback=self.saveSettings)
        y += 40
        
        # Master 5 settings
        self.w.master5_label = TextBox((10, y, 380, 22), "Master 5 - Mixed Thickness")
        y += 25
        self.w.master5_original_label = TextBox((10, y, 380, 22), "Original Path:")
        y += 25
        self.w.master5_original_width = EditText((10, y, 180, 22), "Width:", callback=self.saveSettings)
        self.w.master5_original_height = EditText((200, y, 180, 22), "Height:", callback=self.saveSettings)
        y += 30
        self.w.master5_offset_label = TextBox((10, y, 380, 22), "Offset Path:")
        y += 25
        self.w.master5_offset_width = EditText((10, y, 180, 22), "Width:", callback=self.saveSettings)
        self.w.master5_offset_height = EditText((200, y, 180, 22), "Height:", callback=self.saveSettings)
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
        
        # Master 2
        self.master2_offset_width = self.safe_float(self.w.master2_offset_width.get(), 40)
        self.master2_offset_height = self.safe_float(self.w.master2_offset_height.get(), 40)
        
        # Master 3
        self.master3_width = self.safe_float(self.w.master3_width.get(), 40)
        self.master3_height = self.safe_float(self.w.master3_height.get(), 40)
        self.master3_original_width = self.safe_float(self.w.master3_original_width.get(), 40)
        self.master3_original_height = self.safe_float(self.w.master3_original_height.get(), 40)
        
        # Master 4
        self.master4_width = self.safe_float(self.w.master4_width.get(), 80)
        self.master4_height = self.safe_float(self.w.master4_height.get(), 80)
        self.master4_original_width = self.safe_float(self.w.master4_original_width.get(), 80)
        self.master4_original_height = self.safe_float(self.w.master4_original_height.get(), 80)
        
        # Master 5
        self.master5_offset_width = self.safe_float(self.w.master5_offset_width.get(), 10)
        self.master5_offset_height = self.safe_float(self.w.master5_offset_height.get(), 80)
        self.master5_original_width = self.safe_float(self.w.master5_original_width.get(), 80)
        self.master5_original_height = self.safe_float(self.w.master5_original_height.get(), 10)
    
    def loadSettings(self):
        # Load all settings into UI
        self.w.original_offset.set(str(self.original_offset))
        
        # Master 2
        self.w.master2_offset_width.set(str(self.master2_offset_width))
        self.w.master2_offset_height.set(str(self.master2_offset_height))
        
        # Master 3
        self.w.master3_width.set(str(self.master3_width))
        self.w.master3_height.set(str(self.master3_height))
        self.w.master3_original_width.set(str(self.master3_original_width))
        self.w.master3_original_height.set(str(self.master3_original_height))
        
        # Master 4
        self.w.master4_width.set(str(self.master4_width))
        self.w.master4_height.set(str(self.master4_height))
        self.w.master4_original_width.set(str(self.master4_original_width))
        self.w.master4_original_height.set(str(self.master4_original_height))
        
        # Master 5
        self.w.master5_offset_width.set(str(self.master5_offset_width))
        self.w.master5_offset_height.set(str(self.master5_offset_height))
        self.w.master5_original_width.set(str(self.master5_original_width))
        self.w.master5_original_height.set(str(self.master5_original_height))
    
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
            
            # Create offset paths for all masters
            offset_paths = []
            for path in original_paths:
                # Create a copy of the path
                offset_path = path.copy()
                # Apply Offset Curve filter with exact parameters
                temp_layer = GSLayer()
                temp_layer.shapes.append(offset_path)
                offsetCurveFilter.processLayer_withArguments_(temp_layer, ['OffsetCurve', str(self.original_offset), str(self.original_offset), '0', '0.5'])
                if len(temp_layer.paths) > 0:
                    offset_path = temp_layer.paths[0]
                offset_paths.append(offset_path)
            
            # Create special layers for each master
            wg_layer1 = GSLayer()
            wg_layer1.name = "[]"  # Changed from "[wg<120]" to "[]"
            wg_layer1.associatedMasterId = master1.id
            wg_layer1.LSB = original_LSB
            wg_layer1.RSB = original_RSB
            
            wg_layer2 = GSLayer()
            wg_layer2.name = "[wg<120]"
            wg_layer2.associatedMasterId = master2.id
            wg_layer2.LSB = original_LSB
            wg_layer2.RSB = original_RSB
            
            wg_layer3 = GSLayer()
            wg_layer3.name = "[wg<120]"
            wg_layer3.associatedMasterId = master3.id
            wg_layer3.LSB = original_LSB
            wg_layer3.RSB = original_RSB
            
            wg_layer4 = GSLayer()
            wg_layer4.name = "[wg<120]"
            wg_layer4.associatedMasterId = master4.id
            wg_layer4.LSB = original_LSB
            wg_layer4.RSB = original_RSB
            
            wg_layer5 = GSLayer()
            wg_layer5.name = "[wg<120]"
            wg_layer5.associatedMasterId = master5.id
            wg_layer5.LSB = original_LSB
            wg_layer5.RSB = original_RSB
            
            # Add original path to special layers with 10-point stroke
            for path in original_paths:
                # Master 1 []
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = 10
                new_path.attributes['strokeHeight'] = 10
                wg_layer1.shapes.append(new_path)
                
                # Master 2 [wg<120]
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = 10
                new_path.attributes['strokeHeight'] = 10
                wg_layer2.shapes.append(new_path)
                
                # Master 3 [wg<120]
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = 10
                new_path.attributes['strokeHeight'] = 10
                wg_layer3.shapes.append(new_path)
                
                # Master 4 [wg<120]
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = 10
                new_path.attributes['strokeHeight'] = 10
                wg_layer4.shapes.append(new_path)
                
                # Master 5 [wg<120]
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = 10
                new_path.attributes['strokeHeight'] = 10
                wg_layer5.shapes.append(new_path)
            
            # Add offset path to the first master's [] layer
            for path in offset_paths:
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = 10
                new_path.attributes['strokeHeight'] = 10
                wg_layer1.shapes.append(new_path)
            
            # Add the special layers to the glyph
            glyph.layers.append(wg_layer1)
            glyph.layers.append(wg_layer2)
            glyph.layers.append(wg_layer3)
            glyph.layers.append(wg_layer4)
            glyph.layers.append(wg_layer5)
            
            # Step 1: Process Master 1
            # Clear and rebuild Master 1
            layer1.clear()
            layer1.name = "Single Thin [wg<120]"  # Changed to "Single Thin [wg<120]"
            # Add original paths with specified stroke
            for path in original_paths:
                path.attributes['strokeWidth'] = 10
                path.attributes['strokeHeight'] = 10
                layer1.shapes.append(path)
            # Add offset paths with 2-point stroke
            for path in offset_paths:
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = 2
                new_path.attributes['strokeHeight'] = 2
                layer1.shapes.append(new_path)
            # Restore original spacing
            layer1.LSB = original_LSB
            layer1.RSB = original_RSB
            
            # Step 2: Process Master 2
            layer2.clear()
            # Add original paths with specified stroke
            for path in original_paths:
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = 10
                new_path.attributes['strokeHeight'] = 10
                layer2.shapes.append(new_path)
            # Add offset paths with specified stroke
            for path in offset_paths:
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = self.master2_offset_width
                new_path.attributes['strokeHeight'] = self.master2_offset_height
                layer2.shapes.append(new_path)
            # Restore original spacing
            layer2.LSB = original_LSB
            layer2.RSB = original_RSB
            
            # Step 3: Process Master 3
            layer3.clear()
            # Add original paths with thicker stroke
            for path in original_paths:
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = self.master3_original_width
                new_path.attributes['strokeHeight'] = self.master3_original_height
                layer3.shapes.append(new_path)
            
            # Add offset paths with thicker stroke
            for path in offset_paths:
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = self.master3_width
                new_path.attributes['strokeHeight'] = self.master3_height
                layer3.shapes.append(new_path)
            
            # Restore original spacing
            layer3.LSB = original_LSB
            layer3.RSB = original_RSB
            
            # Step 4: Process Master 4
            layer4.clear()
            # Add original paths with thicker stroke
            for path in original_paths:
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = self.master4_original_width
                new_path.attributes['strokeHeight'] = self.master4_original_height
                layer4.shapes.append(new_path)
            
            # Add offset paths with thicker stroke
            for path in offset_paths:
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = self.master4_width
                new_path.attributes['strokeHeight'] = self.master4_height
                layer4.shapes.append(new_path)
            
            # Restore original spacing
            layer4.LSB = original_LSB
            layer4.RSB = original_RSB
            
            # Step 5: Process Master 5
            layer5.clear()
            # Add original paths with specified stroke
            for path in original_paths:
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = self.master5_original_width
                new_path.attributes['strokeHeight'] = self.master5_original_height
                layer5.shapes.append(new_path)
            # Add offset paths with specified stroke
            for path in offset_paths:
                new_path = path.copy()
                new_path.attributes['strokeWidth'] = self.master5_offset_width
                new_path.attributes['strokeHeight'] = self.master5_offset_height
                layer5.shapes.append(new_path)
            # Restore original spacing
            layer5.LSB = original_LSB
            layer5.RSB = original_RSB

# Run the UI
MultiLineVariableUI()
