from evomark import ask, answer, show, update, topic, set_out_path, out

set_out_path("../README.md")

em = topic("Write a introduction for Evomark")

em.what_it_is = """
- A framework for working with AIGC models in python
"""

em.what_it_does = """
- Control AIGC workflow by writing python code
- The workflow and human give feedback to each other by modifying (evolving) the code
"""

em.important_consideration = """
- Cache whenever possible to save the number of API calls
- Everything happen in one place: no copy and paste
- Easy to give human feedback
"""

show(em)
"""""show
topic: Write a introduction for Evomark
what it is: 
- A framework for working with AIGC models in python

what it does: 
- Control AIGC workflow by writing python code
- The workflow and human give feedback to each other by modifying (evolving) the code

important consideration: 
- Cache whenever possible to save the number of API calls
- Everything happen in one place: no copy and paste
- Easy to give human feedback
"""""


a = ask(em)

show(a)
"""""show
user: topic: Write a introduction for Evomark
what it is: 
- A framework for working with AIGC models in python

what it does: 
- Control AIGC workflow by writing python code
- The workflow and human give feedback to each other by modifying (evolving) the code

important consideration: 
- Cache whenever possible to save the number of API calls
- Everything happen in one place: no copy and paste
- Easy to give human feedback
"""""

a = answer(a)
show(a)
"""""show
Introducing Evomark - a powerful framework designed to simplify working with AIGC models in Python. With Evomark, controlling the workflow of your AIGC models has never been easier. By writing Python code, you can effortlessly fine-tune your models and receive human feedback to help make them even better. Evomark's unique approach involves evolving the code based on feedback, resulting in a more accurate and efficient workflow. The framework also offers important considerations such as caching to save on API calls and ensuring everything happens in one place. Additionally, Evomark makes it easy for humans to give feedback. Say goodbye to copy and paste and hello to a revolutionary way to work with AIGC models - Evomark.
"""""

out("""
# Evomark

""")
out(a)

# By update(), the code can modify itself, that is, evolve!
update()