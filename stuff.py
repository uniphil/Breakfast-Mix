#!/usr/bin/env python2

class Measure(object):
    def __init__(self, amount):
        self.amount = amount

    def __rmul__(self, lhs):
        """convert literal numbers to measures by multiplying"""
        scaled = lhs * self.amount
        return type(self)(scaled)
    
    def __add__(self, rhs):
        sum = rhs.amount + self.amount
        return type(self)(sum)

    def __str__(self):
        for multiplier, unit_name in self.unit_names.items():
            human_amount = self.amount * multiplier
            human_unit = unit_name
            if human_amount >= 0.1:
                break
        return "{:.2f} {}".format(human_amount, human_unit)

class Mass(Measure):
    unit_names = {1: "kilograms",
                  1000: "grams",
                  1000000: "milligrams"}

class Energy(Measure):
    unit_names = {1: "calories"}

class Percent(Measure):
    unit_names = {1: "percent"}

g = Mass(0.001)
mg = Mass(0.000001)
cal = Energy(1)
percent = Percent(1)


def from_serving(size, **facts):
    return dict((name, type(value)(value.amount/float(size.amount))) for name, value in facts.items())


nutrients = {
    'hemp hearts': from_serving(30*g,
        calories=170*cal,
        saturated=1.5*g,
        omega6=8*g,
        omega3=2.5*g,
        monounsaturated=1.5*g,
        sodium=3*mg,
        fibre=3*g,
        sugar=1*g,
        protein=10*g,
        calcium=2*percent,
        iron=30*percent,
        thiamine=30*percent,
        riboflavin=6*percent,
        b6=10*percent,
        folate=15*percent,
        phosphorus=40*percent,
        magnesium=70*percent,
        zinc=30*percent,
        manganese=110*percent,
    ),
    'walnuts': from_serving(30*g,
        calories=200*cal,
        saturated=2*g,
        fibre=2*g,
        sugar=1*g,
        protein=5*g,
        calcium=2*percent,
        iron=4*percent,
    ),
    'almonds': from_serving(50*g,
        calories=290*cal,
        saturated=2*g,
        potassium=360*mg,
        fibre=6*g,
        sugar=2*g,
        protein=11*g,
        calcium=10*percent,
        iron=15*percent,
    ),
    'chia seeds': from_serving(20*g,
        calories=77*cal,
        saturated=0.7*g,
        omega3=4.8*g,
        omega6=1.2*g,
        monounsaturated=0.4*g,
        sodium=4*mg,
        fibres=7*g,
        protein=4*g,
        c=2*percent,
        calcium=15*percent,
        iron=9*percent,
        magnesium=24*percent,
    ),
    'flax seeds': from_serving(20*g,
        calories=90*cal,
        saturated=0.5*g,
        omega3=3.6*g,
        omega6=1*g,  # interpolating from multiple sources
        monounsaturated=1.5*g,
        sodium=5*mg,
        fibre=6*g,
        protein=4*g,
        calcium=8*percent,
        iron=6*percent,
    ),
    'buckwheat groats': from_serving(100*g,
        calories=346*cal,
        saturated=0.6*g,
        omega3=0.8*g,  # polyunsaturated
        monounsaturated=0.8*g,
        sodium=11*mg,
        potassium=320*mg,
        fibre=10.3*g,
        protein=12*g,
        calcium=2*percent,
        iron=14*percent,
    ),
}

class Mix(object):
    def __init__(self, serving, ingredients):
        self.serving = serving
        self.ingredients = ingredients
    
    def amounts(self):
        total = float(sum(self.ingredients.values()))
        masses = {name: amount / total * self.serving for name, amount in self.ingredients.items()}
        return masses

    def nutrition(self):
        masses = self.amounts()
        _nutrition = {}
        for ingredient, amount in masses.items():
            for fact, value in nutrients[ingredient].items():
                serving_value = amount.amount * value
                try:
                    _nutrition[fact] += serving_value
                except KeyError:
                    _nutrition[fact] = serving_value
        return _nutrition

    def __str__(self):
        amounts = "\n".join("  {:<17}{}".format(i, a) for i, a in self.amounts().items())
        nutrition = "\n".join("  {:<16}{}".format(i, v) for i, v in self.nutrition().items())
        return "\nServing Size: {}\n{}\n\nNUTRITION\n{}\n".format(self.serving, amounts, nutrition)


my_mix = Mix(serving=60*g, ingredients={
    'hemp hearts': 5,
    'walnuts': 8,
    'almonds': 8,
    'chia seeds': 3,
    'flax seeds': 2,
    'buckwheat groats': 1,
})


print my_mix
