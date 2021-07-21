class CoordConverter:
    def __init__(self, OG_res, DISPLAY_res):
        self.OG = OG_res
        self.DISPLAY = DISPLAY_res
        self.OG2DISPLAY_ratio = [float(self.DISPLAY[i])/self.OG[i] for i in range(2)]
        self.DISPLAY2OG_ratio = [float(self.OG[i])/self.DISPLAY[i] for i in range(2)]

    
    def Single_OG2Display(self, coords):
        x, y = coords[0], coords[1]
        adjusted_x = int(x * self.OG2DISPLAY_ratio[0])
        adjusted_y = int(y * self.OG2DISPLAY_ratio[1])
        return (adjusted_x, adjusted_y)


    def Single_Display2OG(self, coords):
        x, y = coords[0], coords[1]
        adjusted_x = int(x * self.DISPLAY2OG_ratio[0])
        adjusted_y = int(y * self.DISPLAY2OG_ratio[1])
        return (adjusted_x, adjusted_y)


    def getOG(self):
        return list(self.OG)

    
    def getDisplay(self):
        return list(self.DISPLAY)
