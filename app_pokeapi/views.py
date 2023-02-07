from django.shortcuts import render
from bson.objectid import ObjectId
import json
from pymongo import MongoClient
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
# Create your views here.

def pokemon_list(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['pokeapi_co_db']
    collection = db['pokemon_v2_pokemon']
    pokemons = list(collection.find({}))

    # Recorre todos los pokemons y convierte ObjectId a str
    for pokemon in pokemons:
        for key, value in pokemon.items():
            if isinstance(value, ObjectId):
                pokemon[key] = str(value)

    paginator = Paginator(pokemons, 10) # Mostrar 10 pokemons por página
    page = request.GET.get('page')

    try:
        pokemons = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        pokemons = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango, muestra la última página
        pokemons = paginator.page(paginator.num_pages)

    pokemons_list = list(pokemons)

    response = {
        
        'previous_page': None,
        'next_page': None,
        'first_page': None,
        'last_page': None,
        'pokemons': pokemons_list,
    }

    if pokemons.has_previous():
        response['previous_page'] = f'/api/v2/pokemon?page={pokemons.previous_page_number()}'

    if pokemons.has_next():
        response['next_page'] = f'/api/v2/pokemon?page={pokemons.next_page_number()}'

    if pokemons.has_previous() or pokemons.has_next():
        response['first_page'] = f'/api/v2/pokemon?page={paginator.page(1).number}'
        response['last_page'] = f'/api/v2/pokemon?page={paginator.page(paginator.num_pages).number}'
        
    return JsonResponse(response)