from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blog_app.models import Category, Post


class contactform(forms.Form):
	name = forms.CharField(label="Name",max_length=100)
	email = forms.EmailField(label="email",max_length=100)
	message = forms.CharField(label="message",max_length=300)
	
class registerform(forms.ModelForm):
	username = forms.CharField(label="username",max_length=100,required=True)
	email = forms.CharField(label="email",max_length=100,required=True)
	password = forms.CharField(label="password",max_length=100,required=True)
	confirm_password = forms.CharField(label="confirm password",max_length=100,required=True)
	
	
	class Meta:
		model = User
		fields = ['username','email','password']
		
		
	def clean(self):  #custom validation
		cleaned_data = super().clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")
		
		if password and confirm_password and password!=confirm_password:
			raise forms.ValidationError("Password do not match try again")
		
		
class loginform(forms.Form):
	username = forms.CharField(label="username",max_length=100,required=True)
	password = forms.CharField(label="password", max_length=100, required=True)
	
	def clean(self):
		cleaned_data = super().clean()
		username = cleaned_data.get("username")
		password = cleaned_data.get("password")
		
		if username and password:
			user = authenticate(username=username,password=password)
			
			if user is None:
				raise forms.ValidationError("username and password do not match")
			

class forgotpasswordform(forms.Form):
	email = forms.EmailField(label='email',max_length=254,required=True)
	
	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get('email')
		
		if not User.objects.filter(email=email).exists():
			raise forms.ValidationError("No user registered this email")
		
class postform(forms.ModelForm):
	title = forms.CharField(label='title',max_length=200,required=True)
	content = forms.CharField(label='content',required=True)
	category = forms.ModelChoiceField(label='category',queryset=Category.objects.all())
	img_url = forms.ImageField(label='image',required=False)
	class Meta:
		model = Post
		fields = ['title','content','category','img_url']
		
	def clean(self):
		cleaned_data = super().clean()
		title = cleaned_data.get('title')
		content = cleaned_data.get('content')
		
		# custom validations
		if title and len(title)<5:
			raise forms.ValidationError('Title must be atleast 5 characters')
		if content and len(content)<10:
			raise forms.ValidationError('Content must be atleast 10 characters')
		
		def save(self, commit=...):
			Post = super().save(commit)
			cleaned_data = super().clean()
			if cleaned_data.get('img_url'):
				Post.img_url = cleaned_data.get('img_url')
			else:
				img_url = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJQAAACUCAMAAABC4vDmAAAAS1BMVEX////29vaJiYnHx8f8/Pzx8fHf39/5+flsbGzr6+uXl5fb29vX19eysrK3t7fo6OhxcXGfn5+qqqq9vb3Pz897e3uRkZGBgYFhYWEUmgHiAAADyklEQVR4nO2Za2/kKgxAzXsgEMIj5P7/X3pNZradSWZX/bAl1cpH1ahYkXKEiTEJAEEQBEEQBEEQBEEQBEEQBEEQBEH8o0h5DFyicVAw6gX2I6zW2wubukLiMJ43r5/Z8rurvt2IldxJgeEgLv71kukWny8e4uRDSKvbWd0cZrcdrjEOw8g0yApvEha0yfdh6WZNHK+qd+UljFDqsEVgDXjMgNw5zccjLBY2SMou8Skrv0nPPRwXO0TpIfUhIwHemD0CA6Vu+u38KD+nNIv4ISVB30ZJMXEu2BLUvK0tJbetST+s5H7pEN4sawxM6yr2Mi6ndAufuT3tisOQUJfwsbNIv6YfsPVBvOWX4TqsPv0e1pKR8qlK+GW60men3o5dQeaX91Q8HyN61VeIPGGOTQLOEi9XmDyh13iISEinyRuMX891O7SLl9R0kpKQ3SUqn8TlvKrd1emD5dTkse0UGo1rx4jHtX/xotK3QwE3LV1j8kzm95IuH79lORaJC5C8W/1q29GpXutzJ27tI4MsLOPLuZnMm2C6uRqVsjosfPrjpd9C79HPyKnd1o1vy1Y+W4ZxPbp9u4pxQRldq3+xGH3E+hLjpNTX20p96v6+B0xT4+KL8FOp/zYrlfkXyWrcZiPZF/kJJy3ixJ/SckXK+qsMA7GCFCns6xgruCpmD4MsvYbpnCoe5ecwD1vp9j8BNUBJUbS+tfEIFXs60Tt1zfHAbnnVyUOeva9m0MRZ7mQNkqND6ge+FiHMtTsAzN4pyL0VxrODN2bUfgw21eCD4QwdCt4cpVIMKntsWJxBtaShFoGnrOTSsC4hQZpn2du63Ju5FpWDVIVOmD2RU49qscns5ciZgmkrkATY/XNHizHD7DSqZTFprioeRAW6jXzzYvFIFwSwxLHblHhCtx79EpPZ9hMoJk60lg2U1hof1SVIdv+WJu2eHGn2ken/mF4A8I/1GTRSjnu5iJWqSClwYxMMBObIYz3YdSoOpoBL3dRuE+Y5jHq5D5ieCFgEVMIc4gEveGj7zftprxTtoupPneRaD+vR0UTP3ah4mERAPw+uS00lW5SaEutSUrZpmsbkD+8yzcyBTBb3kKyxOv2SyhEHJYikWeovq3kpZZhUSBmfOzHjdLWcXE9fl7IuZGeKxmXVpUD2Z3HUUjdYhmICtU798e/V3MOWcy5Y0bMuDo0Zx7Fac06DvtvKXhIAb4aPn+qPP8NfZa1luPkyZmz3UFZZicE4LH17MXq8y3h30+fgdZ9BCIIgCIIgCIIgCIIgCIIgCIIgCOJv8j9kuybFJ8+yXAAAAABJRU5ErkJggg=='
				Post.img_url = img_url
			if commit:
				Post.save()
			return Post
	
		