import scrapy
import re

countries = ['American', 'Australian', 'British', 'Bollywood', 'French']

class wikiMovieSpider(scrapy.Spider):
	name = 'wikiMovie'

	def start_requests(self):
		base_url = 'https://en.wikipedia.org/wiki/List_of_@_films_of_'

		for country in countries:	
			for year in range(2000,2018):
				url = base_url.replace('@', country)+str(year)
				yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		year = response.url.split('_')[-1]
		country = response.url.split('_')[-4]
		filename = 'movies_' + country + '_' + year

		with open(filename, 'w') as f:
			movies = response.css("table.wikitable i a::text").extract()
			for movie in movies:
				clean = movie.lower().replace(' ', '_').replace('&', 'and')
				clean = re.sub('[^A-Za-z0-9_]+', '', clean)
				f.write(clean+'\n')
				f.write(clean+'_'+year+'\n')

		self.log('Saved file %s' % filename)



