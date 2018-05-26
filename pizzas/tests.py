from django.test import TestCase
from pizzas.models import Pizza,Topping
from django.contrib.auth.models import User

# Create your tests here.

class ModelTest(TestCase):
	
	def setUp(self):
		User.objects.create_user('admin','admin@163.com','admin12345')
		Pizza.objects.create(id=1,name='meat',maker_id=1)
		Topping.objects.create(id=1,pizza_id=1,name='beaf')
		
	def test_pizza_model(self):
		pizza = Pizza.objects.get(name='meat')
		topping = pizza.topping_set.all()[0]
		self.assertEqual(topping.name,'beaf')
		self.assertEqual(pizza.name,'meat')
		self.assertEqual(str(pizza.maker),'admin')
	
	def test_topping_model(self):
		topping = Topping.objects.get(name='beaf')
		self.assertEqual(topping.name,'beaf')
		self.assertEqual(str(topping.pizza),'meat')
		

class LoginActionTest(TestCase):
	
	def setUp(self):
		User.objects.create_user('admin','admin@163.com','admin12345')
	
	def test_username_and_password(self):
		user = User.objects.get(username='admin')
		self.assertEqual(user.username,'admin')
		self.assertEqual(user.email,'admin@163.com')
#		password is jiamiguodezhi  he  admin12345 buxiangdeng
#		self.assertEqual(user.password,'admin12345')
	
	def test_username_or_password_error(self):
		#/login/----->ok   login/------>not ok  404fail
		response = self.client.post('/login/',{'username':'123','password':'123'})
		self.assertEqual(response.status_code,200)
		self.assertIn(b'Please enter a correct username and password',response.content)
	
	"""
	def test_username_or_password_null(self):
		response = self.client.post('/login/',{'username':'','password':''})
		self.assertEqual(response.status_code,200)
		msg = u'请填写此字段' 
		msg1 = msg.encode(encoding='UTF-8',errors='ignore')
		self.assertIn(msg1,response.content)
	"""
	
	def test_login_success(self):
		response = self.client.post('/login/',{'username':'admin','password':'admin12345'})
		self.assertEqual(response.status_code,302)
	
	def test_logout_success(self):
		response = self.client.post('/logout/',{'username':'admin','password':'admin12345'})
		self.assertEqual(response.status_code,302)
	
	def test_register_success(self):
		response = self.client.post('/register/',{'username':'123','password':'pizzatest'})
		self.assertIn(b'123',response.content)
		self.assertEqual(response.status_code,200)
		response1 = self.client.get('')
		self.assertIn(b'123',response.content)

class IndexTest(TestCase):
	
	def setUp(self):
		User.objects.create_user('admin','admin@163.com','admin12345')
	
	def test_unlogin_index(self):
		response = self.client.get('')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'pizzas/index.html')
	
	def test_login_index(self):
		response = self.client.post('/login/',{'username':'admin','password':'admin12345'})
		response1 = self.client.get('')
		self.assertIn(b'admin',response1.content)

class PizzasTest(TestCase):
	
	def setUp(self):
		User.objects.create_user('admin','admin@163.com','admin12345')
		User.objects.create_user('silan','silan@163.com','silan12345')
		Pizza.objects.create(id=1,name='meat',maker_id=1,public=True)
		Pizza.objects.create(id=2,name='fruit',maker_id=1,public=False)
		Pizza.objects.create(id=3,name='vegetable',maker_id=2,public=True)
		Topping.objects.create(id=1,pizza_id=1,name='beaf')
		Topping.objects.create(id=2,pizza_id=3,name='potato')
	
	def test_pizzas_unlogin(self):
		response = self.client.get('/pizzas/')
		self.assertIn(b'meat',response.content)
		self.assertIn(b'vegetable',response.content)
		self.assertNotIn(b'fruit',response.content)
	
	def test_pizzas_login_private(self):
		self.client.post('/login/',{'username':'admin','password':'admin12345'})
		response = self.client.get('/pizzas/')
		self.assertIn(b'meat',response.content)
		self.assertIn(b'vegetable',response.content)
		self.assertNotIn(b'fruit',response.content)

	def test_pizzas_login_public(self):
		self.client.post('/login/',{'username':'silan','password':'silan12345'})
		response = self.client.get('/pizzas/')
		self.assertIn(b'meat',response.content)
		self.assertIn(b'vegetable',response.content)
		self.assertNotIn(b'fruit',response.content)
	
	def test_mypizzas_unlogin(self):
		response = self.client.get('/my_pizzas/')
		self.assertEqual(response.status_code,302)
		
	def test_mypizzas_login_private(self):
		self.client.post('/login/',{'username':'admin','password':'admin12345'})
		response = self.client.get('/my_pizzas/')
		self.assertIn(b'meat',response.content)
		self.assertNotIn(b'vegetable',response.content)
		self.assertIn(b'fruit',response.content)
		
		self.client.post('/login/',{'username':'silan','password':'silan12345'})
		response = self.client.get('/my_pizzas/')
		self.assertNotIn(b'meat',response.content)
		self.assertIn(b'vegetable',response.content)
		self.assertNotIn(b'fruit',response.content)

	def test_pizza_unlogin(self):
		response = self.client.get('/pizzas/1/')
		self.assertEqual(response.status_code,200)
		self.assertNotIn(b'Edit',response.content)
		self.assertNotIn(b'Delete',response.content)
		response1 = self.client.get('/pizzas/2/')
		self.assertEqual(response1.status_code,404)
	
	def test_pizza_login(self):
		self.client.post('/login/',{'username':'silan','password':'silan12345'})
		response = self.client.get('/pizzas/1/')
		self.assertEqual(response.status_code,200)
		self.assertNotIn(b'Edit',response.content)
		self.assertNotIn(b'Delete',response.content)
		response1 = self.client.get('/pizzas/2/')
		self.assertEqual(response1.status_code,404)
		response2 = self.client.get('/pizzas/3/')
		self.assertEqual(response2.status_code,200)
		self.assertIn(b'Edit',response2.content)
		self.assertIn(b'Delete',response2.content)
		
	def test_new_pizza_unlogin(self):
		response = self.client.get('/new_pizza/')
		self.assertEqual(response.status_code,302)
		
	def test_new_pizza_login(self):
		self.client.post('/login/',{'username':'silan','password':'silan12345'})
		response = self.client.post('/new_pizza/',{'name':'test','check_public':'1'})
		self.assertEqual(response.status_code,302)
		response1 = self.client.get('/pizzas/')
		self.assertIn(b'test',response1.content)
		response2 = self.client.post('/new_pizza/',{'name':'test1'})
		self.assertEqual(response2.status_code,302)
		response3 = self.client.get('/pizzas/')
		self.assertNotIn(b'test1',response3.content)

	def test_edit_pizza_unlogin(self):
		response = self.client.get('/edit_pizza/1/')
		self.assertEqual(response.status_code,302)
	
	def test_edit_pizza_login(self):
		self.client.post('/login/',{'username':'silan','password':'silan12345'})
		response = self.client.post('/edit_pizza/3/',{'name':'vegetabletest'})
		self.assertEqual(response.status_code,302)
		response1 = self.client.get('/pizzas/')
		self.assertNotIn(b'vegetabletest',response1.content)
		response2 = self.client.get('/my_pizzas/')
		self.assertIn(b'vegetabletest',response2.content)
		response3 = self.client.get('/edit_pizza/1/')
		self.assertEqual(response3.status_code,404)
		
	def test_delete_pizza_unlogin(self):
		response = self.client.get('/del_pizza/1/')
		self.assertEqual(response.status_code,302)
		
	def test_delete_pizza_login(self):
		self.client.post('/login/',{'username':'silan','password':'silan12345'})
		response = self.client.post('/del_pizza/1/')
		self.assertEqual(response.status_code,404)
		response1 = self.client.post('/del_pizza/3/')
		self.assertEqual(response1.status_code,302)
		response2 = self.client.get('/pizzas/')
		self.assertNotIn(b'vegetable',response2.content)
		response3 = self.client.get('/my_pizzas/')
		self.assertNotIn(b'vegetable',response3.content)

class ToppingTest(TestCase):
	
	def setUp(self):
		User.objects.create_user('admin','admin@163.com','admin12345')
		User.objects.create_user('silan','silan@163.com','silan12345')
		Pizza.objects.create(id=1,name='meat',maker_id=1,public=True)
		Pizza.objects.create(id=2,name='fruit',maker_id=1,public=False)
		Pizza.objects.create(id=3,name='vegetable',maker_id=2,public=True)
		Topping.objects.create(id=1,pizza_id=1,name='beaf')
		Topping.objects.create(id=2,pizza_id=3,name='potato')
	
	def test_topping_unlogin(self):
		response = self.client.get('/pizzas/1/')
		self.assertEqual(response.status_code,200)
		self.assertIn(b'beaf',response.content)

	def test_topping_login(self):
		self.client.post('/login/',{'username':'admin','password':'admin12345'})
		response = self.client.get('/pizzas/1/')
		self.assertEqual(response.status_code,200)
		self.assertIn(b'beaf',response.content)
		response1 = self.client.get('/pizzas/2/')
		self.assertEqual(response1.status_code,200)
		self.assertIn(b'There are no toppings for this pizza yet',response1.content)
		
	def test_new_topping_unlogin(self):
		response = self.client.get('/new_topping/1/')
		self.assertEqual(response.status_code,302)
	
	def test_new_topping_login(self):
		self.client.post('/login/',{'username':'admin','password':'admin12345'})
		response = self.client.post('/new_topping/1/',{'name':'checkin'})
		self.assertEqual(response.status_code,302)
		response1 = self.client.get('/pizzas/1/')
		self.assertIn(b'checkin',response1.content)
		
		response2 = self.client.post('/new_topping/2/',{'name':'apple'})
		self.assertEqual(response2.status_code,302)
		response3 = self.client.get('/pizzas/2/')
		self.assertIn(b'apple',response3.content)
		
		self.client.post('/login/',{'username':'silan','password':'silan12345'})
		response4 = self.client.get('/new_topping/1/')
		self.assertEqual(response4.status_code,404)
		response5 = self.client.get('/pizzas/1/')
		self.assertIn(b'checkin',response5.content)
		
	def test_edit_topping_unlogin(self):
		response = self.client.get('/edit_topping/1/')
		self.assertEqual(response.status_code,302)
	
	def test_edit_topping_login(self):
		self.client.post('/login/',{'username':'admin','password':'admin12345'})
		response = self.client.post('/edit_topping/1/',{'name':'pork'})
		self.assertEqual(response.status_code,302)
		response1 = self.client.get('/pizzas/1/')
		self.assertIn(b'pork',response1.content)
		
		response2 = self.client.post('/edit_topping/2/',{'name':'apple'})
		self.assertEqual(response2.status_code,404)
		
		self.client.post('/login/',{'username':'silan','password':'silan12345'})
		self.client.post('/edit_topping/2/',{'name':'tomato'})
		response5 = self.client.get('/pizzas/3/')
		self.assertIn(b'tomato',response5.content)
		response6 = self.client.get('/pizzas/1/')
		self.assertIn(b'pork',response6.content)
	
	def test_delete_topping_unlogin(self):
		response = self.client.get('/del_topping/1/')
		self.assertEqual(response.status_code,302)
	
	def test_delete_topping_login(self):
		self.client.post('/login/',{'username':'admin','password':'admin12345'})
		response = self.client.post('/del_topping/1/')
		self.assertEqual(response.status_code,302)
		response1 = self.client.get('/pizzas/1/')
		self.assertNotIn(b'beaf',response1.content)
		response3 = self.client.post('/del_topping/2/')
		self.assertEqual(response3.status_code,404)




		
