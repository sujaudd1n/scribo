class HTMLElement:
    def __init__(
        self, nodeName, children=None, style=None, classList=None, id=None, title=None
    ):
        self.nodeName = nodeName
        self.children = children if children is not None else []
        self.style = style if style is not None else {}
        self.classList = classList if classList is not None else []
        self.id = id
        self.title = title

    def __str__(self):
        return self.nodeName

    @property
    def innerHTML(self):
        # childrensInnerHTML = [
            # child.innerHTML for child in self.children
        # ]

        childrensInnerHTML = []
        for child in self.children:
            childrensInnerHTML.append(child.innerHTML)
        
        styles=[]
        for prop, value in self.style.items():
            styles.append(f"{prop}: {value}")

        styles = ';'.join(styles)

        mydom = f"""\
<{self.nodeName} style="{styles}">
    {'\n'.join(childrensInnerHTML)}
</{self.nodeName}>
        """
        return mydom


class HTMLTextElement(HTMLElement):
    def __init__(self, textContent):
        self.textContent = textContent
    
    def __str__(self):
        return f"#text {self.textContent}"
    
    @property
    def innerHTML(self):
        return self.textContent


class HTMLAnchorElement(HTMLElement):
    def __init__(self, href="#", target="_blank", title=None, children=None, style=None):
        self.nodeName = "a"
        self.href = href
        self.target = target
        super().__init__(self.nodeName, children=children, style=style, title=title)

    @property
    def innerHTML(self):
        childrensInnerHTML = []
        for child in self.children:
            childrensInnerHTML.append(child.innerHTML)

        mydom = f"""\
<{self.nodeName} target="{self.target}" href="{self.href}">
    {'\n'.join(childrensInnerHTML)}
</{self.nodeName}>
        """
        return mydom


    


class HTMLParagraphElement(HTMLElement):
    def __init__(self, children, style={}):
        self.nodeName = "p"
        super().__init__(self.nodeName, children=children, style=style)