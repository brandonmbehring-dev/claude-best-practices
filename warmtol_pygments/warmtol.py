"""
WarmTol Pygments Style — Warm Tol Hybrid palette for code highlighting.

Maps syntax tokens to the 5-hue Warm Tol palette:
- Keywords:  WarmBlue  (#3B6FA0) bold
- Strings:   WarmRose  (#C06858)
- Comments:  gray italic
- Functions: WarmGreen (#4A7E3F)
- Numbers:   WarmGold  (#C09840)
- Operators: DarkText  (#1A1A19)
"""
from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Token,
    Whitespace,
)


class WarmTolStyle(Style):
    """Warm Tol Hybrid — colorblind-safe code highlighting."""

    name = "warmtol"
    background_color = "#F7F5F0"  # CodeBg

    styles = {
        Token:                 "#1A1A19",        # DarkText
        Whitespace:            "#bbbbbb",

        # Comments — gray italic
        Comment:               "italic #888888",
        Comment.Preproc:       "noitalic #3B6FA0",
        Comment.Special:       "bold italic #888888",

        # Keywords — WarmBlue bold
        Keyword:               "bold #3B6FA0",
        Keyword.Constant:      "bold #3B6FA0",
        Keyword.Declaration:   "bold #3B6FA0",
        Keyword.Namespace:     "bold #3B6FA0",
        Keyword.Type:          "#8A4E82",        # WarmPlum for types

        # Operators — DarkText
        Operator:              "#1A1A19",
        Operator.Word:         "bold #3B6FA0",

        # Punctuation
        Punctuation:           "#1A1A19",

        # Names — WarmGreen for functions/classes
        Name:                  "#1A1A19",
        Name.Builtin:          "#3B6FA0",
        Name.Builtin.Pseudo:   "#3B6FA0",
        Name.Class:            "bold #4A7E3F",
        Name.Constant:         "#C09840",        # WarmGold
        Name.Decorator:        "#8A4E82",        # WarmPlum
        Name.Entity:           "#1A1A19",
        Name.Exception:        "bold #C06858",   # WarmRose
        Name.Function:         "#4A7E3F",        # WarmGreen
        Name.Function.Magic:   "#4A7E3F",
        Name.Label:            "#1A1A19",
        Name.Namespace:        "#1A1A19",
        Name.Tag:              "bold #3B6FA0",
        Name.Variable:         "#1A1A19",

        # Strings — WarmRose
        String:                "#C06858",
        String.Affix:          "#C06858",
        String.Backtick:       "#C06858",
        String.Doc:            "italic #888888",
        String.Escape:         "bold #C09840",   # WarmGold for escapes
        String.Interpol:       "bold #C06858",
        String.Regex:          "#C06858",

        # Numbers — WarmGold
        Number:                "#C09840",
        Number.Float:          "#C09840",
        Number.Hex:            "#C09840",
        Number.Integer:        "#C09840",
        Number.Oct:            "#C09840",

        # Literals
        Literal:               "#C09840",

        # Generic (diff output, etc.)
        Generic.Deleted:       "#C06858",
        Generic.Emph:          "italic",
        Generic.Error:         "#C06858",
        Generic.Heading:       "bold #3B6FA0",
        Generic.Inserted:      "#4A7E3F",
        Generic.Output:        "#888888",
        Generic.Prompt:        "bold #3B6FA0",
        Generic.Strong:        "bold",
        Generic.Subheading:    "#8A4E82",
        Generic.Traceback:     "#C06858",

        # Error
        Error:                 "border:#C06858 bg:#C06858",
    }
