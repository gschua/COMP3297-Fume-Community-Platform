from django.db import models

class Admin(models.Model):
	def __str__(self):
		return self.username
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)

class Publisher(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=254)

class Genre(models.Model):
	def __str__(self):
		return self.text
	text = models.CharField(max_length=30)

class Platform(models.Model):
	def __str__(self):
		return self.text
	text = models.CharField(max_length=30)

class Game(models.Model):
	def __str__(self):
		return self.title
	title = models.CharField(max_length=254)
	price = models.FloatField(default=0.0)
	score = models.FloatField(default=0.0)
	description_short = models.TextField(max_length=500)
	description_long = models.TextField()
	release_date = models.DateField('Release Date')
	large_image = models.ImageField(upload_to='.')
	small_image = models.ImageField(upload_to='.')
	publisher = models.ForeignKey(Publisher)
	genre = models.ForeignKey(Genre)
	platform = models.ForeignKey(Platform)

class Member(models.Model):
	def __str__(self):
		return self.username
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	email = models.EmailField()
	screen_name = models.CharField(max_length=30)
	avatar = models.ImageField(upload_to='.')	# upload_to kwarg not clear
	acc_spending = models.FloatField(default=0.0)
	recommended = models.ManyToManyField(Game)

class Transaction(models.Model):
	def __str__(self):
		return self.datetime
	games = models.ForeignKey(Game)
	member = models.ForeignKey(Member)
	platform = models.ForeignKey(Platform)
	price = models.FloatField(default=0.0)
	rewards_used = models.IntegerField(default=0)
	is_purchased = models.BooleanField(default=False)
	datetime = models.DateTimeField('Date of Purchase', null=True)

class Tag(models.Model):
	def __str__(self):
		return self.text
	name = models.CharField(max_length=254)
	count = models.IntegerField(default=1)
	games = models.ManyToManyField(Game)

class MemberTag(models.Model):
	def __str__(self):
		return self.text
	tag = models.ForeignKey(Tag)
	member =models.ForeignKey(Member)

class Review(models.Model):
	def __str__(self):
		return self.text
	body = models.TextField()
	score = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	member = models.ForeignKey(Member)
	game = models.ForeignKey(Game)

class Reward(models.Model):
	def __str__(self):
		return self.reward_datetime
	REWARD_STATUSES = (
		('act', 'Active'),
		('exp', 'Expired'),
		('use', 'Used'),
	)
	award_datetime = models.DateTimeField('Date of Awarding')
	status = models.CharField(max_length=3, choices=REWARD_STATUSES, default='act')
	member = models.ForeignKey(Member)
	transaction = models.ForeignKey(Transaction, null=True)
