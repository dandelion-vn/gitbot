"""Example NumPy style docstrings.

This module demonstrates documentation as specified by the `NumPy
Documentation HOWTO`_. Docstrings may extend over multiple lines. Sections
are created with a section header followed by an underline of equal length.

Example
-------
Examples can be given using either the ``Example`` or ``Examples``
sections. Sections support any reStructuredText formatting, including
literal blocks::

    $ python example_numpy.py


Section breaks are created with two blank lines. Section breaks are also
implicitly created anytime a new section starts. Section bodies *may* be
indented:

Notes
-----
    This is an example of an indented section. It's like any other section,
    but the body is indented to help it stand out from surrounding text.

If a section is indented, then a section break is created by
resuming unindented text.

Attributes
----------
module_level_variable1 : int
    Module level variables may be documented in either the ``Attributes``
    section of the module docstring, or in an inline docstring immediately
    following the variable.

    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.


.. _NumPy Documentation HOWTO:
   https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

"""

import os
import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

routes = web.RouteTableDef()

router = routing.Router()

"""int: Module level variable documented inline.

The docstring may span multiple lines. The type may optionally be specified
on the first line, separated by a colon.
"""


@router.register("issues", action="opened")
async def issue_opened_event(event, git):
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Parameters
    ----------
    param1 : int
        The first parameter.
    param2 : str
        The second parameter.

    Returns
    -------
    bool
        True if successful, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """

    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = (
        f"Thanks for the report @{author}! " f"I will look into it ASAP! (I'm a bot)."
    )
    await git.post(url, data={"body": message})


@routes.post("/")
async def main(request):
    """This is an example of a module level function.

   Function parameters should be documented in the ``Parameters`` section.
   The name of each parameter is required. The type and description of each
   parameter is optional, but should be included if not obvious.

   If ``*args`` or ``**kwargs`` are accepted,
   they should be listed as ``*args`` and ``**kwargs``.

   The format for a parameter is::

       name : type
           description

           The description may span multiple lines. Following lines
           should be indented to match the first line of the description.
           The ": type" is optional.

           Multiple paragraphs are supported in parameter
           descriptions.

   Parameters
   ----------
   param1 : int
       The first parameter.
   param2 : :obj:`str`, optional
       The second parameter.
   *args
       Variable length argument list.
   **kwargs
       Arbitrary keyword arguments.

   Returns
   -------
   bool
       True if successful, False otherwise.

       The return type is not optional. The ``Returns`` section may span
       multiple lines and paragraphs. Following lines should be indented to
       match the first line of the description.

       The ``Returns`` section supports any reStructuredText formatting,
       including literal blocks::

           {
               'param1': param1,
               'param2': param2
           }

   Raises
   ------
   AttributeError
       The ``Raises`` section is a list of all exceptions
       that are relevant to the interface.
   ValueError
       If `param2` is equal to `param1`.

   """

    body = await request.read()

    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")

    event = sansio.Event.from_http(request.headers, body, secret=secret)
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "dandelion-vn", oauth_token=oauth_token)
        await router.dispatch(event, gh)
    return web.Response(status=200)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
