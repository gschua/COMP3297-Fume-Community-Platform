from django.db import models

# Create your models here.
class Publisher(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=254)

class Member(models.Model):
	def __str__(self):
		return self.username
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	email = models.EmailField()
	screen_name = models.CharField(max_length=30)
	avatar = models.ImageField(upload_to='uploads/avatars/') #upload_to kwarg not clear

class Genre(models.Model):
	def __str__(self):
		return self.text
	text = models.CharField(max_length=30)

class Game(models.Model):
	def __str__(self):
		return self.title
	platform = models.CharField(max_length=30)
	title = models.CharField(max_length=254)
	price = models.FloatField(default=0.0)
	score = models.FloatField(default=0.0)
	description = models.TextField()
	release_datetime = models.DateTimeField('release date')
	large_image = models.ImageField(upload_to='uploads/large/')
	small_image = models.ImageField(upload_to='uploads/small/')
	publisher = models.ForeignKey(Publisher)
	genre = models.ForeignKey(Genre)

class Transaction(models.Model):
	def __str__(self):
		return self.datetime
	datetime = models.DateTimeField('date of transaction')
	subtotal = models.FloatField(default=0.0)
	num_of_rewards_used = models.IntegerField(default=0)
	actual_amount = models.FloatField(default=0.0)
	status = models.CharField(max_length=254)
	games = models.ManyToManyField(Game)
	member = models.ForeignKey(Member)


class Review(models.Model):
	def __str__(self):
		return self.text
	text = models.TextField()
	score = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	member = models.ForeignKey(Member)

class Reward(models.Model):
	def __str__(self):
		return self.reward_datetime
	reward_datetime = models.DateTimeField('date of reward')
	expiry_datetime = models.DateTimeField('expiry date')
	is_used = models.BooleanField(default=False)
	member = models.ForeignKey(Member)


class Tag(models.Model):
	def __str__(self):
		return self.text
	text = models.CharField(max_length=254)
	count = models.IntegerField(default=0)
	tag_type = models.CharField(max_length=30)
	games = models.ManyToManyField(Game)

class ShoppingCart(models.Model):
	def __str__(self):
		return self.member.username
	games = models.ManyToManyField(Game)
	member = models.OneToOneField(Member)

class Admin(models.Model):
	def __str__(self):
		return self.username
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)