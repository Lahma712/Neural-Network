def Grid(hCellCount, Width, Height, draw, GridColor):
    def contin(a, b, c, ExcessPixels, CellWidth, Axis, CellCount, C, counter, intv): #fuction that continues the algorithm with parameters given from the init function
        C += CellWidth+a #second grid pixel after 0 is placed a little sooner
        Axis += [C]
        for _ in range(ExcessPixels-1): #loop that places pixels with adjusted distance due to excess pixels ('b' is +1 or +0 depending if number of Excesspixels is less/more than half number of cells)
            C += CellWidth+b
            Axis += [C]
            counter -= 1
            for _ in range(intv): #loop that places pixels with normal distance (without adjusted distance due to excesspixels)
                C += CellWidth+c
                Axis += [C]
                counter -= 1
        for _ in range(counter-1): #loop that places rest of grid pixels once there are no more excesspixels
            C += CellWidth+c
            Axis += [C]
        return


    def init(a, b, c , d, ExcessPixels, CellWidth, Axis, CellCount, C, counter):
        try:
            intv = abs((CellCount - ExcessPixels)//(ExcessPixels-1)) #interval, excesspixel comes every intv'th pixel
            if intv == CellCount: #if excessspixels = 0
                    contin(a, 99, c, ExcessPixels, CellWidth, Axis, CellCount, C, counter, intv) # second position '99' doesnt play any role here
                    return
        except: #if excesspixels = 1
            intv = abs((CellCount - 1))
            contin(b, 99, c, ExcessPixels, CellWidth, Axis, CellCount, C, counter, intv)
            return
        contin(b, d, c, ExcessPixels, CellWidth, Axis, CellCount, C, counter, intv) #if excesspixels not 0 and not 1
        return


    def grid(Axis, CellCount, CellWidth, ExcessPixels):
        C = 0  # counter for grid pixel position
        counter = CellCount
        if ExcessPixels > CellCount//2: #checks if excesspixels are more than half the number of cells
            ExcessPixels = CellCount - ExcessPixels
            init(-2, -1, 1, 0, ExcessPixels, CellWidth, Axis, CellCount, C, counter)
        else: # if excesspixels are less than half the number of cells
            init(-1, 0, 0, 1, ExcessPixels, CellWidth, Axis, CellCount, C, counter)

   
    def Draw(a, b, color): #draws pixels on image
        for y in b:
            for x in a:
                draw.point([x, y], color)

    hCellWidth = Width // hCellCount  # Pixel width per cell (horizontal pixels)
    hExcessPixels = Width % hCellCount #excess pixels if there is a rest
    vCellCount = Height // hCellWidth  # number of vertical cells
    vCellWidth = Height // vCellCount  # Pixel height per cell (vertical pixels)
    vExcessPixels = Height % vCellCount
    HGrid = [0]
    VGrid = [0]
    
    gcolor = GridColor
    grid(HGrid, vCellCount, vCellWidth, vExcessPixels)
    grid(VGrid, hCellCount, hCellWidth, hExcessPixels)
    
    Draw(range(Width), HGrid, gcolor)
    Draw(VGrid, range(Height), gcolor)
    return HGrid, VGrid, vCellCount


def Cells(HGrid, VGrid): #function that creates dataset of the XY coords of every cell
    def cells(grid, Cells):
        for x in range(len(grid)-1):
            cell = [y for y in range(grid[x]+1, grid[x+1])]
            Cells.append(cell)
    
    XCells = []
    YCells = []
    cells(HGrid, YCells)
    cells(VGrid, XCells)
    return XCells, YCells

def drawCell(X,Y, color, draw): #function that draws a single cell when you click on one
    for y in Y:
        for x in X:
            draw.point([x, y], color)

def drawFrame(draw, currentCells, cells, color): #function that draws the frames
    for cellIndex in currentCells:
        try:
            for y in cells[1][cellIndex[1]]:
                for x in cells[0][cellIndex[0]]:
                    draw.point([x, y], color)
        except:
            pass
    return