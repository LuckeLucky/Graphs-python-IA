from __future__ import print_function, unicode_literals
from PyInquirer import Validator, ValidationError, prompt
import os

import exceptions
from map import Map


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


class ValidateLocation(Validator):
    def validate(self, document):
        try:
            graph.get_location(document.text)
        except exceptions.InexistentLocationError:
            raise ValidationError(
                message='Please enter a valid location',
                cursor_position=len(document.text))  # Move cursor to end


def ask_map_to_load():
    import glob
    maps = glob.glob("Maps/*.json")
    choose_map = [
        {
            'type': 'list',
            'name': 'map_json',
            'message': 'Which map you want to load?',
            'choices': maps
        }
    ]
    answers = prompt(choose_map)
    return answers['map_json']


def ask_algorithm():
    algoithm_setup = [
        {
            'type': 'list',
            'name': 'algorithm',
            'message': 'Which search algorithm you wanna use?',
            'choices': ['Uniform Cost', 'Limited Depth', 'A*', 'Greddy Search']
        },
        {
            'type': 'input',
            'name': 'depth',
            'message': 'What\'s the maximum depth?',
            'validate': NumberValidator,
            'when': lambda answers: answers['algorithm'] == 'Limited Depth'
        },
        {
            'type': 'input',
            'name': 'source',
            'message': 'What\'s the source name?',
            'validate': ValidateLocation
        },
        {
            'type': 'input',
            'name': 'destination',
            'message': 'What\'s the destination name?',
            'validate': ValidateLocation,
            'when': lambda answers: answers['algorithm'] not in ['A*', 'Greddy Search']
        },
        {
            'type': 'list',
            'message': 'Show algorithm process?',
            'name': 'confirm',
            'choices': ['Yes', 'No'],
        }
    ]
    answers = prompt(algoithm_setup)
    return answers


def ask_more():
    exit_question = [
        {
            'type': 'list',
            'message': 'Do you want to continue?',
            'name': 'continue',
            'choices': ['Yes', 'No'],
        }
    ]

    answers = prompt(exit_question)
    return answers


if __name__ == '__main__':
    map_chose = ask_map_to_load()
    graph = Map(map_chose)
    while True:
        answers = ask_algorithm()
        try:
            if answers['confirm'] == 'Yes':
                answers['confirm'] = True
            else:
                answers['confirm'] = False
            path = []
            if answers['algorithm'] == 'Uniform Cost':
                path = graph.uniform_cost_search(answers['source'], answers['destination'], answers['confirm'])
            if answers['algorithm'] == 'Limited Depth':
                path = graph.limited_depth(answers['source'], answers['destination'], int(answers['depth']),
                                           answers['confirm'])
            if answers['algorithm'] == 'A*':
                answers['destination'] = 'Faro'
                path = graph.a_star(answers['source'], answers['confirm'])
            if answers['algorithm'] == 'Greddy Search':
                answers['destination'] = 'Faro'
                path = graph.greedy_search(answers['source'], answers['confirm'])

            print("Path from " + answers['source'] + " to " + answers['destination'] + " using " + answers[
                'algorithm'] + ":")
            print(path[0] + " com uma distância de " + path[1] + "km")
        except exceptions.PathNotFoundError:
            print('There is no path between ' + answers['source'] + ' and ' + answers['destination'])
        except exceptions.InexistentLocationError:
            print('No location')

        answer_continue = ask_more()
        if answer_continue['continue'] == 'No':
            break
        os.system('cls' if os.name == 'nt' else 'clear')


