"""
find . -type d -name '__pycache__' -exec rm -r {} +
find . -path '*/migrations/*' ! -name '__init__.py' -type f -exec rm -f {} +
Explanation:

    find .: Starts the search from the current directory.
    -type d -name '__pycache__': Finds directories named __pycache__.
    -exec rm -r {} +: Deletes all found directories and their contents.
    -path '*/migrations/*': Finds all files inside any migrations directory.
    ! -name '__init__.py': Excludes __init__.py from the match.
    -type f -exec rm -f {} +: Deletes all matched files.

    




if u want to make scripts
step 1:nano clean_project.sh
step 2:Add
#!/bin/bash

# Delete all __pycache__ directories
find . -type d -name '__pycache__' -exec rm -r {} +

# Delete all files inside migrations directories except __init__.py
find . -path '*/migrations/*' ! -name '__init__.py' -type f -exec rm -f {} +

STEP 3:Make the script executable:
chmod +x clean_project.sh


step:4
./clean_project.sh




  def create(self, validated_data):
        request = self.context.get('request')
        if request and request.get_host():
            domain_name = request.get_host().split(':')[0]
            tenant = Tenant.get_tenant_by_domain(domain_name)
            if tenant:
                user = User(**validated_data)
                user.tenant = tenant
                user.set_password(validated_data['password'])
                user.save()
                return user
            else:
                raise CustomAPIException("No Tenants available")


"""
