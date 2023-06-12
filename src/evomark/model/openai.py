import openai
import os
from evomark.core.core import EvolverInstance
from evomark.var_types import ValueByInputHash

openai.api_key = os.getenv("EVOMARK_OPENAI_KEY")

default_kwargs_cpl_openai = {"max_tokens": 1000, "model": "text-davinci-003"}

def cpl(prompt, use_cache=True, cache_holder: str = None, **kwargs):
    """
    The function that calls the OpenAI API to generate text based on
    the prompt.
    :param prompt: The prompt to feed to the API
    :param use_cache: Whether to use cache
    :param cache_holder: The file path with which the cache is associated
    :param kwargs: Other arguments to pass to the OpenAI API
    :return:
    """
    _, _, stack = EvolverInstance.get_context()
    filepath = stack[0].filename if cache_holder is None else cache_holder
    input_hash = EvolverInstance.hash(prompt)
    cache = EvolverInstance.read_cache(input_hash, filepath)
    if cache.type is not None:
        return ValueByInputHash(cache.value, input_hash)

    options = {**default_kwargs_cpl_openai, **kwargs}
    completion = openai.Completion.create(prompt=prompt, **options)

    result_text = completion.choices[0].text
    # Trim the result
    result_text = result_text.strip()
    res = ValueByInputHash(result_text, input_hash)
    cache.type = "text"
    cache.value = result_text

    return res

default_kwargs_edit_openai = {"model": "text-davinci-edit-001"}

def edit(input, instruction, use_cache=True, cache_holder: str = None, **kwargs):
    _, _, stack = EvolverInstance.get_context()
    filepath = stack[0].filename if cache_holder is None else cache_holder
    input_hash = EvolverInstance.hash((input, instruction))
    cache = EvolverInstance.read_cache(input_hash, filepath)
    if cache.type is not None:
        return ValueByInputHash(cache.value, input_hash)

    kwargs = {**default_kwargs_edit_openai, **kwargs}
    completion = openai.Edit.create(input=input, instruction=instruction , **kwargs)

    result_text = completion.choices[0].text
    # Trim the result
    result_text = result_text.strip()
    res = ValueByInputHash(result_text, input_hash)
    cache.type = "text"
    cache.value = result_text

    return res

