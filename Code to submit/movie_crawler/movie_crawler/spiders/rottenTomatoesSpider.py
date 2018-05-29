import scrapy
import json
import csv

class rottenTomatoesSpider(scrapy.Spider):
	name = "rottenTomatoes"

	def start_requests(self):
		base_url = 'https://www.rottentomatoes.com/m/'

		with open('all_movies', 'r') as f:
			for row in f:
				url = base_url + row
				yield scrapy.Request(url=url, callback=self.parse)    

	def parse(self, response):
		jsonFile = json.loads(response.css('#jsonLdSchema::text').extract()[0])
		features = dict()

		features['name'] = jsonFile['name']
		features['genre'] = jsonFile['genre']
		features['timeCinema'] = response.css('.content-meta.info time::attr(datetime)').extract()[0]
		features['contentRating'] = jsonFile['contentRating']
		features['company'] = jsonFile['productionCompany']['name']
		features['duration'] = response.css('.content-meta.info time::attr(datetime)').extract()[-1]
		features['synopsis'] = response.css('#movieSynopsis::text').extract()[0]
		features['rating'] = jsonFile['aggregateRating']['ratingValue']

		content = response.css('.content-meta.info li div::text').extract()
		features['box-office'] = [s for s in content if '$' in s][0]

		with open('../data/dataset.csv', 'a+') as f:
			fieldnames = ['name', 'genre', 'timeCinema', 'contentRating', 'company', 'duration', 'synopsis', 'rating', 'box-office']
			writer = csv.DictWriter(f, fieldnames=fieldnames)
			writer.writerow(features)




