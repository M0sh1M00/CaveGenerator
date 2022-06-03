# CaveGenerator

EXPLANATION

Splits the board (200 by 200 tiles) into 16 different regions; 4 down 4 across

Each region has a 2/3 chance of having a large node.

After all Large nodes are populated they have a 100% chance of connecting to their closest neighbour and a 66% chance of connecting to their second closest neighbour.

Math is done to draw a 1 thick line to represent these connections.

Program then thickens the caves by iterating 3 times. Each iteration there is a 50% chance a block is added west of an already existing block, 50% chance for east and same chance for north and south.

Then do small nodes. Board is split into 64 regions with each region having a 50% chance for small node.

Small nodes have 100% chance of connecting to closest neighbour and 50% chance of connecting to second closest neighbour.

Then thicken by iterating 2 more times. This means large caves are 5 thick while small caves are 2 thick.

