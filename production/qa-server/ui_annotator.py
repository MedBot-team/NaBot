import html
import streamlit as st
from htbuilder import div
from htbuilder import span
from htbuilder import  styles
from htbuilder import HtmlElement
from htbuilder.units import rem



class HTMLAnnotator():
    def __init__(self):
        super(HTMLAnnotator, self).__init__()

    def annotation(self, body, background="#ddd", color="#333", **style):
        return span(
            style=styles(
                background=background,
                border_radius=rem(0.33),
                color=color,
                padding=(0, rem(0.67)),
                display="inline-flex",
                justify_content="center",
                align_items="center",
                **style,)
            )(html.escape(body))


    def annotated_text(self, *args):
        out = div()

        for arg in args:
            if isinstance(arg, str):
                out(html.escape(arg))

            elif isinstance(arg, HtmlElement):
                out(arg)

            elif isinstance(arg, tuple):
                out(self.annotation(*arg))

            else:
                raise Exception("Wrong format")

        st.markdown(str(out), unsafe_allow_html=True)

