class website:
    def __init__(self):
        self.websiteName = ''
        self.websiteDescription = ''
        self.productList = []

class product:
    def __init__(self, name, price = None, imageLink = None, productCategory = None):
        self.name = name
        self.price = price
        self.imageLink = imageLink
        self.productCategory = ''