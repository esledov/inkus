# inkus

Inkus is a python SimpleHTTPServer that renders mako templates

It allows you to embed python code into html pages. In a way, it is similar to php, 
but uses python in code blocks instead.

Inkus can serve any html template "as is" without any modifications. Make a copy of pages 
that require special treatment and give them .mako extension. Now they can be accessed as 
pagename.htm from a browser.

Then you can run [Mako templates](http://www.makotemplates.org) (and python) magic on them:

 * define blocks of content that should be easily modified, 
 * make a layout template and inherit your page templates from it, 
 * create python functions directly in the template, 
 * fetch and show data stored somewhere else (for example, in MS Excel or json files), 
 * programmatically rearrange html snippets, etc etc.

Inkus encourages a gradual coversion and does not force you to create new content types unless 
it is absolutely necessary. It is perfectly OK to leave things as html as long as they are manageable.

## Installation

You do need to have mako templates installed.

    pip install Mako
    
Inkus.py itself is a single file. Just drop it into your project folder and run it.

See [http://sledov.com/inkus-python-in-html.htm](http://sledov.com/inkus-python-in-html.htm) for details.