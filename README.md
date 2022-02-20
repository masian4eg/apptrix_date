1. Create django-project, create model Profile
2. Create login with django-allauth 
Login page - app/accounts/login
Profile page - app/profiles/myprofile/ (can update info)
3. Create method to add watermark on avatar
4. Create class Relationship and methods for liking between users
/profiles/all_profiles/ - list of all profiles
/profiles/{id} - profiles detail
/profiles/my_match/ - list of received likes

![img.png](img.png)

Add mail-function in method of Relationship
5. Add lib django-filters for search by users gender, first name, last name.
/profiles/all_profiles/