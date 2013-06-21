# For the automated writing of recipes
import codecs

class Ingredient(object):
	def __init__(self,name):
		self.name = name
		self.qty = ""
		self.units = ""
	def show(self):
		if self.name != 'f':
			print '\t' + self.qty + ' ' + self.units + ' of ' + self.name
		else:
			print '/' + self.qty + '/'
	def latex(self):
		if self.name != 'f':
			out = "\\ing["+self.qty+"]{"+self.units+"}{"+self.name+"}"
		else: 
			out = "\\freeform "+self.qty
		return out
	def js(self):
		return 'name: "'+self.name+'", qty: "'+self.qty+'", units: "'+self.units+'"'

class Step(object):
	def __init__(self,number):
		self.number = number
		self.ingredients = []
		self.description = ""
	def show(self):
		print "----------"
		print "Step Number %i:" % self.number
		for ingredient in self.ingredients:
			ingredient.show()
		print self.description
	def latex(self):
		out = ''
		for ingredient in self.ingredients:
			out += ingredient.latex() + '\n'
		out += self.description
		return out
	def js(self):
		out = ' instruction: "'+self.description+'"'
		out += ',\n ingredients: [\n'
		for ingredient in self.ingredients:
			out += ' {'+ingredient.js() +'},\n'
		out += ']'
		return out

class Recipe(object):
    def __init__(self, title):
        self.title = title
        self.time = ""
        self.size = ""
        self.steps = []
    def show(self):
    	print self.title
    	print "=========="
    	print "Takes " + self.time + "makes " + self.size
    	for step in self.steps:
    		step.show()
    def latex(self):
    	out = "\\begin{recipe}{"+self.title+"}{"+self.size+"}{"+self.time+"}\n"
    	for step in self.steps:
    		out += step.latex()+'\n'
    	out += "\\end{recipe}\n"
    	return out
    def js(self):
    	out = '\n\n//------\n\nwindow.recipes.push(\n{\n'
    	out += ' name: "'+self.title+'"'
    	out += ',\n size: "'+self.size+'"'
    	out += ',\n time: "'+self.time+'"'
    	out += ',\n descr: "'+self.steps[0].ingredients[0].qty+'"'
    	out += ',\n steps: [\n'
    	for step in self.steps:
    		out += '{\n'+step.js()+'\n},\n'
    	out += ']});'
    	return out

while True:
	recipe = Recipe(raw_input('Recipe title? \n'))
	recipe.time = raw_input('Recipe time? \n')
	if recipe.time:  recipe.time += ', '
	recipe.size = raw_input('Recipe size? \n')

	print "Alright! Now you're going to add ingredients and instructions."

	steps = 1

	while steps:
		print("Beginning step %i." % steps)
		step = Step(steps)
		recipe.steps.append(step)
		descr = False

		while True:
			if not descr and steps == 1:
				name = "f"
				descr = True
			else:
				name = raw_input('Name of the next ingredient in this step?\n(put "." to stop adding ingredients, or "f" to leave a comment at this point)\n')

			if name == ".":
				break
			elif name =="f":
				ingredient = Ingredient(name)
				ingredient.qty = raw_input('Enter recipe description (or other comment): \n')
				step.ingredients.append(ingredient)
			else:
				ingredient = Ingredient(name)
				ingredient.qty = raw_input('How much is there of this ingredient? \n')
				ingredient.units = raw_input('In what units? \n')
				step.ingredients.append(ingredient)

		print "You've entered the following ingredients for step %i:" % step.number
		for ingredient in step.ingredients:
			ingredient.show()
		print
		step.description = raw_input('So, what do you do for this step? \n')
		step.show()
		steps += 1
		print "----------"
		if raw_input("Are there more steps? (type 'n' if not)\n") == 'n':
			break

	print "\n\n"
	recipe.show()
	print "\n\n"
	if raw_input("Is the above correct? (type 'n' if not)\n") == 'n':
		print "Starting over...\n\n\n"
	else:
		latex = recipe.latex()
		print latex
		print("Saving latex...")
		with codecs.open('latex/recipes/'+recipe.title+'.tex', mode='w') as outfile:
			outfile.write(latex)

		js = recipe.js()
		print js
		print("Saving js...time for another recipe!")
		with codecs.open('recipes/recipes.js', mode='a', encoding='utf-8') as outfile:
			outfile.write(js)