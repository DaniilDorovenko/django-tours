from random import sample

from django.shortcuts import render
from django.views.generic import View

from data import tours, departures, title, subtitle, description


def import_tour_id(tours):
    for tour in tours:
        tours[tour]['id'] = tour


import_tour_id(tours)


class MainView(View):

    def get(self, request, ):
        random_tours = self.get_random_tours(6, tours)
        return render(request, 'index.html',
                      {'title': title,
                       'subtitle': subtitle,
                       'description': description,
                       'random_tours': random_tours})

    @staticmethod
    def get_random_tours(tours_number: int, tours_data: dict) -> list:
        """
        :param tours_number: number of random tours to return
        :param tours_data: dict of all tours
        :return: list of random tours.
        """
        random_list = sample(range(1, len(tours_data)), tours_number)
        result = []
        for tour_id in random_list:
            result.append(tours_data[tour_id])
        return result


class DepartureView(View):

    def get(self, request, departure):
        filtered_tours_by_departures = self.get_filtered_tours_by_departures(
            departure_code=departure,
            tours=tours)
        departure_name = TourView.departure_name_from_code(
            departure,
            departures)
        tours_count_founded = len(filtered_tours_by_departures)
        max_price = sorted(
            filtered_tours_by_departures,
            key=lambda i: i['price'])[-1]['price']
        min_price = sorted(
            filtered_tours_by_departures,
            key=lambda i: i['price'])[0]['price']
        max_nights = sorted(
            filtered_tours_by_departures,
            key=lambda i: i['nights'])[-1]['nights']
        min_nights = sorted(
            filtered_tours_by_departures,
            key=lambda i: i['nights'])[0]['nights']

        tours_founded = ''

        if tours_count_founded == 0:
            tours_founded = 'Туров не найдено.'
        elif tours_count_founded == 1:
            tours_founded = \
                f'Найден один тур стоимостью ' \
                f'{max_price} на {min_nights} ночей.'
        elif 1 < tours_count_founded < 5:
            tours_founded = \
                f'Найдено {tours_count_founded} тура от ' \
                f'{min_price} до {max_price} ' \
                f'и от {min_nights} до {max_nights} ночей'
        elif tours_count_founded >= 5:
            tours_founded = \
                f'Найдено {tours_count_founded} туров от ' \
                f'{min_price} до {max_price} и от ' \
                f'{min_nights} до {max_nights} ночей'

        return render(request, 'departure.html', {
            'filtered_tours_by_departures': filtered_tours_by_departures,
            'departure_name': departure_name,
            'tours_founded': tours_founded,
                                                  })

    @staticmethod
    def get_filtered_tours_by_departures(
            departure_code: str,
            tours: dict) -> list:
        """
        :param departure_code: code of the city to filter by tours
        :param tours: dict of all tours
        :return: list of filtered tours
        """
        filtered_departures = []
        for tour in tours.values():
            if departure_code == tour['departure']:
                filtered_departures.append(tour)
        return filtered_departures


class TourView(View):

    def get(self, request, tour_id):
        tour = tours[tour_id]
        tour['graphical_stars'] = \
            self.text_numbers_to_stars(tour['stars'])
        tour['departure_name'] = \
            self.departure_name_from_code(tour['departure'], departures)
        return render(request, 'tour.html', {'tour': tour})

    @staticmethod
    def text_numbers_to_stars(text_numbers: str) -> str:
        """
        :param text_numbers: number of stars of the hotel
        :return: star symbols
        """
        return int(text_numbers) * "&#9733;"

    @staticmethod
    def departure_name_from_code(
            departure_code: str,
            departure_code_list: dict) -> str:
        """
        :param departure_code: code of the city to return
        :param departure_code_list: list of codes
        :return: name of the city
        """
        return departure_code_list[departure_code]


def page_not_found(request, exception):
    context = {}
    response = render(request, "pages/errors/_404.html", context=context)
    response.status_code = exception
    return response


def server_error(exception):
    context = {}
    response = render("pages/errors/_500.html", context=context)
    response.status_code = exception
    return response
