from evomark import *

name = "M. Foucault"

set_out_path(name + ".md")

q = question("What is the important books written by " + name + "?")
#q.requirement = 'Answer in the format of ["book1", "book2"]'

show(q)
"""""show
question: What is the important books written by M. Foucault?
"""""

a = answer(q, system_message='Answer in the format of ["book1", "book2"]')
booklist = parse(a)
show(a)
"""""show
["Madness and Civilization", "The Birth of the Clinic"]
"""""


out_cl("Here are the books written by " + name + ":")

for book in booklist:
    t = topic(book)
    t.requirement = "Write a introduction of the book"
    a = answer(t)
    out_cl("# " + book)
    out_cl(a)

evolve()