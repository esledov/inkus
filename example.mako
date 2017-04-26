<%

    from datetime import datetime

    rows = [[v for v in range(0,10)] for row in range(0,5)]

%>

<%def name="makerow(row)">
    <tr>
    % for name in row:
        <td>${name}</td>\
    % endfor
    </tr>
</%def>

<html>
    <body>
        <h2>Page example</h2>
        <p>
            This is an <b>example</b> file <br/>
            It is rendered on the fly from example.mako template
        </p>
        <img src="img.jpg">
        <p>Yes, I can see images!</p>

        <p>
            And import modules:<br/>
            Today is ${datetime.now().strftime('%d %B, %Y')}
        </p>

        <p>And show some calculated data using functions defined in template</p>

        <table border="1" cellspacing="0" cellpadding="5">
            % for row in rows:
                ${makerow(row)}
            % endfor
        </table>

        <p>Isn't it neat?</p>

    </body>
</html>