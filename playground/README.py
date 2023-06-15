from evomark import ask, answer, show, evolve, topic, set_out_path, out

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

a = answer(em)
show(a)
"""""show
Introducing Evomark - the ultimate framework for working with AIGC models in python. With Evomark, you can control your AIGC workflow by writing python code that evolves through feedback from humans. This dynamic interaction between the model and human feedback allows for more accurate predictions and streamlined workflow. Evomark has several important considerations, including caching whenever possible to save the number of API calls, ensuring everything happens in one place to eliminate the need for copy and paste, and making it easy to provide human feedback. Evomark is the perfect tool for any data scientist looking to enhance their AIGC workflow and improve their results.
"""""

out("""
# Evomark

""")
out(a)

# By update(), the code can modify itself, that is, evolve!
evolve()