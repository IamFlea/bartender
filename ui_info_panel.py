from collections import OrderedDict

from ui_widget import QOverlayWidget
from ui_info_panel_label import PanelLabel

from config import * 


class InfoPanel(QOverlayWidget):
    """docstring for InfoPanel"""
    
    HEIGHT = 20

    def __init__(self, parent):
        super(InfoPanel, self).__init__(parent, resizable=False)
        self.panel_info_f = lambda : []
        self.list = OrderedDict()
        self.list_size_prev = 0
        self.set_geometry()
    

    def set_geometry(self):
        width_prefix_sum = 0
        for key in self.list:
            obj = self.list[key]
            obj.redraw()
            obj.set_position(width_prefix_sum)
            width_prefix_sum += obj.width() + 1
        if width_prefix_sum == 0:
            width_prefix_sum = InfoPanel.HEIGHT + 1
        self.setGeometry(self.x(), self.y(), width_prefix_sum - 1, InfoPanel.HEIGHT)

        
    def update(self):
        labels = self.panel_info_f()

        self.update_labels(labels)
        
        for obj, f in labels:
            if f is None:
                f = lambda : ""
            self.list[obj].text = f()
            self.list[obj].redraw()

    def update_labels(self, labels):
        # Set all icons to be removed from the bar
        for key in self.list:
            self.list[key].delete_me = True
        # Iterate through the list of objects
        for obj, f in labels:
            if obj not in self.list: # Check if the object is new -> create it
                self.list[obj] = PanelLabel(self, obj)
                self.set_geometry()
            # Object is used -> do not delete it
            self.list[obj].delete_me = False
        # Iterate through the objects which do have `delete_me == True`.
        for key in list(filter(lambda x, d=self.list: d[x].delete_me, self.list)):
            self.list[key].deleteLater()
            del self.list[key]
            self.set_geometry()
            
   


        


if __name__ == '__main__':
    import bartender
        
