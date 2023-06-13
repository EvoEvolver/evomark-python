import openai
import os
from evomark import EvolverInstance
from evomark.data_type.chatlog import ChatLog
from evomark.data_type.var_types import ValueByInput

openai.api_key = os.getenv("EVOMARK_OPENAI_KEY")

default_kwargs_cpl_openai = {"max_tokens": 1000, "model": "text-davinci-003"}


def cpl(prompt, **kwargs):
    """
    The function that calls the OpenAI API to generate text based on
    the prompt.
    :param prompt: The prompt to feed to the API
    :param use_cache: Whether to use cache
    :param cache_holder: The file path with which the cache is associated
    :param kwargs: Other arguments to pass to the OpenAI API
    :return:
    """
    input = str(prompt)
    options = {**default_kwargs_cpl_openai, **kwargs}
    func = lambda x: _cpl(x, options)

    _, _, stack = EvolverInstance.get_context()
    cache = EvolverInstance.read_cache(input, "cpl", stack[0].filename)
    if cache.value is not None:
        return ValueByInput.from_cache(cache, func)

    result_text = func(input)

    cache.set_cache(result_text)
    return ValueByInput.from_cache(cache, func)


def _cpl(prompt, options):
    return openai.Completion.create(prompt=prompt, **options).text.strip()


default_kwargs_edit_openai = {"model": "text-davinci-edit-001"}


def edit(text, instruction, **kwargs):
    input = (str(text), str(instruction))
    options = {**default_kwargs_edit_openai, **kwargs}
    func = lambda x: _edit(x, options)

    _, _, stack = EvolverInstance.get_context()
    cache = EvolverInstance.read_cache(input, "edit", stack[0].filename)
    if cache.value is not None:
        return ValueByInput.from_cache(cache, func)

    result_text = func(input)

    cache.set_cache(result_text)
    return ValueByInput.from_cache(cache, func)


def _edit(input, options):
    return openai.Edit.create(input=input[0], instruction=input[1], **options).choices[0].text


def init_chat(init_message: any, system_message: any = None) -> ChatLog:
    chat = ChatLog(system_message)
    chat.add_user_message(init_message)
    return chat


def ask(message: any, chat: ChatLog = None):
    if chat is None:
        return init_chat(message)
    chat.add_user_message(message)
    return chat


default_kwargs_chat_openai = {"model": "gpt-3.5-turbo"}

def _answer(messages, options):
    return openai.ChatCompletion.create(messages=messages, **options).choices[0].message.content

def answer(chat: ChatLog, **kwargs):
    input = chat.get_log_list()
    options = {**default_kwargs_chat_openai, **kwargs}
    func = lambda x: _answer(x, options)

    _, _, stack = EvolverInstance.get_context()
    cache = EvolverInstance.read_cache(input, "chat", stack[0].filename)
    if cache.value is not None:
        return ValueByInput.from_cache(cache, func)

    result_text = func(input)
    chat.add_assistant_message(result_text)

    cache.set_cache(result_text)
    return ValueByInput.from_cache(cache, func)



