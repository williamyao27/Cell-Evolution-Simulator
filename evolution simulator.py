# Import modules
import pygame
import random
import math



# Initialize game elements
pygame.init()
screen = pygame.display.set_mode((1200, 675))
pygame.display.set_caption("Evolution Simulator")
done = False
clock = pygame.time.Clock()



# Define color codes and other visuals
backgroundColor = (250, 250, 250)
red = (255, 0, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

font = pygame.font.SysFont('Arial', 14)
smallFont = pygame.font.SysFont('Arial', 12)
titleFont = pygame.font.SysFont('Arial', 18)



# Define variables
displayedCell = "none"
numberReproduced = 0
timeElapsed = 0



# -------Food Class-------
class Food:
    def __init__(self, foodX, foodY):
        self.x = foodX
        self.y = foodY

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 2)

foodList = []
foodRemove = [] # Define food removal list
newFood = 0 # The temporary variable used for storing information on newly spawned food



# -------Cell Class-------
class Cell:
    def __init__(self, cellGeneration, cellAge, cellX, cellY, cellVelocityX, cellVelocityY, cellMaturity, cellMaturityRate, cellHighlighted, # Basic properties
                 cellRadius, cellRadiusMax, cellR, cellG, cellB, # Visual properties
                 cellAcceleration, cellMoveCooldown, cellMoveCooldownMax, cellMoveEnergyLoss, # Movement properties
                 cellVisionRadius, cellDistractedness, cellAltruism, cellStressTolerance, cellTargetPosition, # AI properties
                 cellEnergy, cellEnergyMax, cellPassiveEnergyLoss, cellDigestion, cellFoodEaten, # Food properties
                 cellReproducing, cellReproductiveTimer, cellReproductiveCooldown, cellReproductiveCooldownMax, cellReproductiveEnergyLoss, cellChildren, cellEggsPerCycle, cellGeneticVariability): # Reproductive properties
        self.generation = cellGeneration
        self.age = cellAge
        self.x = cellX
        self.y = cellY
        self.velocityX = cellVelocityX
        self.velocityY = cellVelocityY
        self.maturity = cellMaturity
        self.maturityRate = cellMaturityRate
        self.highlighted = cellHighlighted
        self.radius = cellRadius
        self.radiusMax = cellRadiusMax
        self.r = cellR
        self.g = cellG
        self.b = cellB
        self.acceleration = cellAcceleration
        self.moveCooldown = cellMoveCooldown
        self.moveCooldownMax = cellMoveCooldownMax
        self.moveEnergyLoss = cellMoveEnergyLoss
        self.visionRadius = cellVisionRadius
        self.distractedness = cellDistractedness
        self.altruism = cellAltruism
        self.stressTolerance = cellStressTolerance
        self.targetPosition = cellTargetPosition
        self.energy = cellEnergy
        self.energyMax = cellEnergyMax
        self.passiveEnergyLoss = cellPassiveEnergyLoss
        self.digestion = cellDigestion
        self.foodEaten = cellFoodEaten
        self.reproducing = cellReproducing
        self.reproductiveTimer = cellReproductiveTimer
        self.reproductiveCooldown = cellReproductiveCooldown
        self.reproductiveCooldownMax = cellReproductiveCooldownMax
        self.reproductiveEnergyLoss = cellReproductiveEnergyLoss
        self.children = cellChildren
        self.eggsPerCycle = cellEggsPerCycle
        self.geneticVariability = cellGeneticVariability

    def draw(self):
        if self.age >= 0: # Draw cells only if they are meant to appear on screen
            if self.maturity >= 0: # Cells that have already hatched
                if self.highlighted == True:
                    pygame.draw.circle(screen, yellow, (int(self.x), int(self.y)), int(self.radius+5)) # Draw highlight
                pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x), int(self.y)), int(self.radius)) # Draw circular sprite
                pygame.draw.rect(screen, black, (int(self.x-self.radius*0.5), int(self.y+self.radius+0.2*self.radius), int(self.radius), int(0.2*self.radius))) # Draw energy bar max (black)
                pygame.draw.rect(screen, red, (int(self.x-self.radius*0.5), int(self.y+self.radius+0.2*self.radius), int(self.radius*self.energy/self.energyMax), int(0.2*self.radius))) # Draw energy bar max (red)
                if self.reproducing == True and self.reproductiveTimer == 0:
                    pygame.draw.circle(screen, backgroundColor, (int(self.x), int(self.y)), int(self.radius*0.5)) # Draw inner halo if willing to reproduce, half of the total radius
                if self.reproducing == True and self.reproductiveTimer > 0:
                    pygame.draw.circle(screen, backgroundColor, (int(self.x), int(self.y)), int(self.radius*0.5*self.reproductiveTimer/300)) # Inner halo shrinks
            if self.maturity < 0: # Cells in eggs
                pygame.draw.rect(screen, (self.r, self.g, self.b), (int(self.x-self.radiusMax*0.1-4), int(self.y-self.radiusMax*0.1-4), int(self.radiusMax*0.1*2+4), int(self.radiusMax*0.1*2+4))) # Draw square egg

    def move(self):
        # Calculate distance to target in two planes using trigonometry
        targetDistanceX = self.targetPosition[0] - self.x
        targetDistanceY = self.targetPosition[1] - self.y

        # Change velocity vectors based on this distance; restrict to targetDistance != 0 so that no divide-by-zero errors occur
        if targetDistanceX < 0 and targetDistanceX != 0:
            self.velocityX = self.acceleration * -1 * abs(math.cos(math.atan(targetDistanceY / targetDistanceX)))
        if targetDistanceX > 0 and targetDistanceX != 0:
            self.velocityX = self.acceleration * abs(math.cos(math.atan(targetDistanceY / targetDistanceX)))            
        if targetDistanceY < 0 and targetDistanceX != 0:
            self.velocityY = self.acceleration * -1 * abs(math.sin(math.atan(targetDistanceY / targetDistanceX)))
        if targetDistanceY > 0 and targetDistanceX != 0:
            self.velocityY = self.acceleration * abs(math.sin(math.atan(targetDistanceY / targetDistanceX)))
        self.moveCooldown = self.moveCooldownMax # Reset the movement cooldown
        
        # Based on the cell's distractedness, possibly force it to select a new target (helps prevent cells from getting stuck moving around one place); distractedness goes up if the cell is stressed ("frantic")
        if len(cellList)/(len(foodList)+1) > self.stressTolerance:
            if currentCell.distractedness*(1 + (len(cellList)/(len(foodList)+1)-self.stressTolerance)) >= random.randint(0,100):
                currentCell.targetPosition = ("none","none")
        else:
            if currentCell.distractedness >= random.randint(0,100):
                currentCell.targetPosition = ("none","none")

        # Consume energy; energy consumed increases with cell radius
        self.energy -= self.moveEnergyLoss*(1+(self.radius**1.75)/400)

    def searchMate(self, ignoreSelf):
        self.reproducing = True # Flag self as willing to reproduce
        for c in range(len(cellList)): # Go through food list to find closest piece of food
            currentCell = cellList[c]
            closestMatePosition = (10000,10000) # Initially set the closest mate position to a very high, temporary number
            if currentCell.reproducing == True and currentCell.reproductiveTimer == 0 and c != ignoreSelf: # Checks only for cells willing to reproduce but not already reproducing, and ignores self based on list index
                if ((currentCell.x-self.x)**2 + (currentCell.y-self.y)**2)**0.5 < ((closestMatePosition[0]-self.x)**2 + (closestMatePosition[1]-self.y)**2)**0.5: # Check if the current mate being checked is closer than the previously found closest mate
                    closestMatePosition = currentCell.x,currentCell.y # Declare the current mate to be the closest mate
        # Set target destination closest mate position
        if ((closestMatePosition[0]-self.x)**2 + (closestMatePosition[1]-self.y)**2)**0.5 <= self.radius+self.visionRadius:
            self.targetPosition = closestMatePosition[0],closestMatePosition[1]
        else:
            self.targetPosition = ("none","none") # Reset targeting if none found

    def reproduce(self, mate):
        global numberReproduced # Global value
        
        # Set reproductive timer
        self.reproductiveTimer = 300
        cellList[mate].reproductiveTimer = 300
        
        # -------Create Offspring--------
        youngestParent = self.generation # Set youngest parent generation to self as a placeholder
        if cellList[mate].generation > youngestParent: # Change generation if necessary
            youngestParent = cellList[mate].generation
        # Determine minimum and maximum ends of genetic variability for the child; variability increases with age as the genetic information deteriorates
        varMin = 100 - int((self.geneticVariability*1.002**(self.age/60)+cellList[mate].geneticVariability*1.002**(cellList[mate].age/60))/2)
        varMax = 100 + int((self.geneticVariability*1.002**(self.age/60)+cellList[mate].geneticVariability*1.002**(cellList[mate].age/60))/2)
        # Neither ends can exceed 75%
        if varMin < 25:
            varMin = 25
        if varMax > 175:
            varMax = 175
        for i in range(random.randint(1,int((self.eggsPerCycle+cellList[mate].eggsPerCycle)/2)+1)): # Number of eggs laid is dependent on the parents' eggs per cycle values
            newCell = Cell(youngestParent+1, -300, self.x+random.randint(-10,10), self.y+random.randint(-10,10), 0, 0, -100, ((self.maturityRate+cellList[mate].maturityRate)/2)*(random.randint(varMin,varMax)/100), False, # New cells are laid with -300 age so that they only appear at the end of the reproduction animation, as well as -100 maturity
                           1, ((self.radiusMax+cellList[mate].radiusMax)/2)*(random.randint(varMin,varMax)/100), ((self.r+cellList[mate].r)/2)*(random.randint(varMin,varMax)/100), ((self.g+cellList[mate].g)/2)*(random.randint(varMin,varMax)/100), ((self.b+cellList[mate].b)/2)*(random.randint(varMin,varMax)/100),
                           ((self.acceleration+cellList[mate].acceleration)/2)*(random.randint(varMin,varMax)/100), 0, ((self.moveCooldownMax+cellList[mate].moveCooldownMax)/2)*(random.randint(varMin,varMax)/100), ((self.moveEnergyLoss+cellList[mate].moveEnergyLoss)/2)*(random.randint(varMin,varMax)/100),
                           ((self.visionRadius+cellList[mate].visionRadius)/2)*(random.randint(varMin,varMax)/100), ((self.distractedness+cellList[mate].distractedness)/2)*(random.randint(varMin,varMax)/100), ((self.altruism+cellList[mate].altruism)/2)*(random.randint(varMin,varMax)/100), ((self.stressTolerance+cellList[mate].stressTolerance)/2)*(random.randint(varMin,varMax)/100), ("none","none"),
                           100, ((self.energyMax+cellList[mate].energyMax)/2)*(random.randint(varMin,varMax)/100), ((self.passiveEnergyLoss+cellList[mate].passiveEnergyLoss)/2)*(random.randint(varMin,varMax)/100), ((self.digestion+cellList[mate].digestion)/2)*(random.randint(varMin,varMax)/100), 0,
                           False, 0, 0, ((self.reproductiveCooldownMax+cellList[mate].reproductiveCooldownMax)/2)*(random.randint(varMin,varMax)/100), ((self.reproductiveEnergyLoss+cellList[mate].reproductiveEnergyLoss)/2)*(random.randint(varMin,varMax)/100), 0, ((self.eggsPerCycle+cellList[mate].eggsPerCycle)/2)*(random.randint(varMin,varMax)/100), ((self.geneticVariability+cellList[mate].geneticVariability)/2)*(random.randint(varMin,varMax)/100))
            # Enforce color code maximums
            if newCell.r > 245:
                newCell.r = 245
            if newCell.g > 245:
                newCell.g = 245
            if newCell.b > 245:
                newCell.b = 245
            # Enforce color code minimums
            if newCell.r < 10:
                newCell.r = 10
            if newCell.g < 10:
                newCell.g = 10
            if newCell.b < 10:
                newCell.b = 10
            # Set energy based on max energy, but only half as it is a newborn
            newCell.energy = newCell.energyMax*0.5
            cellList.append(newCell) # Append
            numberReproduced += 1 # Increment reproduction counter
            # Increment parents' children counter
            self.children += 1
            cellList[mate].children += 1

        # Reset the target position
        self.trackingPosition = ("none","none")
        cellList[mate].trackingPosition = ("none","none")

    def searchFood(self):
        if len(foodList) > 0: # Only search for food if there is food, to ignore index errors
            for f in range(len(foodList)): # Go through food list to find closest piece of food
                currentFood = foodList[f]
                closestFoodPosition = (10000,10000) # Initially set the closest food position to a very high, temporary number
                if ((currentFood.x-self.x)**2 + (currentFood.y-self.y)**2) < ((closestFoodPosition[0]-self.x)**2 + (closestFoodPosition[1]-self.y)**2): # Check if the current food being checked is closer than the previously found closest food
                    closestFoodPosition = currentFood.x,currentFood.y # Declare the current food to be the closest food
            # Set target destination closest food position
            if ((closestFoodPosition[0]-self.x)**2 + (closestFoodPosition[1]-self.y)**2)**0.5 <= self.radius+self.visionRadius:
                self.targetPosition = closestFoodPosition[0],closestFoodPosition[1]
            else:
                self.targetPosition = ("none","none") # Reset targeting if none found

    def eat(self, eatenFood):
        self.energy += self.digestion # Restore energy based on digestion value
        self.foodEaten += 1 # Increment food counter
        if self.energy > self.energyMax:
            self.energy = self.energyMax
        foodRemove.append(foodList[eatenFood]) # Remove the food item
        # Reset the target position for all cells who were chasing that food item, including self
        for c in range(0,len(cellList)):
            currentCell = cellList[c]
            if currentCell.targetPosition[0] == foodList[eatenFood].x and currentCell.targetPosition[1] == foodList[eatenFood].y:
                currentCell.targetPosition = ("none","none")

cellList = []
cellsRemove = [] # Define cell removal list
newCell = 0 # The temporary variable used for storing information on newly spawned cells



# -------Functions-------
def spawnNewWorld(cellCount, foodCount): # Spawn random cells at the beginning of the simulation

    # Draw cell
    for i in range(0,cellCount):
        newCell = Cell(0, 0, random.randint(0,1000), random.randint(0,675), 0, 0, 0, random.randint(1,100)/1000, False,
                       1, random.randint(10,450)/10, random.randint(10,245), random.randint(10,245), random.randint(10,245),
                       random.randint(1,100)/10, 0, random.randint(10,400), random.randint(1,500)/100,
                       random.randint(1,1000), random.randint(1,75), random.randint(10,50), random.randint(1,600)/100, ("none","none"),
                       100, random.randint(80,120), random.randint(1,1000)/10000, random.randint(50,250)/10, 0,
                       False, 0, 0, random.randint(120,3600), random.randint(1,49), 0, random.randint(100,300)/100, random.randint(50,250)/10)
        newCell.energy = newCell.energyMax # Set energy based on max energy
        cellList.append(newCell)

    # Draw food
    for i in range(0,foodCount):
        newFood = Food(random.randint(0,1000), random.randint(0,675))
        foodList.append(newFood)



# -------Main Program-------
spawnNewWorld(500, 250) # Spawn newly randomized population

while not done:
    
    # -------Controls-------
    mouseX,mouseY = pygame.mouse.get_pos() # Constantly retrieve mouse position
    
    for event in pygame.event.get(): # Quit game when window closed
        # Clicking
        if event.type == pygame.MOUSEBUTTONDOWN:
            for c in range(len(cellList)): # Detect cell click to set the sidebar to display info for that cell
                currentCell = cellList[c]
                if mouseX in range(int(currentCell.x-currentCell.radius-3), int(currentCell.x+currentCell.radius+3)) and mouseY in range(int(currentCell.y-currentCell.radius-3), int(currentCell.y+currentCell.radius+3)):
                    displayedCell = c
                    for h in range(len(cellList)): # Clear highlight from all cells
                        secondCurrentCell = cellList[h]
                        secondCurrentCell.highlighted = False
                    currentCell.highlighted = True # Apply highlight
        # Quitting 
        if event.type == pygame.QUIT:
            done = True

    # -------AI-------
    for c in range(len(cellList)):
        currentCell = cellList[c]

        # -------Physics-------
        # Movement
        currentCell.x += currentCell.velocityX
        currentCell.y += currentCell.velocityY
        
        # Drag
        currentCell.velocityX *= 0.9
        currentCell.velocityY *= 0.9

        # -------Age & Maturity-------
        if (currentCell.age < 0) or (currentCell.maturity >= 0 and currentCell.age >= 0): # Increase age if it's negative (parents are still reproducing) or if it has hatched
            currentCell.age += 1
        currentCell.maturity += currentCell.maturityRate * currentCell.energy/100 # Cells that have eaten more food mature faster
        if currentCell.maturity <= 100 and currentCell.maturity > 0: # Set radius as a proportion of maximum radius based on maturity, but only while still growing
            currentCell.radius = abs(currentCell.radiusMax * currentCell.maturity/100)
        
        # -------Reproduction-------
        if currentCell.reproducing == True:
            
            if currentCell.reproductiveTimer == 0: # Wants to reproduce
                # Exit reproductive stage if energy dips too low
                if currentCell.energy < (50 + (currentCell.energyMax-100)*0.5):
                    currentCell.reproducing = False
                    currentCell.targetPosition = ("none","none")
                # Entering reproduction
                for r in range(len(cellList)):
                    if cellList[r].reproducing == True and cellList[r].reproductiveTimer == 0 and r != c: # Ensure that the cell is reproducing with another cell, not itself
                        if ((cellList[r].x-currentCell.x)**2 + (cellList[r].y-currentCell.y)**2)**0.5 <= currentCell.radius:
                            currentCell.reproduce(r) # Trigger reproduction
                            break

            if currentCell.reproductiveTimer > 0: # Has already reproduced
                currentCell.reproductiveTimer -= 1 # Decrease reproduction timer passively
                currentCell.x += random.randint(-1,1)/2 # Shake during reproduction
                currentCell.y += random.randint(-1,1)/2 # Shake during reproduction
                currentCell.energy -= currentCell.reproductiveEnergyLoss/300 # Remove energy during reproduction
                if currentCell.reproductiveTimer == 0: # Reset reproductive cycle once the reproductive timer hits 0
                    currentCell.reproducing = False
                    currentCell.reproductiveCooldown = currentCell.reproductiveCooldownMax

        # -------Target Destination Selection-------
        # 1st priority: Reproduction; may interrupt food search
        if currentCell.reproductiveCooldown > 0: # Decrease reproductive cooldown passively
            currentCell.reproductiveCooldown -= 1
        if currentCell.maturity >= 100 and currentCell.energy >= (75 + (currentCell.energyMax-100)*0.5) and currentCell.reproductiveCooldown <= 0 and len(cellList)/(len(foodList)+1) <= currentCell.stressTolerance: # Become willing to reproduce only when able, high-energy, and non-stressed
            currentCell.searchMate(c) # Input of c, which indicates to the function the cell's own list index
        # 2nd priority: Food; may not interrupt anything; may not search for food if energy is above 90% and altruism is too high
        if currentCell.targetPosition == ("none","none") and currentCell.reproducing == False and ((currentCell.energy < currentCell.energyMax*0.9) or (currentCell.energy >= currentCell.energyMax*0.9 and random.randint(0,1000) > (currentCell.altruism+960))):
            currentCell.searchFood()
        # If nothing else: Random; may not interrupt anything
        if currentCell.targetPosition == ("none","none"):
            currentCell.targetPosition = random.randint(0,1000),random.randint(0,675)

        # -------Propel-------
        if currentCell.moveCooldown > 0: # Decrease move cooldown passively
            currentCell.moveCooldown -= 1
        if currentCell.moveCooldown <= 0 and currentCell.reproductiveTimer == 0 and currentCell.maturity >= 0: # Always move if possible, except during reproduction or while still in the egg
            currentCell.move()

        # -------Energy & Energy Consumption-------
        # Eating
        if len(foodList) > 0:
            for f in range(len(foodList)):
                if ((foodList[f].x-currentCell.x)**2 + (foodList[f].y-currentCell.y)**2)**0.5 <= currentCell.radius:
                    currentCell.eat(f) # Trigger eat function, specifying which food item is being eaten
        for f in foodRemove: # Remove food from class list if it has been eaten
            if f in foodList:
                foodList.remove(f)

        # Energy loss
        if currentCell.maturity >= 0: # Cells in eggs do not lose energy
            currentCell.energy -= currentCell.passiveEnergyLoss*(1.0025**(currentCell.age/60)) # Reduce energy level passively; increases over time with age
        # Death if energy reaches 0
        if currentCell.energy <= 0:
            cellsRemove.append(currentCell)
            # Remove display info if the cell was selected
            if c == displayedCell:
                displayedCell = "none"
            # Shift list index of displayed cell over if the dying cell, about to be removed from the list, will affect the displayed cell
            if displayedCell != "none" and c < displayedCell:
                displayedCell -= 1

    # Remove dead cells
    for c in cellsRemove:
        if c in cellList:
            cellList.remove(c)

    # Clear remove lists
    cellsRemove = []
    foodRemove = []

    # -------Food Spawning-------
    if random.randint(0,1000) > (979 - len(cellList)*0.99925**(timeElapsed/60)): # Chance to spawn new food each frame, determined by the number of cells, base chance of 2.0% per frame
        newFood = Food(random.randint(0+50,1000-50), random.randint(0+50,675-50)) # Doesn't spawn food too close to the edges
        foodList.append(newFood)

    # Increment timer
    timeElapsed += 1
            
    # -------Drawing-------
    screen.fill(backgroundColor) # Background
    pygame.draw.rect(screen, white, (1000, 0, 300, 675)) # Draw sidebar

    # Display info - general
    screen.blit(smallFont.render("Cells: "+str(len(cellList))+" ("+str(numberReproduced)+"R)", 0, black), (1010, 650))
    screen.blit(smallFont.render("Food: "+str(len(foodList)), 0, black), (1120, 650))
    screen.blit(smallFont.render("Time: "+str(int(timeElapsed/60))+"s", 0, black), (920, 650))

    # Display info - cell specific
    if displayedCell == "none": # Display nothing if no cell is selected
        screen.blit(titleFont.render("No cell selected", 0, black), (1025, 25))
    if displayedCell != "none": # Display stats
        screen.blit(titleFont.render("Cell #"+str(displayedCell)+"     G"+str(cellList[displayedCell].generation)+", "+str(int(cellList[displayedCell].age/60))+"s", 0, black), (1025, 25))

        screen.blit(font.render("Energy:  "+str(int(cellList[displayedCell].energy))+"/"+str(int(cellList[displayedCell].energyMax)), 0, black), (1025, 60))
        pygame.draw.rect(screen, black, (int(1140), int(65), int(40), int(5)))
        pygame.draw.rect(screen, red, (int(1140), int(65), int(40*cellList[displayedCell].energy/cellList[displayedCell].energyMax), int(5)))
        screen.blit(font.render("Gen. Loss/sec:  "+str(round((60/cellList[displayedCell].moveCooldownMax)*cellList[displayedCell].moveEnergyLoss*(1+(cellList[displayedCell].radius**1.75)/400)+cellList[displayedCell].passiveEnergyLoss*60*(1.0025)**(cellList[displayedCell].age/60),2)), 0, black), (1025, 75))
        screen.blit(font.render("Base Psv. Loss/sec:  "+str(round(cellList[displayedCell].passiveEnergyLoss*60,2)), 0, black), (1025, 90))
        screen.blit(font.render("Digestion:  "+str(round(cellList[displayedCell].digestion,1)), 0, black), (1025, 105))
        screen.blit(font.render("Food Eaten:  "+str(round(cellList[displayedCell].foodEaten,1)), 0, black), (1025, 120))
        
        screen.blit(font.render("Position:  ("+str(int(cellList[displayedCell].x))+","+str(int(cellList[displayedCell].y))+")", 0, black), (1025, 150))
        screen.blit(font.render("Color:  ", 0, black), (1025, 165))
        pygame.draw.rect(screen, (cellList[displayedCell].r, cellList[displayedCell].g, cellList[displayedCell].b), (1072, 168, 11, 11))
        screen.blit(font.render("Maturity:  "+str(int(cellList[displayedCell].maturity)), 0, black), (1025, 180))
        screen.blit(font.render("Radius:  "+str(int(cellList[displayedCell].radiusMax)), 0, black), (1025, 195))
        screen.blit(font.render("Breeding?  "+str(cellList[displayedCell].reproducing), 0, black), (1025, 210))
        
        screen.blit(font.render("Maturity Rate:  "+str(round(cellList[displayedCell].maturityRate,3)), 0, black), (1025, 240))
        screen.blit(font.render("Maturity/sec:  "+str(round(cellList[displayedCell].maturityRate*60*cellList[displayedCell].energy/100,1)), 0, black), (1025, 255))
        screen.blit(font.render("Current Radius:  "+str(round(cellList[displayedCell].radius,1)), 0, black), (1025, 270))
        
        screen.blit(font.render("Acceleration:  "+str(round(cellList[displayedCell].acceleration,1)), 0, black), (1025, 300))
        screen.blit(font.render("Move Rate:  "+str(round(cellList[displayedCell].moveCooldownMax/60,1))+"s", 0, black), (1025, 315))
        screen.blit(font.render("Move Energy:  "+str(round(cellList[displayedCell].moveEnergyLoss*(1+(cellList[displayedCell].radius**1.75)/400),1)), 0, black), (1025, 330))
        screen.blit(font.render("Inc. due to Radius:  "+str(round(1+(cellList[displayedCell].radius**1.75)/400,2)), 0, black), (1025, 345))
        
        screen.blit(font.render("Vision Radius:  "+str(int(cellList[displayedCell].visionRadius)), 0, black), (1025, 375))
        screen.blit(font.render("Distractibility:  "+str(int(cellList[displayedCell].distractedness))+"%", 0, black), (1025, 390))
        screen.blit(font.render("Altruism%/sec:  "+str(int(((cellList[displayedCell].altruism/1000+0.95)**60)*100))+"%", 0, black), (1025, 405))
        screen.blit(font.render("Stress:  "+str(round(len(cellList)/(len(foodList)+1),1))+" / "+str(round(cellList[displayedCell].stressTolerance,1)), 0, black), (1025, 420))

        screen.blit(font.render("Breed Rate:  "+str(round(cellList[displayedCell].reproductiveCooldownMax/60,1))+"s", 0, black), (1025, 450))
        screen.blit(font.render("Breed Energy:  "+str(round(cellList[displayedCell].reproductiveEnergyLoss,1)), 0, black), (1025, 465))
        screen.blit(font.render("Current Cooldown:  "+str(abs(round(cellList[displayedCell].reproductiveCooldown/60,1)))+"s", 0, black), (1025, 480))

        screen.blit(font.render("Max Eggs/cycle:  "+str(round(cellList[displayedCell].eggsPerCycle,1)), 0, black), (1025, 510))
        screen.blit(font.render("Genetic Variability:  "+str(round(cellList[displayedCell].geneticVariability,1))+"%", 0, black), (1025, 525))
        screen.blit(font.render("Current Gen. Var.:  "+str(round(cellList[displayedCell].geneticVariability*1.002**(cellList[displayedCell].age/60),1))+"%", 0, black), (1025, 540))
        screen.blit(font.render("Children:  "+str(round(cellList[displayedCell].children,1)), 0, black), (1025, 555))

    # Draw cells
    for c in range(len(cellList)):
        currentCell = cellList[c]
        currentCell.draw()

    # Draw food
    if len(foodList) > 0:
        for f in range(len(foodList)):
            currentFood = foodList[f]
            currentFood.draw()
    
    # Updates screen
    pygame.display.flip()

    # 60 fps default
    clock.tick(60)



# Quit
pygame.quit()
