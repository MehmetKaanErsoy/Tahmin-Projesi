import scrapy
import requests


class Deneme_Spider(scrapy.Spider):
    name = "proje"
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/category/&filter_category_all=true&category_id=1&sort=purchased_365&order=DESC&filter_in_stock=1"
    ]
    page_count = 0
    links_count = 0

    def parse(self, response, **kwargs):

        next_url = response.css("a.next::attr(href)").extract()[0]
        self.page_count += 1
        if next_url is not None and self.page_count != 3:
            yield scrapy.Request(url=next_url, callback=self.parse)

        for link in response.css("div.cover a::attr(href)").getall():
            yield scrapy.Request(link, callback=self.kitap_ozellikleri)

    def kitap_ozellikleri(self, response):
        i = 0
        sayi = response.css("p.purchased::text").extract()
        kitap_Adi = response.css("div.pr_header h1::text").extract()
        yazar = response.css("a.pr_producers__link::text").extract()
        yayınevi = response.css("div.pr_producers__publisher div a.pr_producers__link::text").extract()
        fiyat_TL = response.xpath("//div[@class='price__item']//text()").extract()
        fiyat_KRS = response.xpath("//div[@class='price__item']//small/text()").extract()
        kitap_aciklama = response.css("span.info__text::text").extract()
        """Tür de düzenlemeler yapılmalıdır."""
        tür = response.css("a.rel-cats__link span::text").extract()[-1]

        while i < len(sayi):
            yield {
                "Kitap Adı ": kitap_Adi[i],
                "Yazar ":yazar[i],
                "Yayınevi ": yayınevi[i],
                "Tür": tür[i],
                "Fiyat ": fiyat_TL[i] + fiyat_KRS[i],
                "Açıklama ": kitap_aciklama[i],
                "Kaç Adet Satıldı ": sayi[i],
            }
            i += 1
