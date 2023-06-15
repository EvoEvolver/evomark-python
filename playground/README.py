from evomark import answer, show, evolve, topic, set_out_path, out

set_out_path("../README.md")

em = topic("Write a introduction for Evomark")

em.what_it_is = """
- A framework for working with AIGC (AI generated content) models in python
"""

em.what_it_does = """
- Control AIGC workflow by writing python code
- The workflow and human give feedback to each other by modifying (evolving) the code
"""

em.its_important_consideration = """
- Cache whenever possible to save the number of API calls
- Everything happen in one place: no copy and paste
- Easy to give human feedback
"""

em.writing_requirement = "Use simple language and short sentences. Use bullet points in the Markdown format if possible."

show(em)
"""""show
topic: Write a introduction for Evomark
what it is: 
- A framework for working with AIGC (AI generated content) models in python

what it does: 
- Control AIGC workflow by writing python code
- The workflow and human give feedback to each other by modifying (evolving) the code

its important consideration: 
- Cache whenever possible to save the number of API calls
- Everything happen in one place: no copy and paste
- Easy to give human feedback

writing requirement: Use simple language and short sentences. Use bullet points in the Markdown format if possible.
"""""

a = answer(em)
show(a)
"""""show
# Introduction to Evomark

Evomark is a powerful Python framework that allows you to control your AI-generated content workflow. With Evomark, you can modify and improve your AIGC models by writing Python code and receiving feedback from humans.

Here are some of the things that Evomark can do:

- Control AIGC workflow by writing Python code
- Allow workflow and human feedback to evolve code
- Cache whenever possible to save API calls
- Keep everything in one place to avoid copy-and-paste
- Provide an easy way to receive human feedback

Evomark is an essential tool for anyone working with AI-generated content models. With its simple language and short sentences, it's easy to understand and use. Whether you're a beginner or an experienced developer, Evomark can help improve your AIGC models and workflow.
"""""

out("""
# Evomark

""")
out(a)

# By update(), the code can modify itself, that is, evolve!
evolve()