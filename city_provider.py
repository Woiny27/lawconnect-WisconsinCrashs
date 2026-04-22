from faker.providers import BaseProvider

class CityProvider(BaseProvider):
    def city_name(self):
        cities = [
            "Madison", "Milwaukee", "Green Bay", "Kenosha", "Racine",
            "Appleton", "Waukesha", "Eau Claire", "Oshkosh", "Janesville",
            "West Allis", "La Crosse", "Sheboygan", "Wauwatosa", "Fond du Lac",
            "New Berlin", "Wausau", "Brookfield", "Beloit", "Menomonee Falls",
            "Oak Creek", "West Bend", "Sun Prairie", "Superior", "Stevens Point",
            "Neenah", "Fitchburg", "Muskego", "Cudahy", "Watertown",
            "De Pere", "South Milwaukee", "Middleton", "Menasha", "Whitewater",
            "Greendale", "Pewaukee", "River Falls", "Onalaska", "Marshfield",
            "Mequon", "Franklin", "Mount Pleasant", "Howard", "Ashwaubenon",
            "Baraboo", "Portage", "Hudson", "Chippewa Falls", "Monroe"
        ]
        return self.random_element(cities)
