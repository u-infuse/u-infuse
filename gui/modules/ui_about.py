"""
Author:  Chris Lawson
Contact: clawso21@une.edu.au
Source:  U-Infuse
Purpose: Functions for the About Dialogue.
"""

def WriteText(self):
    """
    Writes text to the about dialogue.
    """
    self.aboutDialogue.textBrowser.setOpenExternalLinks(True)
    self.aboutDialogue.textBrowser.clear()
    self.aboutDialogue.textBrowser.append("<CENTER><H1><IMG SRC='icon.png' WIDTH='50' HEIGHT='50'>U-Infuse</H1>")
    self.aboutDialogue.textBrowser.append("<H2>Version: 1.0</H2>")
    self.aboutDialogue.textBrowser.append("\n<H2>Licence: GPLv3</H2>")
    self.aboutDialogue.textBrowser.append("<H3>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</H3>")
    self.aboutDialogue.textBrowser.append("<H3>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</H3>")
    self.aboutDialogue.textBrowser.append("<H3>You should have received a copy of the GNU General Public License along with this program. If not, see <A HREF='https://www.gnu.org/licenses/'>https://www.gnu.org/licenses/</A>.</H3>")
    self.aboutDialogue.textBrowser.append("<H3>For further information, tutorials and to ask any questions, visit our Github repo: <A HREF='https://github.com/u-infuse'>https://github.com/u-infuse</A>.</H3>")

def AboutDialogue(self):
    """
    About dialogue for U-Infuse.
    """
    # Make cursor invisible
    self.aboutDialogue.textBrowser.setCursorWidth(0)

    # Write text
    WriteText(self)

    # Show dialogue
    self.aboutDialogue.show()

def CloseButton(self):
    """
    Closes the about dialogue.
    """
    self.aboutDialogue.reject()
