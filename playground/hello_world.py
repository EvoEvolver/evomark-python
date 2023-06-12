from evomark.E import show, update
from evomark.model.openai import cpl


a = cpl("Who discoverd America? Answer:")

show(a)


# By update(), the code can modify itself, that is, evolve!
update()