from usda import UsdaClient


client = UsdaClient('gNz4MEeAXWvLdDF2va95mAuIvGjpFn5AcJYiI8Hi')

x = input()

foods_search = client.search_foods(x, 1)
food = next(foods_search)

print(food)
report = client.get_food_report(food.id)

for nutrient in report.nutrients:
    print(nutrient.name, nutrient.value, nutrient.unit)