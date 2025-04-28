# MenuTitle: Delete Paths in Masters
# -*- coding: utf-8 -*-
__doc__="""
Deletes all paths from all masters of the currently selected glyph.
"""

def DeleteAllPaths(thisLayer):
	thisLayer.parent.beginUndo()
	
	for i in range(len(thisLayer.shapes)-1, -1, -1):
		path = thisLayer.shapes[i]
		if isinstance(path, GSPath):
			del thisLayer.shapes[i]

	thisLayer.parent.endUndo()

# Get the current font
font = Glyphs.font

# Check if a font is open and a glyph is selected
if font and font.selectedLayers:
	# Get the current glyph
	current_glyph = font.selectedLayers[0].parent
	
	if current_glyph:
		# Disable interface updates for better performance
		font.disableUpdateInterface()
		
		try:
			# Process all masters
			for master in font.masters:
				# Get the layer for this master
				layer = current_glyph.layers[master.id]
				DeleteAllPaths(layer)
				print(f"Cleared paths in master: {master.name}")
			
			print("Done!")
		except Exception as e:
			print(f"An error occurred: {str(e)}")
		finally:
			# Always re-enable interface updates
			font.enableUpdateInterface()
	else:
		print("Could not get current glyph")
else:
	print("No font open or no glyph selected")