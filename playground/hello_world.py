from evomark import show, update, ask, answer, out

a = ask("Who is M. Foucault?")

show(a)
"""""show
user: Who is M. Foucault?
"""""

a = answer(a)

show(a)
"""""show
M. Foucault refers to Michel Foucault, a French philosopher, social theorist, and historian who is known for his influential works on power, sexuality, and knowledge. He was born on October 15, 1926, in Poitiers, France, and died on June 25, 1984. His major works include Madness and Civilization, The Birth of the Clinic, Discipline and Punish, and The History of Sexuality. Foucault's ideas have had a significant impact on various disciplines, including philosophy, sociology, psychology, cultural studies, and political science.
"""""

out(a)

update()