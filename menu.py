import nuke
import sys

nuke.menu("Nodes").addMenu('RenameTool', icon='rename_icon.png')
nuke.menu("Nodes").addCommand('RenameTool/Rename Sequence', 'renameSequence()')
nuke.menu("Nodes").addCommand('RenameTool/Update', 'import rename_sequence\nreload(rename_sequence)')


def renameSequence():
	import rename_sequence
	# print window
	if len(nuke.selectedNodes()) != 1 or nuke.selectedNode().Class() != 'Read':
		nuke.message('Please select one Read node.')
		return
	window = rename_sequence.RenameSequenceUI()
	window.open()
