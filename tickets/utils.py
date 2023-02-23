def get_alert(level, instance, model, department):
    """
    levl: user level 
    instance : the save instance ticket
    model : User model for getting a particuler user
    department: department to get he department superior email  
    """
    if department: 

        if level == 'analyst' and instance.publish:
            """Get the supervisor email attach to the department."""
            supervisor_email = department.supervisor.email
            print('supervisor again')


            """
            * Todo: Send email notifying the supervisor of the department an alert 
            """

        elif level == 'supervisor' and instance.publish:
            """Get the head of department email."""
            head_of_department_email = department.head_of_department.email

            """
            * Todo: Send email notifying the head of department an alert
            """

        elif level == 'head of department' and instance.publish:
            """Get the company cto/cfo email"""
            cto_or_cfo = model.objects.filter(level__name='cto / cfo').first()
            cto_or_cfo_email = cto_or_cfo.email

            """
            * Todo: Send email to the cto/cfo of the company an alert 
            """

        elif level == 'cto / cfo' and instance.publish:
            """Get the company president email"""
            president = model.objects.filter(level__name = 'president').first()
            president_email = president.email 

            """
            * Todo: Send email to the company president
            """

        elif level == 'president' and instance.publish:
            """Get the CEO email"""
            ceo = model.objects.filter(level__name = 'ceo').first()
            ceo_email = ceo.email 

            """
            * Todo: Send email to the CEO of the president
            """                    
