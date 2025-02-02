
class XPath:
    padding_check = ('//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/dt[4]', "innerHTML")

    def __init__(self, product: str, any_version: bool = False, padding: bool = False):
        self.any_version = any_version
        self.padding = padding
        self.product = product

    @property
    def trend_price(self) -> str:
        if self.any_version:
            to_ret = '//div[contains(@class, "infoContainer")]/dl/dd[4]/span'
        else:
            to_ret = '//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/'
            if self.padding:
               to_ret += 'dd[7]/span'
            else:
                to_ret += 'dd[6]/span'
        return to_ret, "innerHTML"
    
    @property
    def lowest_price(self) -> str:
        if self.any_version:
            to_ret = '//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[4]/div[1]/div/div/span'
        else:
            to_ret = '//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[3]/div[1]/div[1]/div[1]/span'
        return to_ret, "innerHTML"

    @property
    def seller_location(self) -> str:
        if self.any_version:
            to_ret = '//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[3]/div[1]/div[1]/span/span/span[2]'
        else:
            to_ret = '//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[2]/div[1]/div[1]/span/span/span[2]'
        return to_ret, "aria-label"

    @property
    def card_version(self) -> str:
        if self.any_version:
            return '//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[3]/div/div[2]/div/div/a[1]', "aria-label"
        to_ret = '//div[@id="tabContent-info"]/div/div[@class="col-12 col-lg-6 mx-auto"]/div/div[2]/dl/'
        if self.padding:
            to_ret += 'dd[3]/div/a'
        else:
            to_ret += 'dd[2]/div/a'
        if self.product.lower() == "magic":
            to_ret += '[2]'
        return to_ret, "innerHTML"
    
    @property
    def card_condition(self) -> str:
        if self.any_version:
            to_ret = '//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[3]/div/div[2]/div/div/a[2]'
        else:
            to_ret = '//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[2]/div[1]/div[2]/div/div[1]/a'
        return to_ret, "data-bs-original-title"

    @property
    def card_language(self) -> str:
        if self.any_version:
            to_ret = '//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[3]/div/div[2]/div/div/span'
        else:
            to_ret = '//div[contains(@class, "article-table")]/div[@class="table-body"]/div[1]/div[2]/div[1]/div[2]/div/div[1]/span'
        return to_ret, "aria-label"
