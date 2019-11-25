from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
class Form(models.Model):
	id = models.UUIDField(primary_key=True, default = uuid.uuid4)
	title = models.CharField(max_length = 200)
	description = models.TextField()
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	color = models.TextField()
	font = models.TextField()
	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return reverse('complete-form', args=[str(self.id)])


class Parent_question(models.Model):
	question = models.TextField()
	question_number = models.IntegerField()
	is_required = models.TextField()
	question_type = models.IntegerField()
	form = models.ForeignKey(Form, on_delete = models.SET_NULL, null = True)
	class Meta:
		abstract = True
	def __str__(self):
		return self.question

class Text_question(Parent_question):
	type = models.TextField()

class Long_question(Parent_question):
	pass

class Single_mcq(Parent_question):
	pass

class Multi_mcq(Parent_question):
	pass

class Rating(Parent_question):
	pass

class Toggle(Parent_question):
	is_conditional = models.TextField()

class Drop_down(Parent_question):
	pass

class File_upload(Parent_question):
	extension = models.TextField();

class Parent_option(models.Model):
	option = models.TextField()
	option_number = models.IntegerField()
	class Meta:
		abstract = True

class Single_mcq_option(Parent_option):
	parent = models.ForeignKey(Single_mcq, on_delete=models.SET_NULL, null = True)

class Multi_mcq_option(Parent_option):
	parent = models.ForeignKey(Multi_mcq, on_delete=models.SET_NULL, null = True)

class Drop_down_option(Parent_option):
	parent = models.ForeignKey(Drop_down, on_delete=models.SET_NULL, null = True)

class Text_response(models.Model):
	parent_question = models.ForeignKey(Text_question, on_delete=models.SET_NULL, null=True)
	question_type = 1
	answer = models.CharField(max_length =200)
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class Long_response(models.Model):
	parent_question = models.ForeignKey(Long_question , on_delete=models.SET_NULL, null=True)
	question_type = 2
	answer = models.TextField()
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class Single_mcq_response(models.Model):
	parent_question = models.ForeignKey(Single_mcq, on_delete=models.SET_NULL, null=True)
	parent_option = models.ForeignKey(Single_mcq_option,on_delete=models.SET_NULL, null=True)
	question_type = 3
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class Multi_mcq_response(models.Model):
	parent_question = models.ForeignKey(Multi_mcq, on_delete=models.SET_NULL, null=True)
	parent_option = models.ForeignKey(Multi_mcq_option,on_delete=models.SET_NULL, null=True)
	question_type = 4
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class Toggle_response(models.Model):
	parent_question = models.ForeignKey(Toggle, on_delete=models.SET_NULL, null = True)
	answer = models.IntegerField()
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	question_type = 5

class Drop_down_response(models.Model):
	parent_question = models.ForeignKey(Drop_down, on_delete = models.SET_NULL, null = True)
	parent_option = models.ForeignKey(Drop_down_option, on_delete = models.SET_NULL, null=True)
	question_type = 6
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class File_upload_response(models.Model):
	parent_question = models.ForeignKey(File_upload, on_delete=models.SET_NULL, null=True)
	question_type = 7
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	file = models.FileField() 

class Rating_response(models.Model):
	parent_question = models.ForeignKey(Rating, on_delete= models.SET_NULL, null = True)
	question_type = 8
	owner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
	answer = models.IntegerField()

# class Form_user(models.Model):
# 	form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True)
# 	users = models.ManyToManyField(User)